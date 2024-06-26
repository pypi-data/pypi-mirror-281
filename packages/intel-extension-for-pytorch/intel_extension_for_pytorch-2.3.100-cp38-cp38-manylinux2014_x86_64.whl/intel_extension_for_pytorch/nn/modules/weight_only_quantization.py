import torch
from torch import nn
from intel_extension_for_pytorch.nn.utils._weight_prepack import (
    may_import_deepspeed_modules,
    _all_reduce_and_bias_add,
    _pre_ipex_gemm,
)
from intel_extension_for_pytorch.quantization import (
    QConfigWoq,
    quantize_per_channel,
    quantize_per_block,
    WoqWeightDtype,
)
from ...utils._logger import logger, WarningType


class WeightOnlyQuantizedLinear(nn.Module):
    r"""
    A weight-only quantized (WOQ) linear module with floating point tensor as inputs and outputs.
    Weight is dequantized at runtime for computation.
    """

    def __init__(
        self, in_features, out_features, bias_=True, dtype=WoqWeightDtype.INT8
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias_
        self.dtype = dtype
        # This weight attribute is for queries of dtype, shape, etc.
        # It is a reference of the packed weight in self._op_context
        # The shape is not necessarily = [out_features, in_features] due to packing
        # Its dtype is torch.int8 for INT8 and torch.uint8 for INT4
        self.weight = None
        self._op_context = None
        self._lowp_mode = 0
        self._act_quant_mode = 0
        self._group_size = -1

    def pre_ipex_gemm(self, input):
        return input

    def post_ipex_gemm(self, output):
        return output

    def forward(self, x):
        x = self.pre_ipex_gemm(x)

        Y = torch.ops.torch_ipex.ipex_woq_linear(x, self._op_context.get_data_handle())

        return self.post_ipex_gemm(Y)

    def _get_name(self):
        return "WeightOnlyQuantizedLinear"

    def extra_repr(self):
        extra_repr_str = "in_features={}, out_features={}, dtype={}".format(
            self.in_features, self.out_features, self.dtype
        )
        extra_repr_str += ", bias={}".format(self.bias)
        extra_repr_str += ", lowp_mode={}".format(self._lowp_mode)
        extra_repr_str += ", act_quant_mode={}".format(self._act_quant_mode)
        extra_repr_str += ", group_size={}".format(self._group_size)
        return extra_repr_str

    @classmethod
    def from_float(cls, mod, scales=None, zero_points=None):
        r"""Create a weight-only quantized module from a float module or qparams_dict

        Args:
            mod (Module): an instance of nn.Linear or its subclasses.
            scales: the scales Tensor for quantizing weight. If it is None,
                scales are found by min/max of the weight.
            zero_points: the zero points Tensor for quantizing weight. If it is None,
                zero points are found by min/max of the weight.
        """
        float_modules = [torch.nn.Linear]
        deepspeed_modules = may_import_deepspeed_modules()
        if deepspeed_modules is not None:
            float_modules.extend(deepspeed_modules)
        if any(issubclass(type(mod), float_module) for float_module in float_modules):
            float_modules.extend([type(mod)])

        assert type(mod) in float_modules, (
            "WeightOnlyQuantizedLinear.from_float only works for one of"
            + str([float_mod.__name__ for float_mod in float_modules])
            + f" or their subclasses, but found {type(mod)}"
        )
        assert hasattr(mod, "qconfig"), "Input float module must have qconfig defined"
        qconfig = mod.qconfig
        if qconfig is None or not isinstance(qconfig, QConfigWoq):
            return mod

        lowp_mode = qconfig.lowp_mode
        if qconfig.lowp_mode == 3 and qconfig.weight_dtype == WoqWeightDtype.INT8:
            # lowp_mode=3 (INT8) is not supported for INT8 weight
            # Fall back to lowp_mode=2 in such case
            # TODO(Weiwen) Support lowp_mode=3
            lowp_mode = 2
            logger.warning(
                "Warning: lowp_mode=3(INT8) is not supported yet for INT8 weight. "
                + "Falling back to 2(BF16).",
                _type=WarningType.NotSupported,
            )
        act_quant_mode = qconfig.act_quant_mode
        dtype = qconfig.weight_dtype
        group_size = qconfig.group_size

        if group_size == -1:
            qweight, scales, zero_points = quantize_per_channel(
                mod.weight, dtype, scales, zero_points
            )
        else:
            qweight, scales, zero_points = quantize_per_block(
                mod.weight, dtype, group_size, scales, zero_points
            )
        if not hasattr(mod, "in_features"):
            mod.in_features = mod.weight.size()[1]
        if not hasattr(mod, "out_features"):
            mod.out_features = mod.weight.size()[0]

        qlinear = cls._init_cls(
            mod,
            dtype,
            qweight,
            scales,
            zero_points,
            None,  # g_idx
            group_size,
            lowp_mode,
            act_quant_mode,
        )
        del qweight
        return qlinear

    @classmethod
    def from_float_and_int4_weight(
        cls, mod, qweight, scales, zero_points, bias=None, group_size=-1, g_idx=None
    ):
        r"""Create a weight-only quantized module from a float module and int4 weight

        Args:
            mod (Module): a float module, either produced by torch.ao.quantization
                          utilities or provided by the user
            qweight (Tensor): tensor in int32 dtype and contains actually int4 data
            bias (Tensor or None): bias for linear
            scales (Tensor): scales for qweight
            zero_points (Tensor): zero points for qweight
            group_size: Group size for weight quantization
            g_idx: Indices of groups for each input channel of weight. Generated by
                GPTQ with act-order.
        """
        float_modules = [torch.nn.Linear]
        deepspeed_modules = may_import_deepspeed_modules()
        if deepspeed_modules is not None:
            float_modules.extend(deepspeed_modules)
        if any(issubclass(type(mod), float_module) for float_module in float_modules):
            float_modules.extend([type(mod)])

        assert type(mod) in float_modules, (
            "WeightOnlyQuantizedLinear.from_float only works for one of"
            + str([float_mod.__name__ for float_mod in float_modules])
            + f" or their subclasses, but found {type(mod)}"
        )
        assert hasattr(mod, "qconfig"), "Input float module must have qconfig defined"

        lowp_mode = 0
        act_quant_mode = 0
        if mod.qconfig is not None:
            if hasattr(mod.qconfig, "lowp_mode"):
                lowp_mode = mod.qconfig.lowp_mode
            if hasattr(mod.qconfig, "act_quant_mode"):
                act_quant_mode = mod.qconfig.act_quant_mode

        w_dtype = qweight.dtype
        supported_qw_dtype = [
            torch.int32,
            torch.uint8,
            torch.quint4x2,
            torch.bfloat16,
            torch.float32,
        ]
        assert (
            w_dtype in supported_qw_dtype
        ), "Data type of int4 weight should be in {}, but got: {}".format(
            supported_qw_dtype, w_dtype
        )
        if not hasattr(mod, "in_features"):
            mod.in_features = mod.weight.size()[1]
        if not hasattr(mod, "out_features"):
            mod.out_features = mod.weight.size()[0]

        qlinear = cls(mod.in_features, mod.out_features, dtype=WoqWeightDtype.INT4)
        if bias is None:
            bias = mod.bias
        qlinear._op_context = torch.ops.ipex_prepack.weight_only_qlinear_prepack_int4(
            qweight,
            scales,
            zero_points,
            bias,
            g_idx,
            None,
            group_size,
            int(lowp_mode),
            act_quant_mode,
        )
        qlinear.weight = qlinear._op_context.get_weight()
        qlinear._lowp_mode = lowp_mode
        qlinear._act_quant_mode = act_quant_mode
        qlinear._group_size = group_size
        del qweight
        return qlinear

    @classmethod
    def _init_cls(
        cls,
        mod,
        dtype,
        qweight,
        scales,
        zero_points,
        g_idx,
        group_size,
        lowp_mode,
        act_quant_mode,
    ):
        qlinear = cls(
            mod.in_features, mod.out_features, mod.bias is not None, dtype=dtype
        )
        qlinear._op_context = torch.ops.ipex_prepack.weight_only_qlinear_prepack(
            qweight,
            dtype,
            [mod.out_features, mod.in_features],
            scales,
            zero_points,
            mod.bias,
            g_idx,
            None,
            group_size,
            int(lowp_mode),
            act_quant_mode,
        )
        qlinear.weight = qlinear._op_context.get_weight()
        qlinear._lowp_mode = lowp_mode
        qlinear._act_quant_mode = act_quant_mode
        qlinear._group_size = group_size
        return qlinear


class IpexWoqLinearAllreduce(WeightOnlyQuantizedLinear):
    def __init__(
        self,
        in_features,
        out_features,
        mp_group,
        bias_value,
        bias_=True,
        dtype=WoqWeightDtype.INT8,
    ):
        # Save the original bias here
        # For bias handling, please refer to the comment in __init__ of _IPEXLinearAllreduce
        super().__init__(in_features, out_features, bias_, dtype=dtype)
        self.mp_group = mp_group
        self.original_bias = bias_value

    @classmethod
    def _init_from_mod(cls, mod, dtype):
        return cls(
            mod.in_features,
            mod.out_features,
            mod.mp_group,
            mod.bias,  # save the original bias value
            dtype=dtype,
        )

    @classmethod
    def _init_cls(
        cls,
        mod,
        dtype,
        qweight,
        scales,
        zero_points,
        g_idx,
        group_size,
        lowp_mode,
        act_quant_mode,
    ):
        qlinear = cls._init_from_mod(mod, dtype)

        qlinear._op_context = torch.ops.ipex_prepack.weight_only_qlinear_prepack(
            qweight,
            dtype,
            [mod.out_features, mod.in_features],
            scales,
            zero_points,
            None,  # Set bias to None when prepacking. Please refer to the comment in __init__ of _IPEXLinearAllreduce
            g_idx,
            None,  # batch_size
            group_size,
            lowp_mode,
            act_quant_mode,
        )
        qlinear.weight = qlinear._op_context.get_weight()

        return qlinear

    def post_ipex_gemm(self, output):
        return _all_reduce_and_bias_add(self.mp_group, self.original_bias, output)


class IpexWoqLmHeadLinearAllreduce(IpexWoqLinearAllreduce):
    def __init__(
        self,
        in_features,
        out_features,
        mp_group,
        rank,
        world_size,
        bias_value,
        bias_=True,
        dtype=WoqWeightDtype.INT8,
    ):
        # Save the original bias here
        # For bias handling, please refer to the comment in __init__ of _IPEXLinearAllreduce
        super().__init__(in_features, out_features, mp_group, bias_value, bias_, dtype)
        self.rank = rank
        self.world_size = world_size

    @classmethod
    def _init_from_mod(cls, mod, dtype):
        return cls(
            mod.in_features,
            mod.out_features,
            mod.mp_group,
            mod.rank,
            mod.world_size,
            mod.bias,  # save the original bias value
            dtype=dtype,
        )

    def pre_ipex_gemm(self, input):
        return _pre_ipex_gemm(input, self.world_size, self.rank)

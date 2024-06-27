import unittest
from itertools import product
from parameterized import parameterized

import torch
import torch.nn as nn

from lycoris.modules import (
    LycorisBaseModule,
    LoConModule,
    LohaModule,
    LokrModule,
    FullModule,
    DiagOFTModule,
    ButterflyOFTModule,
    GLoRAModule,
    DyLoraModule,
    IA3Module,
)


modules: list[LycorisBaseModule] = [
    LoConModule,
    LohaModule,
    LokrModule,
    FullModule,
    DiagOFTModule,
    ButterflyOFTModule,
    GLoRAModule,
    DyLoraModule,
    IA3Module,
]
base_module_and_input = [
    lambda dim: (nn.Linear(dim, dim), torch.randn(1, dim)),
    lambda dim: (nn.Conv1d(dim, dim, 3, 1, 1), torch.randn(1, dim, 16)),
    lambda dim: (nn.Conv2d(dim, dim, (3, 3), 1, 1), torch.randn(1, dim, 16, 16)),
    # lambda dim: (nn.Conv3d(dim, dim, (3, 3, 3), 1, 1), torch.randn(1, dim, 16, 16, 16)),
]
device_and_dtype = [
    (torch.device("cpu"), torch.float32),
]
weight_decompose = [False, True]
use_tucker = [False, True]
use_scalar = [False, True]

if torch.cuda.is_available():
    device_and_dtype.append((torch.device("cuda"), torch.float32))
    device_and_dtype.append((torch.device("cuda"), torch.float16))
    device_and_dtype.append((torch.device("cuda"), torch.bfloat16))

if torch.backends.mps.is_available():
    device_and_dtype.append((torch.device("mps"), torch.float32))


patch_forward_param_list = list(
    product(
        modules,
        base_module_and_input,
        device_and_dtype,
        weight_decompose,
        use_tucker,
        use_scalar,
    )
)


class LycorisModuleTests(unittest.TestCase):
    @parameterized.expand(patch_forward_param_list)
    def test_lycoris_functional(self, module, base, device_dtype, wd, tucker, scalar):
        base, test_input = base(16)
        device, dtype = device_dtype

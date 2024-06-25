# Pytorch extension written in rust

A demo pytorch (2.3.0) package using [maturin](https://github.com/PyO3/maturin) and [tch](https://github.com/LaurentMazare/tch-rs).

## Build in a venv

```bash
# Create and activate a venv
python -m venv .venv
source .venv/bin/activate
# Install maturin
pip install maturin
# Build the torch_lib_with_rust package with maturin
LIBTORCH_USE_PYTORCH=1 maturin develop
```

## Run

```python
import torch
import torch_lib_with_rust

a=torch.randn(16).to("cuda")

print(a)
print(torch_lib_with_rust.add_one(a))
```
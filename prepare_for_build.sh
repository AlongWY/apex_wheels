python -m pip install -U pip setuptools wheel packaging auditwheel-symbols ninja cmake numpy
# We want to figure out the CUDA version to download pytorch
# e.g. we can have system CUDA version being 11.7 but if torch==1.12 then we need to download the wheel from cu116
# see https://github.com/pytorch/pytorch/blob/main/RELEASE.md#release-compatibility-matrix
# This code is ugly, maybe there's a better way to do this.
export TORCH_CUDA_VERSION=$(python -c "from os import environ as env; \
    minv = {'1.12': 113, '1.13': 116, '2.0': 117, '2.1': 118, '2.2': 118, '2.3': 118, '2.4': 118}[env['MATRIX_TORCH_VERSION']]; \
    maxv = {'1.12': 116, '1.13': 117, '2.0': 118, '2.1': 121, '2.2': 121, '2.3': 121, '2.4': 124}[env['MATRIX_TORCH_VERSION']]; \
    print(max(min(int(env['MATRIX_CUDA_VERSION']), maxv), minv))" \
)

ls -l /usr/local
rm /usr/local/cuda
ln -s /usr/local/cuda-${MANYLINUX_CUDA_VERSION} /usr/local/cuda

which python
which pip
which nvcc

python --version
python -m pip --version
gcc --version
nvcc --version

echo "install torch==${CI_TORCH_VERSION}+cu${TORCH_CUDA_VERSION}"
python -m pip install --no-cache-dir torch==${CI_TORCH_VERSION} --index-url https://download.pytorch.org/whl/cu${TORCH_CUDA_VERSION}

# todo: search with regex
echo "$(git describe --tags)+cu${TORCH_CUDA_VERSION}torch${CI_TORCH_VERSION}"
sed -i "s/version=\"0.1\"/version=\"$(git describe --tags)+cu${TORCH_CUDA_VERSION}torch${CI_TORCH_VERSION}\"/g" /project/setup.py

# sed append [tool.cibuildwheel]
# build-frontend = { name = "pip", args = ["--no-build-isolation"] }
sed -i '$a [tool.cibuildwheel]\nbuild-frontend = { name = "pip", args = ["--no-build-isolation", "--no-cache-dir", "--disable-pip-version-check"] }' /project/pyproject.toml

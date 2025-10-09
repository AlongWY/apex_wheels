# see https://github.com/pytorch/pytorch/blob/main/RELEASE.md#release-compatibility-matrix
import yaml

versions = {
    "2.3.1": {"python": [8, 9, 10, 11], "cuda": [118, 121], "deepcompile": 0},
    "2.4.1": {"python": [8, 9, 10, 11], "cuda": [118, 121, 124], "deepcompile": 0},
    "2.5.1": {"python": [9, 10, 11, 12], "cuda": [118, 121, 124], "deepcompile": 0},
    "2.6.0": {"python": [9, 10, 11, 12], "cuda": [118, 124, 126], "deepcompile": 1},
    "2.7.1": {"python": [9, 10, 11, 12, 13], "cuda": [118, 126, 128], "deepcompile": 1},
    "2.8.0": {"python": [9, 10, 11, 12, 13], "cuda": [126, 128, 129], "deepcompile": 1},
}

cuda_version_mapping = {
    118: "11.8.0",
    121: "12.1.1",
    124: "12.4.0",
    126: "12.6.0",
    128: "12.8.0",
    129: "12.9.0",
}

cuda_arch = {
    "11.3.0": "7.0;7.5;8.0;8.6+PTX",
    "11.6.0": "7.0;7.5;8.0;8.6+PTX",
    "11.7.0": "7.0;7.5;8.0;8.6+PTX",
    "11.8.0": "7.0;7.5;8.0;8.6;9.0+PTX",
    "12.1.1": "7.0;7.5;8.0;8.6;9.0+PTX",
    "12.4.0": "7.0;7.5;8.0;8.6;9.0+PTX",
    "12.6.0": "7.0;7.5;8.0;8.6;9.0+PTX",
    "12.8.0": "7.0;7.5;8.0;8.6;9.0;10.0;12.0+PTX",
    "12.9.0": "7.0;7.5;8.0;8.6;9.0;10.0;12.0+PTX",
    "13.0.0": "7.5;8.0;8.6;9.0;10.0;12.0+PTX",
}

pairs_set = set()
pairs = []
for torch_version, pycu in versions.items():
    for python_version in pycu["python"]:
        python_version = f"3.{python_version}"
        for raw_cuda_version in pycu["cuda"]:
            cuda_version = cuda_version_mapping[raw_cuda_version]
            pair = (torch_version, python_version, cuda_version, raw_cuda_version)
            if pair not in pairs_set:
                pairs.append(pair)
                pairs_set.add(pair)

for torch_version, python_version, cuda_version, raw_cuda_version in pairs:
    print(f'- torch-version: "{torch_version}"')
    print(f'  python-version: "{python_version}"')
    print(f'  cuda-version: "{cuda_version}"')
    print(f'  arch: "{cuda_arch[cuda_version]}"')
    # print(f"  deepcompile: {versions[torch_version]['deepcompile']}")

    print(f'  cibw-build: "cp{python_version.replace(".", "")}-*64"')
    print(f'  cibw-build-image: "pytorch/manylinux2_28-builder:cuda{cuda_version[:-2]}"')
    print(f'  cibw-build-cuda-version: "{cuda_version[:-2]}"')
    print(f'  cibw-build-torch-cuda-version: "{raw_cuda_version}"')
    print(f'  cibw-build-cuda-compat-version: "{cuda_version[:-2].replace(".", "-")}"')
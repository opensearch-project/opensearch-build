import subprocess


def current_arch():
    arch = subprocess.check_output(['uname', '-m']).decode().strip()
    if arch == 'x86_64':
        return 'x64'
    elif arch == 'aarch64' or arch == 'arm64':
        return  'arm64'
    else:
        raise ValueError(f'Unsupported architecture: {arch}')

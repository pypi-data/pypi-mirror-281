import ctypes
import platform

# 加载共享对象文件
system = platform.system()
architecture = platform.machine()
if system == 'Linux':
    if architecture == 'x86_64':
        lib_path = 'bin/rsa_darwin_arm64.so'
    else:
        raise Exception(f"Unsupported architecture: {architecture} on Linux")
elif system == 'Darwin':
    if architecture == 'arm64':
        lib_path = 'bin/rsa_darwin_arm64.so'
    else:
        raise Exception(f"Unsupported architecture: {architecture} on macOS")
else:
    raise Exception(f"Unsupported system: {system}")

sign_lib = ctypes.CDLL(lib_path)

# 设置Sign函数的参数类型和返回类型
sign_lib.Sign.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool]
sign_lib.Sign.restype = ctypes.c_char_p


def encrypt_by_rsa_private_key(message: str, private_key: str, is_random: bool, hex_format: bool) -> str:
    # 调用Sign函数
    result = sign_lib.Sign(message.encode('utf-8'), private_key.encode('utf-8'), is_random, hex_format)
    return result.decode('utf-8')

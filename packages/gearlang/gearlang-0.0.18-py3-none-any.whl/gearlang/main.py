import ctypes
from os import path
import sys
import importlib.metadata
import platform


def cli():
    clib_call(sys.argv)


def getlib() -> str:
    if path.exists(path.join(path.dirname(__file__), 'clibs', 'gear-dev.so')):
        print('\n\t!!! Using development version of the library !!!')
        return 'gear-dev.so'

    match sys.platform:
        case 'win32':
            match platform.machine().lower():
                case 'amd64':   # x86_64
                    return 'gear_windows_amd64.dll'
                case 'x86_64':
                    return 'gear_windows_amd64.dll'
                case 'ARM64':
                    return 'gear_windows_arm64.dll'
                case _:
                    raise OSError('Your Windows system architecture is not supported')

        case 'darwin':
            match platform.machine().lower():
                case 'x86_64':
                    return 'gear_darwin_amd64.dylib'
                case 'arm64':
                    return 'gear_darwin_arm64.dylib'
                case _:
                    raise OSError('Your MacOS system architecture is not supported')

        case 'linux':
            match platform.machine():
                case 'x86_64':
                    return 'gear_linux_amd64.so'
                case 'aarch64':
                    return 'gear_linux_arm64.so'
                case 'armv7l':
                    return 'gear_linux_armv7.so'
                case _:
                    raise OSError('Your Linux system architecture is not supported')

        case _:
            raise OSError('Your system is not supported')


def clib_call(args: list[str]):
    try:
        version: str = importlib.metadata.version('gearlang')
    except importlib.metadata.PackageNotFoundError:
        version: str = '0.0.0.0'
    clib = ctypes.CDLL(path.join(path.dirname(__file__), 'clibs', getlib()))

    clib.libMain.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    clib.libMain.restype = None

    # Prepare args
    argc = len(args)
    argv = (ctypes.POINTER(ctypes.c_char) * argc)()
    ver = ctypes.create_string_buffer(version.encode('utf-8'))

    for i, arg in enumerate(args):
        argv[i] = ctypes.create_string_buffer(arg.encode('utf-8'))

    clib.libMain(argc, argv, ver)


if __name__ == '__main__':
    # print(sys.argv)
    # cli(['gear', 'build'])
    cli()

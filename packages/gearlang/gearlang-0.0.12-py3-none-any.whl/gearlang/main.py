import ctypes
from os import path
import sys
import importlib.metadata


def cli():
    clib_call(sys.argv)


def clib_call(args: list[str]):
    try:
        version: str = importlib.metadata.version('gearlang')
    except importlib.metadata.PackageNotFoundError:
        version: str = '0.0.0.0'
    clib = ctypes.CDLL(path.join(path.dirname(__file__), 'clibs', 'gear.so'))

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

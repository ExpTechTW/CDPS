import io
import sys
import warnings


def boostrap():
    for name, stream in {'sys.stdout': sys.stdout, 'sys.stderr': sys.stderr}.items():
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(line_buffering=True)
        else:
            warnings.warn(
                '{} {} is not a io.TextIOWrapper, cannot apply reconfigure'.format(name, stream))

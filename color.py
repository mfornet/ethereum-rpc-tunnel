import io
from termcolor import colored


def _color(*args, color, **kwargs):
    buffer = io.StringIO()
    print(*args, **kwargs, file=buffer)
    print(colored(buffer.getvalue(), color))


def _register(fn):
    def inner(*args, **kwargs):
        _color(*args, color=fn.__name__, **kwargs)
    return inner


class Print:
    @_register
    def green(): ...

    @_register
    def red(): ...

    @_register
    def cyan(): ...

    @_register
    def blue(): ...

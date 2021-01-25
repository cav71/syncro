import click
import functools
import logging


class CliBase:
    @classmethod
    def cli(cls, *args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return functools.wraps(args[0])(cls()._set(args[0]))
        else:
            def _fn(fn):
                return cls((args, kwargs))._set(fn)
            return _fn

    def __init__(self, arguments=None):
        self.arguments = arguments

    def _set(self, fn):
        self.fn = fn
        return functools.wraps(fn)(self.wrapper() or self)

    def __call__(self, *args, **kwargs):
        args, kwargs = self.before(self.arguments, self.fn, *args, **kwargs) or (args, kwargs)
        result = self.fn(*args, **kwargs)

    def wrapper(self):
        pass

    def before(self, arguments, fn, *args, **kwargs):
        pass


class Cli(CliBase):
    def wrapper(self):
        fn1 = click.option("-v", "--verbose", count=True)(self)
        fn1 = click.option("-q", "--quiet", count=True)(fn1)
        return fn1

    def before(self, arguments, fn, *args, **kwargs):
        level = kwargs.pop("verbose") - kwargs.pop("quiet")
        arguments = arguments or ((), {})
        if arguments[1].get("quiet", False):
            level -= 1
        level = logging.INFO if level == 0 else (logging.DEBUG if level > 0 else logging.WARN)
        logging.basicConfig(level=level)
        return args, kwargs


cli = Cli.cli

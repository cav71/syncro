import click
import functools


class Deco:
    def __init__(self, *args, **kwargs):
        self.arguments = args, kwargs
        if len(args) == 1 and callable(args[0]) and not kwargs:
            self.fn = self.wrapper(args[0]) or args[0]
            self.__name__ = args[0].__name__
            self.__doc__ = args[0].__doc__
        else:
            self.fn = None

    def __call__(self, *args, **kwargs):
        if not self.fn:
            if len(args) == 1 and callable(args[0]) and not kwargs:
                deco = Deco(args[0])
                deco.arguments = self.arguments
                return deco
            raise RuntimeError("invalid decorator call")
        self.before(self.arguments, self.fn, *args, **kwargs)
        result = self.fn(*args, **kwargs)
        return self.after(self.arguments, self.fn, result)

    def wrapper(self, fn):
        print(f"wrapper {arguments=} {fn=}")
        fn1 = click.option("-v", "--verbose", count=True)(fn)
        fn1 = click.option("-q", "--quiet", count=True)(fn1)
        return functools.wraps(fn)(fn1)

    def before(self, arguments, fn, *args, **kwargs):
        print(f"before {arguments=} {fn=} {args=} {kwargs=}")

    def after(self, arguments, fn, result):
        print(f"after {arguments=} {fn=} {result=}")


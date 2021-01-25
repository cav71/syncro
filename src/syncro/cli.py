import click
import functools


class Deco:
    def __init__(self, *args, **kwargs):
        self.arguments = args, kwargs
        if len(args) == 1 and callable(args[0]) and not kwargs:
            self.fn = self.wrapper(None, args[0]) or args[0]
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

    def wrapper(self, arguments, fn):
        print(f"init {arguments=} {fn=}")
        fn = click.option("-v", "--verbose=", count=True)
        fn = click.option("-q", "--quiet=", count=True)

    def before(self, arguments, fn, *args, **kwargs):
        print(f"before {arguments=} {fn=} {args=} {kwargs=}")

    def after(self, arguments, fn, result):
        print(f"after {arguments=} {fn=} {result=}")


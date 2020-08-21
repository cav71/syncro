import argparse
import functools
import contextlib
import inspect
import logging


class CliError(Exception):
    """raised when an option is invalid"""
    pass


class CliBase(object):
    """base cli decorator


    This class can be used as:
        
        @CliBase
        def main(options):
            ...

        or 
        @CliBase(1, b=2)
        def main(options):
            ...

    These will result in calls as:
        CliBase.DRIVER(main, sys.argv[1:])
        CliBase.DRIVER(main, sys.argv[1:], 1, b=2)


    The main entry point can be exposed as an API as well:
        main([ "--opt", "val", ]) -> in this case the usual argparse parsing (including errors)
        main(object) -> this won't process the argument parsing
        

    """

    DRIVER = None

    def __init__(self, *args, **kwargs):
        self.main, self.arguments = None, None
        if (not kwargs) and (len(args) == 1) and callable(args[0]):
            # called as in @cli
            self.main = args[0]
            self.__doc__ = self.main.__doc__
        else:
            # called as in @cli(...)
            self.arguments = (args, kwargs)

    def __call__(self, *args, **kwargs):
        assert self.__class__.DRIVER, \
            '{0}.DRIVER must be defined'.format(self.__class__.__name__)
        # only positional args
        assert not kwargs

        # dispacth/handle cases for main(), main(None)
        def syargv_fixer(args, allow_none=0):
            if allow_none:
                return [] if not args else (None if args == (None,) else args[0])
            else:
                if args == (None,):
                    raise RuntimeError("cannot call <main>(None)")
                return None if not args else args[0]

        ctx = argparse.Namespace(
            main=self.main,
            sys_argv=self.arguments,
            args=(),
            kwargs={}
        )

        # logic is complex
        if self.main:
            ctx.sys_argv = syargv_fixer(args)
            with self.__class__.DRIVER(ctx.main, ctx.sys_argv, *ctx.args, **ctx.kwargs) as options:
                return ctx.main(*options) if isinstance(options, (list, tuple)) else \
                        ctx.main(options)
        else:
            ctx.main = args[0]
            ctx.args, ctx.kwargs = self.arguments

            @functools.wraps(ctx.main)
            def _inner(*args, **kwargs):
                assert not kwargs
                ctx.sys_argv = syargv_fixer(args)
                with self.__class__.DRIVER(ctx.main, ctx.sys_argv, *ctx.args, **ctx.kwargs) as options:
                    return ctx.main(*options) if isinstance(options, (list, tuple)) else \
                        ctx.main(options)

            return _inner


@contextlib.contextmanager
def driver(main, sys_argv, *args, **kwargs):
    mod = inspect.getmodule(main)
    name = mod.__name__
    description, _, epilog = (mod.__doc__ or "").lstrip().partition("\n")

    options = sys_argv
    if isinstance(options, (tuple, list, None.__class__)):
        class MyFormatter(argparse.ArgumentDefaultsHelpFormatter, 
                            argparse.RawDescriptionHelpFormatter):
            pass
        parser = argparse.ArgumentParser(
            description=description, epilog=epilog, formatter_class=MyFormatter)

        parser.add_argument("-v", "--verbose", action="store_true")
        getattr(mod, "add_arguments", lambda p: True)(parser)

        options = parser.parse_args(sys_argv)
        try:
            options = getattr(mod, "process_options", lambda o: None)(options) or options
        except CliError as e:
            parser.error(e)


    logging.basicConfig(level=logging.DEBUG if options.verbose else logging.INFO)
    yield options


class Cli(CliBase):
    DRIVER = driver

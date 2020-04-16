import logging
import optparse
from distutils import cmd

# A hacky way to determine which version of python we are running on
# Pyqver2 relies on the removed module "compiler" and will error out without it
try:
    from pyqver import pyqver2 as pyqver_runner
except:
    from pyqver import pyqver3 as pyqver_runner
from pyqver import pyqverbase

log = logging.getLogger(__name__)


class BaseCommand(cmd.Command):
    """Command is an abstract class that requires initialize_options, finalize_options,
    and user_options to be defined.  This class provides stub definitions and other
    utility methods.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def register_opt(parser, *args, **kwargs):
    try:
        # Flake8 3.x registration
        parser.add_option(*args, **kwargs)
    except (optparse.OptionError, TypeError):
        # Flake8 2.x registration
        parse_from_config = kwargs.pop('parse_from_config', False)
        kwargs.pop('comma_separated_list', False)
        kwargs.pop('normalize_paths', False)
        parser.add_option(*args, **kwargs)
        if parse_from_config:
            parser.config_options.append(args[-1].lstrip('-'))


class PyqverChecker(object):
    name = "pyqverChecker"
    version = "1.4"
    min_version = "2.5"

    def __init__(self, tree, filename, *args, **kwargs):
        self.tree = tree
        self.filename = filename

        self.args = args
        self.kwargs = kwargs

        self.results = []

    @classmethod
    def register_options(cls, parser):
        register_opt(parser, '--min-version',
                     type='string',
                     action='store',
                     default='2.5',
                     parse_from_config=True,
                     help="The min version of python to check. For ex, '2.6' will show code only supported in 2.7 or newer")

    def provide_options(self, options):
        log.debug(options)
        self.min_version = tuple(map(int, options.min_version.split(".")))

    def usage_exit(self):
        pass

    def begin(self, *args):
        pass

    def item(self, filename, version, reasons):
        for reason in reasons:
            ver = ".".join(map(str, version))
            err_ver = "".join(map(str, version))
            msg = "V%s0 (%s) %s" % (err_ver, ver, reason[1])

            line_number = reason[0]
            # else flake8 throws an exception doing math on NoneType and int
            if line_number is None:
                line_number = 1
            offset = 0
            ret = (line_number, offset, msg, type(self))
            self.results.append(ret)

    # yield ret = (lineno, col_offset, msg, self)
    def run(self):
        self.results = []

        # FIXME: get these monkeypatching globals off this module flaking plane
        pyqverbase._printer = self
        pyqverbase._min_version = self.min_version
        # This only has an effect if pyqver_runner is pyqver2, but we'd
        # like this to work for whichever major version of python this
        pyqver_runner._allow_caught_import_errors = True

        pyqverbase.evaluate_file(self.filename, pyqver_runner.get_versions)
        for line_number, column_number, message, checker_name in self.results:
            yield (line_number, column_number, message, checker_name)

#!/usr/bin/env python3

# Note to devs: Keep backwards compatibility with Python 3.0.

import ast
import platform
import sys
from pyqver.pyqverbase import run, Printer

DefaultMinVersion = (3, 0)

StandardModules = {
    "argparse":         (3, 2),
    "faulthandler":     (3, 3),
    "importlib":        (3, 1),
    "ipaddress":        (3, 3),
    "lzma":             (3, 3),
    "tkinter.ttk":      (3, 1),
    "unittest.mock":    (3, 3),
    "venv":             (3, 3),
}

Functions = {
    "bytearray.maketrans":                      (3, 1),
    "bytes.maketrans":                          (3, 1),
    "bz2.open":                                 (3, 3),
    "collections.Counter":                      (3, 1),
    "collections.OrderedDict":                  (3, 1),
    "crypt.mksalt":                             (3, 3),
    "email.generator.BytesGenerator":           (3, 2),
    "email.message_from_binary_file":           (3, 2),
    "email.message_from_bytes":                 (3, 2),
    "functools.lru_cache":                      (3, 2),
    "gzip.compress":                            (3, 2),
    "gzip.decompress":                          (3, 2),
    "inspect.getclosurevars":                   (3, 3),
    "inspect.getgeneratorlocals":               (3, 3),
    "inspect.getgeneratorstate":                (3, 2),
    "itertools.combinations_with_replacement":  (3, 1),
    "itertools.compress":                       (3, 1),
    "logging.config.dictConfig":                (3, 2),
    "logging.NullHandler":                      (3, 1),
    "math.erf":                                 (3, 2),
    "math.erfc":                                (3, 2),
    "math.expm1":                               (3, 2),
    "math.gamma":                               (3, 2),
    "math.isfinite":                            (3, 2),
    "math.lgamma":                              (3, 2),
    "math.log2":                                (3, 3),
    "os.environb":                              (3, 2),
    "os.fsdecode":                              (3, 2),
    "os.fsencode":                              (3, 2),
    "os.fwalk":                                 (3, 3),
    "os.getenvb":                               (3, 2),
    "os.get_exec_path":                         (3, 2),
    "os.getgrouplist":                          (3, 3),
    "os.getpriority":                           (3, 3),
    "os.getresgid":                             (3, 2),
    "os.getresuid":                             (3, 2),
    "os.get_terminal_size":                     (3, 3),
    "os.getxattr":                              (3, 3),
    "os.initgroups":                            (3, 2),
    "os.listxattr":                             (3, 3),
    "os.lockf":                                 (3, 3),
    "os.pipe2":                                 (3, 3),
    "os.posix_fadvise":                         (3, 3),
    "os.posix_fallocate":                       (3, 3),
    "os.pread":                                 (3, 3),
    "os.pwrite":                                (3, 3),
    "os.readv":                                 (3, 3),
    "os.removexattr":                           (3, 3),
    "os.replace":                               (3, 3),
    "os.sched_get_priority_max":                (3, 3),
    "os.sched_get_priority_min":                (3, 3),
    "os.sched_getaffinity":                     (3, 3),
    "os.sched_getparam":                        (3, 3),
    "os.sched_getscheduler":                    (3, 3),
    "os.sched_rr_get_interval":                 (3, 3),
    "os.sched_setaffinity":                     (3, 3),
    "os.sched_setparam":                        (3, 3),
    "os.sched_setscheduler":                    (3, 3),
    "os.sched_yield":                           (3, 3),
    "os.sendfile":                              (3, 3),
    "os.setpriority":                           (3, 3),
    "os.setresgid":                             (3, 2),
    "os.setresuid":                             (3, 2),
    "os.setxattr":                              (3, 3),
    "os.sync":                                  (3, 3),
    "os.truncate":                              (3, 3),
    "os.waitid":                                (3, 3),
    "os.writev":                                (3, 3),
    "shutil.chown":                             (3, 3),
    "shutil.disk_usage":                        (3, 3),
    "shutil.get_archive_formats":               (3, 3),
    "shutil.get_terminal_size":                 (3, 3),
    "shutil.get_unpack_formats":                (3, 3),
    "shutil.make_archive":                      (3, 3),
    "shutil.register_archive_format":           (3, 3),
    "shutil.register_unpack_format":            (3, 3),
    "shutil.unpack_archive":                    (3, 3),
    "shutil.unregister_archive_format":         (3, 3),
    "shutil.unregister_unpack_format":          (3, 3),
    "shutil.which":                             (3, 3),
    "signal.pthread_kill":                      (3, 3),
    "signal.pthread_sigmask":                   (3, 3),
    "signal.sigpending":                        (3, 3),
    "signal.sigtimedwait":                      (3, 3),
    "signal.sigwait":                           (3, 3),
    "signal.sigwaitinfo":                       (3, 3),
    "socket.CMSG_LEN":                          (3, 3),
    "socket.CMSG_SPACE":                        (3, 3),
    "socket.fromshare":                         (3, 3),
    "socket.if_indextoname":                    (3, 3),
    "socket.if_nameindex":                      (3, 3),
    "socket.if_nametoindex":                    (3, 3),
    "socket.sethostname":                       (3, 3),
    "ssl.match_hostname":                       (3, 2),
    "ssl.RAND_bytes":                           (3, 3),
    "ssl.RAND_pseudo_bytes":                    (3, 3),
    "ssl.SSLContext":                           (3, 2),
    "ssl.SSLEOFError":                          (3, 3),
    "ssl.SSLSyscallError":                      (3, 3),
    "ssl.SSLWantReadError":                     (3, 3),
    "ssl.SSLWantWriteError":                    (3, 3),
    "ssl.SSLZeroReturnError":                   (3, 3),
    "stat.filemode":                            (3, 3),
    "textwrap.indent":                          (3, 3),
    "threading.get_ident":                      (3, 3),
    "time.clock_getres":                        (3, 3),
    "time.clock_gettime":                       (3, 3),
    "time.clock_settime":                       (3, 3),
    "time.get_clock_info":                      (3, 3),
    "time.monotonic":                           (3, 3),
    "time.perf_counter":                        (3, 3),
    "time.process_time":                        (3, 3),
    "types.new_class":                          (3, 3),
    "types.prepare_class":                      (3, 3),
}

class NodeChecker(ast.NodeVisitor):
    """
    A visitor, which traverses the syntax tree to find possible
    version issues.

    After traversal, the member vers will contain a dictionary
    mapping versions in a (maj,min) tuple format to lists of issues.
    An issue is a tuple of the line number where the issue resides,
    and a short message describing the issue.

    Python 3 specific: Traversal is achieved by calling the visit member.
    """
    def __init__(self):
        self.vers = dict()
        self.vers[(3,0)] = []
    def add(self, node, ver, msg):
        if ver not in self.vers:
            self.vers[ver] = []
        self.vers[ver].append((node.lineno, msg))
    def visit_Call(self, node):
        def rollup(n):
            if isinstance(n, ast.Name):
                return n.id
            elif isinstance(n, ast.Attribute):
                r = rollup(n.value)
                if r:
                    return r + "." + n.attr
        name = rollup(node.func)
        if name:
            v = Functions.get(name)
            if v is not None:
                self.add(node, v, name)
        self.generic_visit(node)
    def visit_Import(self, node):
        for n in node.names:
            v = StandardModules.get(n.name)
            if v is not None:
                self.add(node, v, n.name)
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        v = StandardModules.get(node.module)
        if v is not None:
            self.add(node, v, node.module)
        for n in node.names:
            name = (node.module or "") + "." + n.name
            v = Functions.get(name)
            if v is not None:
                self.add(node, v, name)
    def visit_Raise(self, node):
        if isinstance(node.cause, ast.Name) and node.cause.id == "None":
            self.add(node, (3,3), "raise ... from None")
    def visit_YieldFrom(self, node):
        self.add(node, (3,3), "yield from")

def get_versions(source, filename=None):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 3.1 is (3,1)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = ast.parse(source, filename=filename)
    checker = NodeChecker()
    checker.visit(tree)
    return checker.vers

def v33(source):
    if sys.version_info >= (3, 3):
        return qver(source)
    else:
        print("Not all features tested, run --test with Python 3.3", file=sys.stderr)
        return (3, 3)

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print("hello world")')
    (3, 0)
    >>> qver("import importlib")
    (3, 1)
    >>> qver("from importlib import x")
    (3, 1)
    >>> qver("import tkinter.ttk")
    (3, 1)
    >>> qver("from collections import Counter")
    (3, 1)
    >>> qver("collections.OrderedDict()")
    (3, 1)
    >>> qver("import functools\\n@functools.lru_cache()\\ndef f(x): x*x")
    (3, 2)
    >>> v33("yield from x")
    (3, 3)
    >>> v33("raise x from None")
    (3, 3)
    """
    return max(get_versions(source).keys())

# Printer declarations

def print_usage_and_exit():
    print("""Usage: {0} [options] source ...

    Report minimum Python version required to run given source files.

    -m x.y or --min-version x.y (default 3.0)
        report version triggers at or above version x.y in verbose mode
    -v or --verbose
        print more detailed report of version triggers for each version
    -l or --lint
        print a report in the style of Lint, with line numbers
    """.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

def print_syntax_error(filename, err):
    print("{0}: syntax error compiling with Python {1}: {2}".format(filename, platform.python_version(), err))

def print_verbose_begin(filename, versions):
    print(filename)

def print_verbose_item(filename, version, reasons):
    if reasons:
        # each reason is (lineno, message)
        print("\t{0}\t{1}".format(".".join(map(str, version)), ", ".join(r[1] for r in reasons)))

verbose_printer = Printer(
    print_verbose_begin, print_verbose_item, print_syntax_error, print_usage_and_exit)
    
def print_lint_begin(filename, versions):
    pass

def print_lint_item(filename, version, reasons):
    for r in reasons:
        # each reason is (lineno, message)
        print("{0}:{1}: {2} {3}".format(filename, r[0], ".".join(map(str, version)), r[1]))

lint_printer = Printer(
    print_lint_begin, print_lint_item, print_syntax_error, print_usage_and_exit)

def print_compact_begin(filename, versions):
    print("{0}\t{1}".format(".".join(map(str, max(versions.keys()))), filename))

def print_compact_item(filename, version, reasons):
    pass

compact_printer = Printer(
    print_compact_begin, print_compact_item, print_syntax_error, print_usage_and_exit)

printers = {'verbose': verbose_printer,
            'lint': lint_printer,
            'compact': compact_printer}

def main():
    run(printers, DefaultMinVersion, get_versions)

if __name__=='__main__':
    main()

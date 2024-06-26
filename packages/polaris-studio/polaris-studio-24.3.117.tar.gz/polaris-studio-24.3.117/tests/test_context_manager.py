import tempfile
from contextlib import contextmanager
from os.path import join

from polaris.utils.database.db_utils import commit_and_close, safe_connect


def test_commit_and_close():
    with tempfile.TemporaryDirectory() as d:

        def row_count():
            c = safe_connect(join(d, "foo.sqlite"))
            count = c.execute("select count(*) from test;").fetchone()
            c.close()
            return count[0]

        # This has no effect on the files on disk as it lacks a commit
        c = safe_connect(join(d, "foo.sqlite"), missing_ok=True)
        c.execute("CREATE TABLE test(col1 text);")
        c.execute("INSERT INTO test VALUES('a');")
        assert (1,) == c.execute("select count(*) from test;").fetchone()
        c.close()
        assert row_count() == 0
        # ------------------------------------------------------------

        # This has no effect on the files on disk as it errors before finishing
        # the transaction block
        try:
            with safe_connect(join(d, "foo.sqlite"), missing_ok=True) as c:
                c.execute("INSERT INTO test VALUES('a');")
                raise RuntimeError("error")
        except Exception:
            c.close()
        assert row_count() == 0
        # ----------------------------------------------------------------------

        # This actually inserts a record -----------------
        with safe_connect(join(d, "foo.sqlite")) as c:
            c.execute("INSERT INTO test VALUES('a');")
        c.close()
        assert row_count() == 1

        # ------------------------------------------------

        def xxx():
            conn = safe_connect(join(d, "foo.sqlite"))
            return commit_and_close(conn)

        # This actually inserts a record -----------------
        with xxx() as c:
            c.execute("INSERT INTO test VALUES('a');")
        assert row_count() == 2
        # ------------------------------------------------

        # This should not insert a record ----------------
        try:
            with xxx() as c:
                c.execute("INSERT INTO test VALUES('a');")
                c.execute("SELECT fllogle();")
        except Exception:
            pass
        assert row_count() == 2
        # ------------------------------------------------

        # also should not insert a record (no commit) ----
        with commit_and_close(join(d, "foo.sqlite"), commit=False) as c:
            c.execute("INSERT INTO test VALUES('a');")
        assert row_count() == 2
        # ------------------------------------------------


class ArrayBracketer(object):
    def __init__(self, arr):
        self.arr = arr

    def __enter__(self):
        self.arr.append("before")
        return self.arr

    def __exit__(self, b, c, d):
        self.arr.append("after")


@contextmanager
def cont_manager_method(arr):
    with ArrayBracketer(arr) as arr_:
        arr_.append("2.1")
        yield arr_
        arr_.append("2.2")


def test_single_level():
    arr2 = []
    with ArrayBracketer(arr2) as f:
        f.append("x")
    assert ["before", "x", "after"] == arr2


def test_exit_is_called_when_raising():
    arr2 = []
    try:
        with ArrayBracketer(arr2) as f:
            f.append("x")
            raise RuntimeError("error")
    except Exception:
        pass
    assert ["before", "x", "after"] == arr2


def test_nested_levels():
    arr = []
    with cont_manager_method(arr) as f:
        f.append("x")
    assert ["before", "2.1", "x", "2.2", "after"] == arr


def test_can_return_them():
    def foo(x):
        return cont_manager_method(x)

    arr = []
    with foo(arr) as f:
        f.append("x")

    assert ["before", "2.1", "x", "2.2", "after"] == arr

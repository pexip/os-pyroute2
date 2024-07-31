from socket import AF_UNIX

from pr2test.marks import require_root

from pyroute2 import DiagSocket

pytestmark = [require_root()]


def test_basic():
    sstats_set = set()
    pstats_set = set()
    sstats = None
    fd = None

    with DiagSocket() as ds:
        ds.bind()
        sstats = ds.get_sock_stats(family=AF_UNIX)
        for s in sstats:
            sstats_set.add(s['udiag_ino'])

    with open('/proc/net/unix') as fd:
        for line in fd.readlines():
            line = line.split()
            try:
                pstats_set.add(int(line[6]))
            except ValueError:
                pass

    assert sstats_set == pstats_set

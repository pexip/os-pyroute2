import pytest
from pr2test.context_manager import make_test_matrix
from pr2test.marks import require_root
from pr2test.tools import fdb_record_exists

pytestmark = [require_root()]

test_matrix = make_test_matrix(
    targets=['local', 'netns'],
    tables=[None],
    dbs=['sqlite3/:memory:', 'postgres/pr2test'],
)


@pytest.mark.parametrize('context', test_matrix, indirect=True)
def test_fdb_create(context):

    spec = {
        'ifindex': context.default_interface.index,
        'lladdr': '00:11:22:33:44:55',
    }

    context.ndb.fdb.create(**spec).commit()
    assert fdb_record_exists(context.netns, **spec)

    context.ndb.fdb[spec].remove().commit()
    assert not fdb_record_exists(context.netns, **spec)

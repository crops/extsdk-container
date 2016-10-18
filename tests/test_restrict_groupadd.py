import os
import pytest
import shlex
import subprocess

gids = [0]

@pytest.mark.parametrize("gid", gids)
def test_fail_gid(gid):
    cmd = shlex.split("./restrict_groupadd.sh {} somegroup".format(gid))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    assert result.returncode != 0
    assert "Refusing to use a gid of 0" in result.stdout.decode()


def test_expected_args():
    # Add the fake groupadd to path
    os.environ['PATH'] = "./tests:" + os.environ['PATH']

    cmd = shlex.split("./restrict_groupadd.sh 1 testgroup")
    result = subprocess.run(cmd, check=False)

    assert result.returncode == 0

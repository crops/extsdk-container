import os
import pytest
import shlex
import subprocess


def test_fail_gid():
    cmd = shlex.split("./restrict_useradd.sh 101 0 somegroup")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    assert result.returncode != 0
    assert "Refusing to use a gid of 0" in result.stdout.decode()


# Changed restriction to only disallow root (0) due to
# various win/mac hypervisor issues
def test_fail_uid():
    cmd = shlex.split("./restrict_useradd.sh {} 0 somegroup".format(0))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    assert result.returncode != 0
    assert "Refusing to use a uid of 0" in result.stdout.decode()


useskelarg = [ True, False ]
@pytest.mark.parametrize("useskelarg", useskelarg)
@pytest.fixture
def setup_env_and_cmd():
    cmd = "./restrict_useradd.sh 101 1 testname"
    oldenv = os.environ.copy()

    # Add the fake useradd to path
    os.environ['PATH'] = "./tests:" + os.environ['PATH']

    if useskelarg:
        # Set the flag to useradd that says to check for the skel arg
        os.environ['SKELARG_USED'] = "1"
        cmd = cmd + " /myskel"

    yield shlex.split(cmd)
    os.environ = oldenv


def test_expected_args(setup_env_and_cmd):
    cmd = setup_env_and_cmd

    result = subprocess.run(cmd, check=False)

    assert result.returncode == 0

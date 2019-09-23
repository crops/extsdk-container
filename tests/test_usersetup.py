import os
import pytest
import shlex
import subprocess

def test_expected_args():
    # Add the fake sudo to path
    os.environ['PATH'] = "./tests:" + os.environ['PATH']

    cmd = shlex.split('./usersetup.py --uid 15 --gid 15 --username testuser somecmd firstarg "this is arg2" "this is arg3" "arg4" "this is last arg"')
    result = subprocess.run(cmd, check=False)

    assert result.returncode == 0

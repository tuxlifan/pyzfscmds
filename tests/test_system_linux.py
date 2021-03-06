import os

import pytest

import pyzfscmds.check
import pyzfscmds.system.linux as zfslinux
import pyzfscmds.system.agnostic

module_env = os.path.basename(__file__).upper().rsplit('.', 1)[0]
if module_env in os.environ:
    pytestmark = pytest.mark.skipif(
        "false" in os.environ[module_env],
        reason=f"Environment variable {module_env} specified test should be skipped.")

require_root_dataset = pytest.mark.require_root_dataset
require_zpool_root_mountpoint = pytest.mark.require_zpool_root_mountpoint
require_linux = pytest.mark.require_linux

"""zfs linux tests"""


@require_linux
@require_root_dataset
@require_zpool_root_mountpoint
def test_linux_mount(root_dataset, zpool_root_mountpoint):
    assert root_dataset == zfslinux.mountpoint_dataset(zpool_root_mountpoint)


@require_linux
def test_linux_mount_failure():
    assert zfslinux.mountpoint_dataset("/garbage/mountpoint") is None


@require_linux
def test_system_startup_check():
    assert pyzfscmds.system.agnostic.check_valid_system() == "linux"


@require_linux
@require_root_dataset
@require_zpool_root_mountpoint
def test_mount(root_dataset, zpool_root_mountpoint):
    assert zpool_root_mountpoint == pyzfscmds.system.linux.dataset_mountpoint(root_dataset)

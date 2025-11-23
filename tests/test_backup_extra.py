import os
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.modules import backup

def test_backup_mkdir_fail(fs):
    """Test backup fails when creating backup directory fails."""
    # We can simulate failure by patching mkdir or permissions.
    # pypurge uses Path.mkdir(parents=True, exist_ok=True)

    with patch("pathlib.Path.mkdir", side_effect=OSError("Boom")):
        # Should raise OSError and not be caught inside backup_targets_atomic because mkdir is outside the try block?
        # Check code:
        # backup_root.mkdir(...) -> Not in try block.
        # So it raises exception.

        with pytest.raises(OSError):
            backup.backup_targets_atomic([], Path("/backup"), Path("/src"))

def test_backup_mkstemp_fail(fs):
    """Test backup fails when mkstemp fails."""
    fs.create_dir("/backup")
    fs.create_dir("/src")

    with patch("tempfile.mkstemp", side_effect=OSError("Boom")):
        # Also outside try block?
        # Yes.
        with pytest.raises(OSError):
             backup.backup_targets_atomic([], Path("/backup"), Path("/src"))

def test_backup_zipfile_creation_fail(fs):
    """Test backup fails when ZipFile creation fails."""
    fs.create_dir("/backup")
    fs.create_dir("/src")

    with patch("zipfile.ZipFile", side_effect=Exception("Zip Fail")):
        # This IS inside try block.
        assert backup.backup_targets_atomic([], Path("/backup"), Path("/src")) is None

def test_backup_file_write_fail(fs):
    """Test individual file write failure (should warn but continue?)."""
    # Code: try: zf.write(...) except: logger.warning...

    fs.create_dir("/backup")
    fs.create_dir("/src")
    f = Path("/src/file")
    fs.create_file(f)

    # We patch zf.write. But zf is context manager yielded by ZipFile.

    mock_zf = MagicMock()
    mock_zf.write.side_effect = Exception("Write fail")

    with patch("zipfile.ZipFile", return_value=mock_zf):
        mock_zf.__enter__.return_value = mock_zf
        mock_zf.__exit__.return_value = None

        # backup_targets_atomic should succeed (return path, sha) despite one file failure
        res = backup.backup_targets_atomic([f], Path("/backup"), Path("/src"))
        assert res is not None

def test_backup_symlink_read_fail(fs):
    """Test failure reading symlink target."""
    fs.create_dir("/backup")
    fs.create_dir("/src")
    link = Path("/src/link")
    fs.create_symlink(link, "/target")

    # os.readlink(p) fails
    with patch("os.readlink", side_effect=Exception("Boom")):
         # symlink_manifest append target=None
         res = backup.backup_targets_atomic([link], Path("/backup"), Path("/src"))
         assert res is not None
         # We can verify manifest content if we could inspect the zip.
         # But we mocked ZipFile maybe? No, let's use real ZipFile logic if possible or check arguments to writestr.

def test_backup_relative_to_fail_file(fs):
    """Test p.relative_to failure for file."""
    fs.create_dir("/backup")
    fs.create_dir("/src")
    f = Path("/other/file") # Not relative to /src
    fs.create_file(f)

    # Code: try: rel = p.relative_to(root) except: rel = Path(p.name)

    res = backup.backup_targets_atomic([f], Path("/backup"), Path("/src"))
    assert res is not None
    # Check if backup contains "file" at root
    # We can use zipfile to inspect the created file.
    path, sha = res
    with zipfile.ZipFile(path) as zf:
        assert "file" in zf.namelist()

def test_backup_dir_recursion(fs):
    """Test backing up directory recursively."""
    fs.create_dir("/backup")
    fs.create_dir("/src/sub")
    f = Path("/src/sub/file")
    fs.create_file(f)

    res = backup.backup_targets_atomic([Path("/src/sub")], Path("/backup"), Path("/src"))
    assert res is not None
    path, sha = res
    with zipfile.ZipFile(path) as zf:
        assert "sub/file" in zf.namelist()

def test_backup_dir_recursion_write_fail(fs):
    """Test failure writing file inside directory recursion."""
    fs.create_dir("/backup")
    fs.create_dir("/src/sub")
    f = Path("/src/sub/file")
    fs.create_file(f)

    with patch("zipfile.ZipFile") as MockZip:
         mock_zf = MockZip.return_value.__enter__.return_value
         # First write (dir itself?) No, it iterates rglob("*").
         # Only sub.is_file() are written.
         mock_zf.write.side_effect = Exception("Boom")

         res = backup.backup_targets_atomic([Path("/src/sub")], Path("/backup"), Path("/src"))
         assert res is not None

def test_backup_cleanup_fail(fs):
    """Test failure during cleanup after main exception."""
    fs.create_dir("/backup")
    fs.create_dir("/src")

    with patch("zipfile.ZipFile", side_effect=Exception("Main Fail")):
        # And mock unlink to fail
        with patch.object(Path, "unlink", side_effect=Exception("Unlink Fail")):
             assert backup.backup_targets_atomic([], Path("/backup"), Path("/src")) is None

def test_backup_symlink_manifest_write(fs):
    """Test creation of symlink manifest."""
    fs.create_dir("/backup")
    fs.create_dir("/src")
    link = Path("/src/link")
    fs.create_symlink(link, "target")

    res = backup.backup_targets_atomic([link], Path("/backup"), Path("/src"))
    assert res is not None
    path, sha = res
    with zipfile.ZipFile(path) as zf:
        assert "cleanpy_symlink_manifest.json" in zf.namelist()

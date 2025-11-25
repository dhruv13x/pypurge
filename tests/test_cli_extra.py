# tests/test_cli_extra.py

import json
import logging
import os
import signal
import sys
import stat
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.cli import main, EXIT_OK, EXIT_CANCELLED, EXIT_PARTIAL_FAILURE, EXIT_DANGEROUS_ROOT, EXIT_LOCK_ERROR, EXIT_UNKNOWN_ERROR

# Common path deep enough to avoid dangerous root check
TEST_ROOT = "/test/project/deep/enough"

@pytest.fixture
def deep_fs(fs):
    fs.create_dir(TEST_ROOT)
    return fs

def test_main_force_flag(deep_fs):
    """Test main with --force flag."""
    fs = deep_fs
    file_path = f"{TEST_ROOT}/file.tmp"
    fs.create_file(file_path)

    with patch("pypurge.cli.force_unlink") as mock_force_unlink:
        with patch("pypurge.cli.scan_for_targets") as mock_scan:
             mock_scan.return_value = {"group": [Path(file_path)]}
             argv = [TEST_ROOT, "--force", "--yes", "--allow-root"]
             assert main(argv) == EXIT_OK
             mock_force_unlink.assert_called_with(Path(file_path))

def test_main_dry_run_preview(deep_fs):
    """Test main with --preview flag (dry-run)."""
    fs = deep_fs
    file_path = f"{TEST_ROOT}/file.tmp"
    fs.create_file(file_path)

    with patch("pypurge.cli.scan_for_targets") as mock_scan:
        mock_scan.return_value = {"group": [Path(file_path)]}
        argv = [TEST_ROOT, "--preview", "--allow-root"]
        assert main(argv) == EXIT_OK

def test_main_interactive_prompt_no(deep_fs):
    """Test interactive prompt rejection."""
    fs = deep_fs
    file_path = f"{TEST_ROOT}/file.tmp"
    fs.create_file(file_path)

    with patch("pypurge.cli.scan_for_targets") as mock_scan:
        mock_scan.return_value = {"group": [Path(file_path)]}
        with patch("builtins.input", return_value="n"):
             argv = [TEST_ROOT, "--allow-root"]
             assert main(argv) == EXIT_CANCELLED

def test_main_interactive_prompt_eof(deep_fs):
    """Test interactive prompt EOF."""
    fs = deep_fs
    file_path = f"{TEST_ROOT}/file.tmp"
    fs.create_file(file_path)

    with patch("pypurge.cli.scan_for_targets") as mock_scan:
        mock_scan.return_value = {"group": [Path(file_path)]}
        with patch("builtins.input", side_effect=EOFError):
             argv = [TEST_ROOT, "--allow-root"]
             assert main(argv) == EXIT_CANCELLED

def test_main_invalid_config_file(deep_fs):
    """Test main with invalid config file path or content."""
    fs = deep_fs
    config_path = Path(f"{TEST_ROOT}/config.json")
    fs.create_file(config_path, contents="invalid json")

    argv = [TEST_ROOT, "--config", str(config_path), "--preview", "--allow-root"]
    assert main(argv) == EXIT_OK

def test_main_scan_failure_handling(deep_fs):
    """Test main when scan returns items but deletion fails."""
    # Mock Path object returned by scan_for_targets

    mock_path = MagicMock() # Use MagicMock which should have all attributes
    mock_path.relative_to.return_value = Path("file.tmp")
    mock_path.is_symlink.return_value = False
    mock_path.is_file.return_value = True
    mock_path.is_dir.return_value = False
    mock_path.unlink.side_effect = Exception("Delete failed")

    with patch("pypurge.cli.scan_for_targets") as mock_scan:
        mock_scan.return_value = {"group": [mock_path]}

        argv = [TEST_ROOT, "--yes", "--allow-root"]
        assert main(argv) == EXIT_PARTIAL_FAILURE

def test_main_backup_failure_handling(deep_fs):
    """Test main when backup fails."""
    fs = deep_fs
    file_path = f"{TEST_ROOT}/file.tmp"
    p = Path(file_path)
    fs.create_file(p)

    with patch("pypurge.cli.scan_for_targets") as mock_scan:
        mock_scan.return_value = {"group": [p]}

        with patch("pypurge.cli.backup_targets_atomic", return_value=None):
             argv = [TEST_ROOT, "--yes", "--backup", "--allow-root"]
             assert main(argv) == EXIT_UNKNOWN_ERROR

def test_main_permission_failures_root_check(monkeypatch):
    """Test main failing when running as root without --allow-root."""
    monkeypatch.setattr(os, "geteuid", lambda: 0)
    argv = [TEST_ROOT]
    assert main(argv) == EXIT_DANGEROUS_ROOT

def test_main_dangerous_root_check(fs):
    """Test main failing when target is dangerous root."""
    argv = ["/"]
    assert main(argv) == EXIT_DANGEROUS_ROOT

def test_main_lock_failure(deep_fs):
    """Test main when lock acquisition fails."""
    fs = deep_fs
    with patch("pypurge.cli.acquire_lock", return_value=None):
        argv = [TEST_ROOT, "--allow-root"]
        assert main(argv) == EXIT_LOCK_ERROR

def test_main_signal_handling(deep_fs):
    """Test signal handling setup."""
    fs = deep_fs
    with patch("signal.signal") as mock_signal:
        argv = [TEST_ROOT, "--preview", "--allow-root"]
        main(argv)
        assert mock_signal.called

def test_main_version(capsys):
    """Test version flag."""
    argv = ["--version"]
    assert main(argv) == EXIT_OK
    captured = capsys.readouterr()
    assert captured.out.strip()

def test_main_pretty_print_check(monkeypatch):
    """Test pretty printing logic branches."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    argv = [TEST_ROOT, "--no-color", "--preview"]
    with patch("pypurge.cli.scan_for_targets", return_value={}):
         main(argv)

    argv = [TEST_ROOT, "--interactive", "--preview"]
    with patch("pypurge.cli.scan_for_targets", return_value={}):
         main(argv)

def test_main_config_loading_exception(deep_fs):
    """Test config loading generic exception."""
    fs = deep_fs
    cfg = Path(f"{TEST_ROOT}/.pypurge.json")
    fs.create_file(cfg)

    with patch("builtins.open", side_effect=Exception("Read fail")):
        argv = [TEST_ROOT, "--preview", "--allow-root"]
        assert main(argv) == EXIT_OK

def test_main_large_threshold_warning(deep_fs):
    """Test warning when size exceeds threshold."""
    fs = deep_fs
    p = Path(f"{TEST_ROOT}/large.file")
    fs.create_file(p)

    with patch("pypurge.cli.scan_for_targets", return_value={"g": [p]}):
        with patch("pypurge.cli.get_size", return_value=200 * 1024 * 1024): # 200MB
             # Use --yes so we proceed past the warning check
             argv = [TEST_ROOT, "--yes", "--allow-root"]
             with patch("pypurge.cli.logger.warning") as mock_log:
                 main(argv)
                 assert any("Large amount of data" in str(c) for c in mock_log.call_args_list)

def test_main_delete_symlinks(deep_fs):
    """Test main with --delete-symlinks."""
    fs = deep_fs
    p = Path(f"{TEST_ROOT}/link")
    fs.create_symlink(p, "/tmp/target")

    with patch("pypurge.cli.scan_for_targets", return_value={"g": [p]}):
        argv = [TEST_ROOT, "--yes", "--delete-symlinks"]
        main(argv)
        assert not p.exists()

def test_main_delete_dir(deep_fs):
    """Test main deleting directory."""
    fs = deep_fs
    d = Path(f"{TEST_ROOT}/subdir")
    fs.create_dir(d)

    with patch("pypurge.cli.scan_for_targets", return_value={"g": [d]}):
        argv = [TEST_ROOT, "--yes", "--allow-root"]
        main(argv)
        assert not d.exists()

def test_main_delete_dir_fail_notfound(deep_fs):
    """Test main deleting directory that disappears (FileNotFoundError)."""
    fs = deep_fs
    d = Path(f"{TEST_ROOT}/subdir")
    fs.create_dir(d)

    with patch("pypurge.cli.scan_for_targets", return_value={"g": [d]}):
        with patch("shutil.rmtree", side_effect=FileNotFoundError):
             argv = [TEST_ROOT, "--yes", "--allow-root"]
             assert main(argv) == EXIT_OK

def test_main_exclude_regex_error(deep_fs):
    """Test main with invalid regex exclude."""
    fs = deep_fs
    argv = [TEST_ROOT, "--exclude", "re:("]
    main(argv)

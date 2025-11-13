import shutil
import unittest
import unittest.mock
from pathlib import Path

from pypurge.cli import main


class TestCli(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_cli_dir")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_main_with_preview(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--preview", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_version(self):
        argv = ["--version"]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_yes(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_clean_venv(self):
        (self.test_dir / ".venv").mkdir()
        argv = ["--yes", "--clean-venv", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_exclude(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--exclude", "*.pyc", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue((self.test_dir / "file.pyc").exists())

    def test_main_with_older_than(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--older-than", "1", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue((self.test_dir / "file.pyc").exists())

    def test_main_with_force(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--force", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_backup(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--backup", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_no_color(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--no-color", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_delete_symlinks(self):
        (self.test_dir / "file.pyc").touch()
        (self.test_dir / "link").symlink_to(self.test_dir / "file.pyc")
        argv = ["--yes", "--delete-symlinks", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_allow_broad_root(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", "--allow-broad-root", "/"]
        exit_code = main(argv)
        self.assertEqual(exit_code, 5)

    def test_main_with_allow_root(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", "--allow-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_interactive_prompt_no(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = [str(self.test_dir)]
        with unittest.mock.patch("builtins.input", return_value="n"):
            exit_code = main(argv)
        self.assertEqual(exit_code, 2)

    def test_main_with_config_file(self):
        import json

        config = {"exclude_patterns": ["*.pyc"]}
        (self.test_dir / ".pypurge.json").write_text(json.dumps(config))
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue((self.test_dir / "file.pyc").exists())

    def test_main_with_log_file(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--log-file", "test.log", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue(Path("test.log").exists())
        Path("test.log").unlink()


if __name__ == "__main__":
    unittest.main()

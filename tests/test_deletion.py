import unittest
from pathlib import Path
from src.pypurge.modules.deletion import force_rmtree, force_unlink


class TestDeletion(unittest.TestCase):
    def test_force_unlink(self):
        with open("test_file.txt", "w") as f:
            f.write("hello")
        force_unlink(Path("test_file.txt"))
        self.assertFalse(Path("test_file.txt").exists())

    def test_force_rmtree(self):
        Path("test_dir").mkdir()
        with open("test_dir/test_file.txt", "w") as f:
            f.write("hello")
        force_rmtree(Path("test_dir"))
        self.assertFalse(Path("test_dir").exists())


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path
from src.pypurge.modules.safety import is_dangerous_root


class TestSafety(unittest.TestCase):
    def test_is_dangerous_root(self):
        self.assertTrue(is_dangerous_root(Path("/")))
        self.assertTrue(is_dangerous_root(Path.home()))
        self.assertFalse(is_dangerous_root(Path("./safe_dir")))


if __name__ == "__main__":
    unittest.main()

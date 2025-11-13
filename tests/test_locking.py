import unittest
from pathlib import Path
from pypurge.modules.locking import acquire_lock, release_lock


class TestLocking(unittest.TestCase):
    def test_acquire_and_release_lock(self):
        lock_path = Path("test.lock")
        lock_fd = acquire_lock(lock_path)
        self.assertIsNotNone(lock_fd)
        release_lock(lock_fd, lock_path)
        self.assertFalse(lock_path.exists())


if __name__ == "__main__":
    unittest.main()

import shutil
import unittest
from pathlib import Path

from pypurge.modules.locking import acquire_lock, release_lock


class TestLocking(unittest.TestCase):
    def setUp(self):
        self.lock_path = Path("test.lock")
        if self.lock_path.is_dir():
            shutil.rmtree(self.lock_path)
        elif self.lock_path.exists():
            self.lock_path.unlink()

    def tearDown(self):
        if self.lock_path.is_dir():
            shutil.rmtree(self.lock_path)
        elif self.lock_path.exists():
            self.lock_path.unlink()

    def test_acquire_and_release_lock(self):
        lock_fd = acquire_lock(self.lock_path)
        self.assertIsNotNone(lock_fd)
        release_lock(lock_fd, self.lock_path)
        self.assertFalse(self.lock_path.exists())

    def test_lock_contention(self):
        lock_fd1 = acquire_lock(self.lock_path)
        self.assertIsNotNone(lock_fd1)
        lock_fd2 = acquire_lock(self.lock_path)
        self.assertIsNone(lock_fd2)
        release_lock(lock_fd1, self.lock_path)

    def test_stale_lock(self):
        lock_fd1 = acquire_lock(self.lock_path, stale_seconds=-1)
        self.assertIsNotNone(lock_fd1)
        release_lock(lock_fd1, self.lock_path)
        lock_fd2 = acquire_lock(self.lock_path, stale_seconds=-1)
        self.assertIsNotNone(lock_fd2)
        release_lock(lock_fd2, self.lock_path)

    def test_lock_file_is_dir(self):
        self.lock_path.mkdir()
        lock_fd = acquire_lock(self.lock_path)
        self.assertIsNone(lock_fd)


if __name__ == "__main__":
    unittest.main()

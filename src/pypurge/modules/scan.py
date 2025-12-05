# src/pypurge/modules/scan.py

import fnmatch
import os
import re
from collections import defaultdict
from pathlib import Path
import pathspec

from .utils import is_old_enough


def load_gitignore(root_path: Path):
    """
    Loads .gitignore patterns from the root path and returns a pathspec spec.
    """
    gitignore_path = root_path / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r") as f:
                return pathspec.PathSpec.from_lines("gitwildmatch", f)
        except Exception:
            pass
    return None


def scan_for_targets(
    root_path: Path,
    dir_groups: dict,
    file_groups: dict,
    exclude_dirs: set,
    exclude_patterns: list,
    older_than_sec: int,
    age_type: str,
    delete_symlinks: bool,
    use_gitignore: bool = True,
) -> dict:
    targets = defaultdict(list)

    spec = None
    if use_gitignore:
        spec = load_gitignore(root_path)

    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        try:
            rel_root = Path(root).relative_to(root_path)
        except Exception:
            rel_root = Path(".")

        # Directories
        for d in list(dirs):
            d_path = Path(root) / d
            rel_path = rel_root / d
            rel_str = str(rel_path)

            # 1. Check exclude patterns (Priority 1: Explicit Safety)
            if any(
                (pt == "re" and pat.search(rel_str))
                or (pt == "glob" and fnmatch.fnmatch(rel_str, pat))
                for pt, pat in exclude_patterns
            ):
                dirs.remove(d)
                continue

            # 2. Check if it matches explicit directory targets (Priority 2: Explicit Targets)
            matched = False
            for g, pats in dir_groups.items():
                for pat in pats:
                    try:
                        if fnmatch.fnmatch(d, pat) or fnmatch.fnmatch(rel_str, pat):
                            # It is a target! Check age.
                            if older_than_sec and not is_old_enough(d_path, older_than_sec, age_type):
                                matched = True
                                break

                            targets[g].append(d_path)
                            matched = True
                            break
                    except Exception:
                        continue
                if matched:
                    break

            if matched:
                # If it is a target, we process it and remove from recursion (since we delete it)
                if d in dirs:
                    dirs.remove(d)
                continue

            # 3. Check gitignore (Priority 3: Implicit Safety)
            # pathspec handles trailing slashes in patterns by matching against path + '/' if it is a dir
            # But here we pass rel_str. We should check if pathspec needs 'dir/'
            # Generally spec.match_file(name) works.
            # But let's try to match 'rel_str/' as well if it fails?
            # Actually pathspec implementation matches 'foo' against 'foo/' pattern if we treat it right.
            # But let's just use match_file(rel_str) first.
            if spec:
                 if spec.match_file(rel_str):
                     dirs.remove(d)
                     continue
                 # Also try adding trailing slash which signals directory to pathspec
                 if spec.match_file(rel_str + "/"):
                     dirs.remove(d)
                     continue

            if d_path.is_symlink() and not delete_symlinks:
                 pass

        # Files
        for f in files:
            f_path = Path(root) / f
            rel_path = rel_root / f
            rel_str = str(rel_path)

            # 1. Check exclude patterns (Priority 1: Explicit Safety)
            if any(
                (pt == "re" and pat.search(rel_str))
                or (pt == "glob" and fnmatch.fnmatch(rel_str, pat))
                for pt, pat in exclude_patterns
            ):
                continue

            # 2. Check if matches explicit file targets (Priority 2: Explicit Targets)
            matched = False
            for g, pats in file_groups.items():
                for pat in pats:
                    try:
                        if fnmatch.fnmatch(f, pat) or fnmatch.fnmatch(rel_str, pat):
                            if older_than_sec and not is_old_enough(f_path, older_than_sec, age_type):
                                matched = True
                                break

                            targets[g].append(f_path)
                            matched = True
                            break
                    except Exception:
                        continue
                if matched:
                    break

            if matched:
                continue

            # 3. Check gitignore (Priority 3: Implicit Safety)
            if spec and spec.match_file(rel_str):
                continue

            if f_path.is_symlink() and not delete_symlinks:
                continue

    return targets

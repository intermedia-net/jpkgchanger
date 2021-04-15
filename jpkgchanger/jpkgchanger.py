"""Change java project package name!"""

import argparse
import logging
import os
from typing import List

PROTECTED_FILES: List[str] = []
PROTECTED_DIRS: List[str] = []


def parse_args():
    """Parse cli arguments."""
    parser = argparse.ArgumentParser(description="Java project package name changer.")
    parser.add_argument("--directory", default=".", type=str, help="Working directory.")
    parser.add_argument(
        "--current",
        required=True,
        type=str,
        help='Current package name. For example: "com.example".',
    )
    parser.add_argument(
        "--target",
        required=True,
        type=str,
        help='Target package name. For example: "org.another".',
    )
    parser.add_argument(
        "--protected_dirs",
        default=[],
        type=str,
        nargs="+",
        help="List of protected from any changes directories",
    )
    parser.add_argument(
        "--protected_files",
        default=[],
        type=str,
        nargs="+",
        help="List of protected from any changes files",
    )
    return parser.parse_args()


def build_path(package_name: str) -> str:
    """Build path from java package name."""
    return package_name.replace(".", "/")


def build_variants(package_name: str) -> List[str]:
    """Build package name variants, which can be appeared in java project files."""
    return [package_name, package_name.replace(".", "_"), build_path(package_name)]


def file_replace(filename: str, origin: str, target: str):
    """Replace all occurrences of origin in the file to target."""
    with open(filename, encoding="utf8", errors="ignore") as file:
        if not any(origin in line for line in file):
            return
    with open(filename, encoding="utf8", errors="ignore") as file:
        out_fname = filename + ".tmp"
        with open(out_fname, "w", encoding="utf8", errors="ignore") as out:
            for line in file:
                out.write(line.replace(origin, target))
            out.close()
        os.rename(out_fname, filename)


def is_protected_dir(dir_path: str) -> bool:
    """Check if the directory is protected from changes."""
    is_dir_path_protected = False
    for protected_dir in PROTECTED_DIRS:
        dir_abspath = os.path.abspath(dir_path)
        protected_dir_abspath = os.path.abspath(protected_dir)
        if dir_abspath.startswith(protected_dir_abspath):
            is_dir_path_protected = True
    return is_dir_path_protected


def is_protected_file(filename: str) -> bool:
    """Check if the file is protected from changes."""
    return filename in PROTECTED_FILES


def rename_file(current_path: str, target_path: str, dir_path: str, filename: str):
    """Rename file to new package path."""
    fullname = os.path.join(dir_path, filename)
    target_dir = dir_path.replace(current_path, target_path)
    target_name = os.path.join(target_dir, filename)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    logging.debug("Rename `%s` to `%s`", fullname, target_name)
    os.rename(fullname, target_name)


def change_package_name_in_file(
    current_variants: List[str],
    target_variants: List[str],
    dir_path: str,
    filename: str,
):
    """Change package name in file."""
    fullname = os.path.join(dir_path, filename)
    for i, _ in enumerate(current_variants):
        file_replace(fullname, current_variants[i], target_variants[i])


def fill_protected(
    working_dir: str, protected_dirs: List[str], protected_files: List[str]
):
    """Fill protected directories and files based on working dir"""
    for protected_dir in protected_dirs:
        PROTECTED_DIRS.append(os.path.join(working_dir, protected_dir))
    for protected_file in protected_files:
        PROTECTED_FILES.append(os.path.join(working_dir, protected_file))


def change_package_name(
    working_dir: str,
    current: str,
    target: str,
    protected_dirs: List[str],
    protected_files: List[str],
):
    """Entry point of changing package name."""
    fill_protected(working_dir, protected_dirs, protected_files)
    logging.info("Current working directory: `%s`", working_dir)
    logging.info("Current package: `%s`, target package `%s`", current, target)
    logging.info("Current protected directories: %s", repr(PROTECTED_DIRS))
    logging.info("Current protected files: %s", repr(PROTECTED_FILES))
    current_variants = build_variants(current)
    target_variants = build_variants(target)
    current_path = build_path(current)
    target_path = build_path(target)
    for dir_path, _, filenames in os.walk(working_dir):
        is_dir_path_protected = is_protected_dir(dir_path)
        if not is_dir_path_protected:
            for filename in filenames:
                fullname = os.path.join(dir_path, filename)
                if not is_protected_file(fullname):
                    change_package_name_in_file(
                        current_variants, target_variants, dir_path, filename
                    )
                    if current_path in dir_path:
                        rename_file(current_path, target_path, dir_path, filename)


def main():
    """Entry point of CLI script."""
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG)
    directory: str = os.path.expanduser(os.path.expandvars(args.directory))
    working_dir: str = os.path.normpath(os.path.abspath(directory))
    change_package_name(
        working_dir,
        args.current,
        args.target,
        args.protected_dirs,
        args.protected_files,
    )

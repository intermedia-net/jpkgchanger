import glob
import os
import shutil
import filecmp
import difflib

from py._path.local import LocalPath


def prepare_working_files(test_name: str, tmpdir: LocalPath):
    all_files = set(glob.glob(f"./tests/{test_name}/*.java"))
    expected_files = set(glob.glob(f"./tests/{test_name}/*Expected.java"))
    tests_files = all_files - expected_files
    work_dir = tmpdir.mkdir(test_name)

    working_files = []
    for test_file in tests_files:
        dst = os.path.join(work_dir, os.path.basename(test_file))
        working_files.append(dst)
        shutil.copyfile(test_file, dst)
    return work_dir, working_files


def assert_expected_result(test_name: str, working_files):
    for working_file in working_files:
        expected_file = os.path.join(
            f"./tests/{test_name}/",
            os.path.basename(os.path.splitext(working_file)[0]) + "Expected.java"
        )

        exception_message = ""
        with open(expected_file, "r") as expected_f:
            exception_message += "Expected file " + expected_file + "\n"
            expected_lines = expected_f.readlines()
            exception_message += "\n".join(expected_lines)
            exception_message += "\n"
            with open(working_file, "r") as working_f:
                exception_message += "Working file " + working_file + "\n"
                working_lines = working_f.readlines()
                exception_message += "\n".join(working_lines)
                exception_message += "\n"
                diff = difflib.unified_diff(
                    expected_lines,
                    working_lines,
                    fromfile=expected_file,
                    tofile=working_file
                )
                exception_message += "Diff:\n"
                for line in diff:
                    exception_message += line + "\n"
        assert filecmp.cmp(expected_file, working_file), exception_message
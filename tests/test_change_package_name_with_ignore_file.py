from jpkgchanger import change_package_name
from py._path.local import LocalPath
from tests.utils.utils import prepare_working_files
from tests.utils.utils import assert_expected_result


def test_change_package_name_with_ignore_file(tmpdir: LocalPath):
    work_dir, working_files = prepare_working_files("test_change_package_name_with_ignore_file", tmpdir)

    change_package_name(work_dir, "com.example", "com.another", [], ["ComExampleToComAnother1.java"])

    assert_expected_result("test_change_package_name_with_ignore_file", working_files)

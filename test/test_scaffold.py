from unittest.mock import Mock

import black

from create_py_app.command import Scaffolder, ScaffoldOptions, KindOfThing


def format_using_black(s):
    return black.format_str(s, mode=black.FileMode())


class PathMock(Mock):
    def __init__(
        self,
        spec=None,
        side_effect=None,
        return_value=...,
        wraps=None,
        name=None,
        spec_set=None,
        parent=None,
        _spec_state=None,
        _new_name="",
        _new_parent=None,
        **kwargs,
    ) -> None:
        super().__init__(
            spec,
            side_effect,
            return_value,
            wraps,
            name,
            spec_set,
            parent,
            _spec_state,
            _new_name,
            _new_parent,
            **kwargs,
        )
        self.created_paths: dict[str, PathMock] = {}

    def __truediv__(self, other):
        next_path = PathMock()
        self.created_paths[other] = next_path
        return next_path

    def written_text(self):
        return self.write_text.call_args[0][0]


def test_creates_main_with_correct_filename():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=True,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    assert "foo.py" in path.created_paths


def test_writes_empty_main_when_nothing_else_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=True,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    main_file = path.created_paths["foo.py"]
    assert "def main() -> int:\n    return 0" in main_file.written_text()
    actual = main_file.written_text()
    expected = format_using_black(main_file.written_text())
    assert actual == expected


def test_writes_main_with_logging_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=True,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=True,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    main_file = path.created_paths["foo.py"]
    assert "logging.basicConfig" in main_file.written_text()
    assert main_file.written_text() == format_using_black(main_file.written_text())


def test_writes_main_with_settings_imported_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=True,
            fast_api=False,
            scheduled_job=False,
            parse_args=False,
            use_logging=False,
            env_settings=True,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    main_file = path.created_paths["foo.py"]
    assert "from src.project_settings import settings" in main_file.written_text()


def test_writes_main_with_argparse_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=True,
            fast_api=False,
            parse_args=True,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    main_file = path.created_paths["foo.py"]
    assert "parser = argparse.ArgumentParser()" in main_file.written_text()
    actual = main_file.written_text()
    assert actual == format_using_black(main_file.written_text())


def test_writes_fastapi_to_requirements_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=True,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    req_file = path.created_paths["requirements.in"]
    assert "fastapi" in req_file.written_text()


def test_writes_sqla_to_requirements_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=True,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    req_file = path.created_paths["requirements.in"]
    assert "SQLAlchemy" in req_file.written_text()


def test_writes_pyd_sett_to_requirements_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=True,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    req_file = path.created_paths["requirements.in"]
    assert "pydantic-settings" in req_file.written_text()


def test_writes_settings_file_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=True,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    settings_file = path.created_paths["src"].created_paths["project_settings.py"]
    assert "pydantic_settings" in settings_file.written_text()
    assert settings_file.written_text() == format_using_black(
        settings_file.written_text()
    )


def test_writes_vs_code_settings_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=True,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    settings_file = path.created_paths[".vscode"].created_paths["settings.json"]
    assert "python.testing.pytestArgs" in settings_file.written_text()


def test_writes_repo_patt_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=True,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    repo_file = path.created_paths["src"].created_paths["base_repo.py"]
    assert "class BaseRepository(Protocol)" in repo_file.written_text()
    assert repo_file.written_text() == format_using_black(repo_file.written_text())


def test_writes_example_repo_when_sqla_also_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=True,
            repo_pattern=True,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    repo_file = path.created_paths["src"].created_paths["example_repo.py"]
    assert "class SqlaPostRepository" in repo_file.written_text()
    assert repo_file.written_text() == format_using_black(repo_file.written_text())


def test_writes_scheduled_job_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=True,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    sjob_path = (
        path.created_paths["src"]
        .created_paths["entry_points"]
        .created_paths["scheduled_job"]
    )
    sjob_file = sjob_path.created_paths["scheduled_job.py"]
    assert "scheduler.start()" in sjob_file.written_text()
    assert sjob_file.written_text() == format_using_black(sjob_file.written_text())


def test_writes_apscheduler_when_scheduled_job_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=True,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    req_file = path.created_paths["requirements.in"]
    assert "apscheduler" in req_file.written_text()


def test_writes_scheduled_job_to_vscode_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=True,
            use_logging=False,
            env_settings=False,
            vs_code=True,
            sqla=False,
            repo_pattern=False,
            di_setup=False,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    launch_file = path.created_paths[".vscode"].created_paths["launch.json"]
    assert (
        '"program": "src/entry_points/scheduled_job/scheduled_job.py",'
        in launch_file.written_text()
    )


def test_writes_configure_services_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=False,
            repo_pattern=False,
            di_setup=True,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    cs_file = path.created_paths["src"].created_paths["configure_services.py"]
    assert "get_some_service" in cs_file.written_text()
    assert cs_file.written_text() == format_using_black(cs_file.written_text())


def test_writes_sqla_to_configure_services_when_selected():
    path = PathMock()
    dut = Scaffolder(
        "foo",
        path,
        ScaffoldOptions(
            kind=KindOfThing.PROGRAM,
            write_main_script=False,
            fast_api=False,
            parse_args=False,
            scheduled_job=False,
            use_logging=False,
            env_settings=False,
            vs_code=False,
            sqla=True,
            repo_pattern=False,
            di_setup=True,
            set_up_git=False,
            tkinter=False,
        ),
    )
    dut.write()
    cs_file = path.created_paths["src"].created_paths["configure_services.py"]
    assert "def get_sync_session_factory()" in cs_file.written_text()
    # assert cs_file.written_text() == format_using_black(cs_file.written_text())

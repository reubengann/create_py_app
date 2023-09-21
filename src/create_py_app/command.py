import argparse
import subprocess
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import jinja2

import create_py_app
from create_py_app.pick import pick

OPTIONS = [
    "Main script",
    "FastAPI entry point",
    "Command line arguments",
    "Scheduled job",
    "Logging",
    "ENV settings",
    "Set up VS Code",
    "Set up Sqlalchemy ORM",
    "Set up repository design pattern",
    "Set up a file for configuring dependency injection",
]


@dataclass
class ScaffoldOptions:
    write_main_script: bool
    fast_api: bool
    parse_args: bool
    scheduled_job: bool
    use_logging: bool
    env_settings: bool
    vs_code: bool
    sqla: bool
    repo_pattern: bool
    di_setup: bool


def parse_options(selected: list[str]) -> ScaffoldOptions:
    return ScaffoldOptions(*[o in selected for o in OPTIONS])


def get_template(template_name: str):
    return jinja2.Template((resources.files(create_py_app) / template_name).read_text())


class Scaffolder:
    def __init__(
        self, project_name: str, project_folder: Path, options: ScaffoldOptions
    ) -> None:
        self.project_name = project_name
        self.project_folder = project_folder
        self.options = options
        self.src_folder = self.project_folder / "src"
        self.test_folder = self.project_folder / "test"

    def write(self):
        print(f"Writing output to folder {self.project_folder.resolve()}")
        self.maybe_initialize_git()
        self.maybe_create_folders()
        self.create_requirements()
        self.create_coverage()
        self.set_up_testing()
        self.make_readme()
        if self.options.vs_code:
            self.write_vs_code_settings()
        if self.options.env_settings:
            self.set_up_env_settings()
        if self.options.write_main_script:
            self.write_main_script()
        if self.options.sqla:
            self.set_up_sqla()
        if self.options.repo_pattern:
            self.set_up_repo_pattern()
        if self.options.fast_api:
            self.add_fastapi_entry_point()
        if self.options.scheduled_job:
            self.add_scheduled_job_entry_point()
        if self.options.di_setup:
            self.add_configure_services()

    def add_configure_services(self):
        template = get_template("configure_services_template.txt")
        (self.src_folder / "configure_services.py").write_text(
            template.render(
                {
                    "blank_configure_services": not self.options.sqla
                    and not self.options.repo_pattern,
                    "sqla": self.options.sqla,
                    "env_settings": self.options.env_settings,
                }
            )
        )

    def add_scheduled_job_entry_point(self):
        entry_points_folder = self.maybe_make_entry_points_folder()
        sch_job_folder = entry_points_folder / "scheduled_job"
        if not sch_job_folder.exists():
            sch_job_folder.mkdir()
        template = get_template("scheduled_job_template.txt")
        (sch_job_folder / "scheduled_job.py").write_text(template.render())

    def maybe_make_entry_points_folder(self):
        entry_points_folder = self.src_folder / "entry_points"
        if not entry_points_folder.exists():
            entry_points_folder.mkdir()
        (entry_points_folder / "__init__.py").touch()
        return entry_points_folder

    def add_fastapi_entry_point(self):
        entry_points_folder = self.maybe_make_entry_points_folder()
        api_folder = entry_points_folder / "api"
        if not api_folder.exists():
            api_folder.mkdir()
        (api_folder / "__init__.py").touch()
        template = get_template("api_main_template.txt")
        (api_folder / "app.py").write_text(template.render())
        template = get_template("api_router_template.txt")
        (api_folder / "post_router.py").write_text(
            template.render(
                {"sqla": self.options.sqla, "di_setup": self.options.di_setup}
            )
        )

    def set_up_repo_pattern(self):
        template = get_template("repo_pattern_template.txt")
        (self.src_folder / "base_repo.py").write_text(template.render())
        if self.options.sqla:
            template = get_template("example_repo_template.txt")
            (self.src_folder / "example_repo.py").write_text(template.render())

    def set_up_sqla(self):
        template = get_template("tables_template.txt")
        (self.src_folder / "tables.py").write_text(template.render())

    def make_readme(self):
        template = get_template("readme_template.txt")
        (self.project_folder / "readme.md").write_text(
            template.render(
                {
                    "project_name": self.project_name,
                    "parse_args": self.options.parse_args,
                }
            )
        )

    def set_up_env_settings(self):
        src_folder = self.src_folder
        template = get_template("settings_template.txt")
        (src_folder / "project_settings.py").write_text(
            template.render({"sqla": self.options.sqla})
        )
        template = get_template("env_template.txt")
        (self.project_folder / ".env").write_text(
            template.render({"sqla": self.options.sqla})
        )
        (self.project_folder / ".env.template").write_text(
            template.render({"sqla": self.options.sqla})
        )

    def set_up_testing(self):
        test_folder = self.test_folder
        template = get_template("test_init_template.txt")
        (test_folder / "__init__.py").write_text(template.render())
        template = get_template("test_example_template.txt")
        (test_folder / "test_example.py").write_text(template.render())
        if self.options.fast_api:
            template = get_template("api_test_template.txt")
            (test_folder / "test_api.py").write_text(
                template.render({"di_setup": self.options.di_setup})
            )

    def create_coverage(self):
        template = get_template("coverage_rc_template.txt")
        (self.project_folder / ".coveragerc").write_text(
            template.render({"env_settings": self.options.env_settings})
        )

    def create_requirements(self):
        template = get_template("requirements_in_template.txt")
        (self.project_folder / "requirements.in").write_text(
            template.render(
                {
                    "env_settings": self.options.env_settings,
                    "sqla": self.options.sqla or self.options.repo_pattern,
                    "fast_api": self.options.fast_api,
                    "scheduled_job": self.options.scheduled_job,
                }
            )
        )
        template = get_template("requirements_in_dev_template.txt")
        (self.project_folder / "requirements-dev.in").write_text(template.render())

    def maybe_create_folders(self):
        if not self.src_folder.exists():
            self.src_folder.mkdir()
        if not self.test_folder.exists():
            self.test_folder.mkdir()

    def maybe_initialize_git(self):
        template = get_template("gitignore_template.txt")
        (self.project_folder / ".gitignore").write_text(
            template.render({"fast_api": self.options.fast_api})
        )
        if not (self.project_folder / ".git").exists():
            subprocess.run(["git", "init", self.project_folder], shell=True)

    def write_vs_code_settings(self):
        vs_code_folder = self.project_folder / ".vscode"
        if not vs_code_folder.exists():
            vs_code_folder.mkdir()
        template = get_template("vs_code_launch_json_template.txt")
        (vs_code_folder / "launch.json").write_text(
            template.render(
                {
                    "entrypoint": f"{self.project_name}.py",
                    "fast_api": self.options.fast_api,
                    "scheduled_job": self.options.scheduled_job,
                }
            )
        )
        template = get_template("vs_code_settings_template.txt")
        (vs_code_folder / "settings.json").write_text(template.render())

    def write_main_script(self):
        template = get_template("main_template.txt")
        context = {
            "use_logging": self.options.use_logging,
            "env_settings": self.options.env_settings,
            "parse_args": self.options.parse_args,
        }
        if not self.options.parse_args:
            context["empty_main"] = True
        (self.project_folder / f"{self.project_name}.py").write_text(
            template.render(context)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--overwrite", help="Overwrite", action="store_true")
    args = parser.parse_args()
    project_name: str = args.project_name
    dest_folder = Path(project_name)
    # TEMP
    allow_nonempty_folder = args.overwrite
    if (
        dest_folder.exists()
        and dest_folder.is_dir()
        and any(dest_folder.iterdir())
        and not allow_nonempty_folder
    ):
        print(f"Folder {dest_folder} is not empty. Refusing to do anything")
        return 1
    title = "Please choose your options (press SPACE to mark, ENTER to continue, ESC or q to quit): "
    selected = pick(OPTIONS, title)
    if selected is None:
        return 0
    # print(selected)
    if not dest_folder.exists():
        dest_folder.mkdir()
    selected_option_names = [o[0] for o in selected]
    options = parse_options(selected_option_names)
    scaffolder = Scaffolder(project_name, dest_folder, options)
    scaffolder.write()
    print("Project written. Now run\n")
    print("pip install -r requirements.in -r requirements-dev.in")
    return 0

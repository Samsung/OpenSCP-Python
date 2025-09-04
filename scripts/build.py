# Copyright 2025 Samsung Electronics Co, Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import argparse
import enum

from constants import Const
from utils import collect_artifacts, run_cmd, run_cmds


class Component(str, enum.Enum):
    LIB = "lib"
    DOC = "doc"


def main() -> None:
    options = parse_arguments()
    match options.component:
        case Component.LIB.value:
            build_lib()
        case Component.DOC.value:
            build_docs()
        case _:
            sys.exit(f"'{options.component}' component build is unsupported")


def parse_arguments() -> argparse.Namespace:
    components = [component.value for component in Component]
    parser = argparse.ArgumentParser("Build Python SCP library sources and generate documentation",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--component",
                        choices=components,
                        required=True,
                        help="Target component to build:\n"
                             f"  {Component.LIB.value}: Python SCP library\n"
                             f"  {Component.DOC.value}: Python SCP library documentation")
    options = parser.parse_args()
    return options


def build_lib() -> None:
    compose_source_distribution()
    artifacts_path = Const.Path.PROJECT_ROOT / "dist" / "*"
    collect_artifacts(artifacts_path, Const.Path.OUT_LIB_DIR)


def compose_source_distribution() -> None:
    setup_path = Const.Path.PROJECT_ROOT/ "setup.py"
    command = f"cd {Const.Path.PROJECT_ROOT} && {Const.Bin.LIB_PYTHON} {setup_path} sdist"
    run_cmd(command)


def build_docs() -> None:
    generate_html_docs()
    artifacts_path = Const.Path.PROJECT_ROOT/ "docs" / "_build" / "html" / "*"
    collect_artifacts(artifacts_path, Const.Path.OUT_DOCS_DIR)


def generate_html_docs() -> None:
    commands = [f"rm -rf {Const.Path.VENV_DIR}",
                f"{Const.Bin.LIB_PYTHON} -m venv {Const.Path.VENV_DIR}",
                f"{Const.Path.VENV_BIN_DIR}/pip3 install {Const.Path.PROJECT_ROOT}[docs]",
                f"{Const.Path.VENV_BIN_DIR}/sphinx-apidoc -f -o {Const.Path.PROJECT_ROOT}/docs {Const.Path.PROJECT_ROOT}/openscp",
                # Sphinx ignores classes with some decorators - https://github.com/dagster-io/dagster/issues/2427#issuecomment-832348566
                f"patch {Const.Path.PROJECT_ROOT}/docs/openscp.rst {Const.Path.PROJECT_ROOT}/scripts/smart_card_connection_docs.patch",
                f"SPHINXBUILD={Const.Path.VENV_BIN_DIR}/sphinx-build make -C {Const.Path.PROJECT_ROOT}/docs html"]
    run_cmds(commands)


if __name__ == "__main__":
    main()

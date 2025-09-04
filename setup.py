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

from setuptools import setup, find_packages

VERSION = "1.0.0"

setup(
    name="openscp",
    version=VERSION,
    description="GlobalPlatform's SCP03 and SCP11 protocols implementation for off-card entity",
    packages=find_packages(exclude=["*tests*"]),
    python_requries=">=3.7",
    install_requries=[
        "JPype1"
    ],
    extras_require={
        "test": [
            "JPype1",
            "pytest"
        ],
        "docs": [
            "JPype1",
            "sphinx",
            "m2r2"
        ]
    }
)

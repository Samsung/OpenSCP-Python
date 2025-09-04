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

import os
from typing import Any

import jpype.imports

# https://jpype.readthedocs.io/en/latest/install.html#known-bugs-limitations
# Because of lack of JVM support, you cannot shutdown the JVM and then restart it. Nor can you start more than one
# copy of the JVM.
is_jvm_started = False


def _start_jvm_if_needed() -> None:
    global is_jvm_started
    if is_jvm_started:
        return
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(current_dir)
    jpype.startJVM(classpath=[project_root + "/lib/*"])
    is_jvm_started = True


# java_bytes: byte[] (Java primitive)
def _java_bytes_to_python_bytes(java_bytes: Any) -> bytes:
    python_bytes_array = [_signed_to_unsigned_byte(java_bytes[i]) for i in range(java_bytes.length)]
    python_bytes_str = ["{:02X}".format(python_bytes_array[i]) for i in range(len(python_bytes_array))]
    return bytes.fromhex("".join(python_bytes_str))


# java_bytes: byte[] (Java primitive)
def _python_bytes_to_java_bytes(value: bytes) -> Any:  # -> java byte[]
    _start_jvm_if_needed()
    import java.io
    baos = java.io.ByteArrayOutputStream()
    baos.write(value, 0, len(value))
    return baos.toByteArray()


def _signed_to_unsigned_byte(b: int) -> int:
    return b & 0xFF

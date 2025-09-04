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

class Apdu:
    """Data holder class for ISO 7816 Command APDU representation"""

    cla: int
    ins: int
    p1: int
    p2: int
    data: bytes
    le: int
    force_add_le: bool

    def __init__(self, cla: int, ins: int, p1: int, p2: int, data: bytes, le: int = 0x00, force_add_le: bool = False):
        """
        :param cla: CAPDU class byte (CLA)
        :param ins: CAPDU instruction byte (INS)
        :param p1: CAPDU parameter #1 byte (P1)
        :param p2: CAPDU parameter #2 byte (P2)
        :param data: CAPDU data bytes
        :param le: response length expected (Le)
        :param force_add_le: force addition of 0x00 Le byte to the resulting CAPDU bytes
        """
        self.cla = cla
        self.ins = ins
        self.p1 = p1
        self.p2 = p2
        self.data = data
        self.le = le
        self.force_add_le = force_add_le

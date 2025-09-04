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

from openscp.utils import _start_jvm_if_needed
from enum import Enum

_start_jvm_if_needed()
import com.samsung.openscp


class ScpMode(Enum):
    """SCP mode, which defines size of challenges, cryptograms and MACs"""

    S8 = com.samsung.openscp.ScpMode.S8
    S16 = com.samsung.openscp.ScpMode.S16

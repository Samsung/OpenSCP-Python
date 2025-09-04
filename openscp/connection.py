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

from typing import Any

from openscp.utils import _start_jvm_if_needed, _java_bytes_to_python_bytes

from jpype import JImplements, JOverride

from abc import ABC, abstractmethod

_start_jvm_if_needed()
import com.samsung.openscp


@JImplements(com.samsung.openscp.SmartCardConnection)
class SmartCardConnection(ABC):
    """Smart card connection interface, which library user should implement using real connection to the eSE chip"""

    @abstractmethod
    def send_and_receive(self, apdu: bytes) -> bytes:
        """
        APDU processing callback. Will be called when library code will need communicate with a smart card.

        :param apdu: Command APDU bytes
        :return: Response APDU bytes
        """
        raise NotImplementedError("Abstract method is not implemented")

    @abstractmethod
    def is_extended_length_apdu_supported(self) -> bool:
        """
        Will be called at the connection start to choose the APDU size to use.

        :return: is extended APDU length supported by a smart card
        """
        raise NotImplementedError("Abstract method is not implemented")

    @abstractmethod
    def close_connection(self) -> None:
        """
        Smart card connection closure callback. Will be called at the end of the session.

        :return: None
        """
        raise NotImplementedError("Abstract method is not implemented")

    @JOverride  # type: ignore[misc]
    # apdu: byte[] (Java primitive)
    def sendAndReceive(self, apdu: Any) -> bytes:
        """Java interface callback implementation. DO NOT override"""
        apdu_in_python_bytes = _java_bytes_to_python_bytes(apdu)
        return self.send_and_receive(apdu_in_python_bytes)

    @JOverride  # type: ignore[misc]
    def isExtendedLengthApduSupported(self) -> bool:
        """Java interface callback implementation. DO NOT override"""
        return self.is_extended_length_apdu_supported()

    @JOverride  # type: ignore[misc]
    def close(self) -> None:
        """Java interface callback implementation. DO NOT override"""
        return self.close_connection()

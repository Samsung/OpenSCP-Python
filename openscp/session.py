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

from typing import List, Any, Optional

import openscp.connection
import openscp.scp_mode
from openscp.scp_certificate import ScpCertificate
import openscp.aes_alg
import openscp.apdu
from openscp.utils import _start_jvm_if_needed, _java_bytes_to_python_bytes, _python_bytes_to_java_bytes

_start_jvm_if_needed()
import java.security
import java.util
import org.bouncycastle.jce.provider
import com.samsung.openscp


class SecurityDomainSession:
    """SCP03 and SCP11 session implementation"""

    def __init__(self, connection: openscp.connection.SmartCardConnection) -> None:
        """
        :param connection: :class:`openscp.SmartCardConnection` interface implementation
        """
        security_provider = org.bouncycastle.jce.provider.BouncyCastleProvider()
        self._session = com.samsung.openscp.SecurityDomainSession(connection, security_provider)

    def authenticate_scp03(self,
                           key_id: int,
                           key_version: int,
                           enc_key: bytes,
                           mac_key: bytes,
                           dek_key: bytes,
                           scp_mode: openscp.scp_mode.ScpMode) -> None:
        """
        Perform SCP03 authentication - execute INITIALIZE UPDATE & EXTERNAL AUTHENTICATE commands

        :param key_id: SCP key identifier
        :param key_version: SCP key version number
        :param enc_key: static secure channel encryption key
        :param mac_key: static secure channel message authentication code key
        :param dek_key: static data encryption key
        :param scp_mode: SCP mode - S8 or S16
        :return: None

        :raises: exceptions from underlying Java library
        """
        self._authenticate_scp03(key_id, key_version, enc_key, mac_key, dek_key, scp_mode)

    def authenticate_scp11(self,
                           sd_key_id: int,
                           sd_key_version: int,
                           oce_key_id: int,
                           oce_key_version: int,
                           pk_sd_ecka_bytes: bytes,
                           cert_chain_oce_ecka: List[bytes],
                           sk_oce_ecka_bytes: bytes,
                           session_keys_alg: openscp.aes_alg.AesAlg,
                           scp_mode: openscp.scp_mode.ScpMode) -> None:
        """
        Perform SCP11 authentication - execute PERFORM_SECURITY_OPERATION & MUTUAL_AUTHENTICATE commands

        :param sd_key_id: security domain SCP key identifier of associated SK.SD.ECKA
        :param sd_key_version: security domain SCP key version number of associated SK.SD.ECKA
        :param oce_key_id: off-card entity SCP key identifier of associated SK.OCE.ECKA
        :param oce_key_version: off-card entity SCP key version number of associated SK.OCE.ECKA
        :param pk_sd_ecka_bytes: public key of the SD used for key agreement in encoded form (PK.SD.ECKA)
        :param cert_chain_oce_ecka: certificate chain including the certificate containing the public key of the OCE
                                    used for key agreement in encoded form (CERT.OCE.ECKA)
        :param sk_oce_ecka_bytes: private key of the OCE used for key agreement in encoded form (SK.OCE.ECKA)
        :param session_keys_alg: AES algorithm for session keys that will be generated
        :param scp_mode: SCP mode - S8 or S16
        :return: None

        :raises: exceptions from underlying Java library
        """
        self._authenticate_scp11(sd_key_id,
                                 sd_key_version,
                                 oce_key_id,
                                 oce_key_version,
                                 pk_sd_ecka_bytes,
                                 cert_chain_oce_ecka,
                                 sk_oce_ecka_bytes,
                                 session_keys_alg,
                                 scp_mode)

    def get_certificate_bundle(self, sd_key_id: int, sd_key_version: int) -> List[ScpCertificate]:
        """
        Retrieve an SCP11 Certificate Store from smart card

        :param sd_key_id: security domain SCP key identifier of associated SK.SD.ECKA
        :param sd_key_version: security domain SCP key version number of associated SK.SD.ECKA
        :return: list of certificates from smart card

        :raises: exceptions from underlying Java library
        """
        key_ref = com.samsung.openscp.KeyRef(sd_key_id, sd_key_version)
        certs_list_java = self._session.getCertificateBundle(key_ref)
        certs_list = []
        for cert_java in certs_list_java:
            certs_list.append(ScpCertificate(cert_java))
        return certs_list

    def send_and_receive(self, capdu: openscp.apdu.Apdu) -> bytes:
        """
        Send Command APDU, wait for Response APDU from smart card

        :param capdu: Command APDU bytes
        :return: Response APDU data bytes
        """
        java_capdu = com.samsung.openscp.Apdu(
            capdu.cla,
            capdu.ins,
            capdu.p1,
            capdu.p2,
            capdu.data,
            capdu.le,
            capdu.force_add_le
        )
        java_rapdu_data = self._session.sendAndReceive(java_capdu)
        return _java_bytes_to_python_bytes(java_rapdu_data)

    def _authenticate_scp03(self,
                            key_id: int,
                            key_version: int,
                            enc_key: bytes,
                            mac_key: bytes,
                            dek_key: bytes,
                            scp_mode: openscp.scp_mode.ScpMode,
                            host_challenge: Optional[bytes] = None) -> None:
        key_ref = com.samsung.openscp.KeyRef(key_id, key_version)
        static_keys = com.samsung.openscp.StaticKeys(enc_key, mac_key, dek_key)
        key_params = com.samsung.openscp.Scp03KeyParams(key_ref, static_keys)
        if host_challenge:  # API for testing
            self._session.authenticate(key_params, scp_mode.value, host_challenge)
        else:
            self._session.authenticate(key_params, scp_mode.value)

    def _authenticate_scp11(self,
                            sd_key_id: int,
                            sd_key_version: int,
                            oce_key_id: int,
                            oce_key_version: int,
                            pk_sd_ecka_bytes: bytes,
                            cert_chain_oce_ecka: List[bytes],
                            sk_oce_ecka_bytes: bytes,
                            session_keys_alg: openscp.aes_alg.AesAlg,
                            scp_mode: openscp.scp_mode.ScpMode,
                            epk_oce_ecka_bytes: Optional[bytes] = None,
                            esk_oce_ecka_bytes: Optional[bytes] = None) -> None:
        key_params = self._create_java_scp11_key_params(sd_key_id,
                                                        sd_key_version,
                                                        oce_key_id,
                                                        oce_key_version,
                                                        pk_sd_ecka_bytes,
                                                        cert_chain_oce_ecka,
                                                        sk_oce_ecka_bytes,
                                                        session_keys_alg)
        if epk_oce_ecka_bytes and esk_oce_ecka_bytes:  # API for testing
            ephemeral_key_pair = self._create_java_key_pair(epk_oce_ecka_bytes, esk_oce_ecka_bytes)
            self._session.authenticate(key_params, scp_mode.value, ephemeral_key_pair)
        else:
            self._session.authenticate(key_params, scp_mode.value)

    def _create_java_scp11_key_params(self,
                                      sd_key_id: int,
                                      sd_key_version: int,
                                      oce_key_id: int,
                                      oce_key_version: int,
                                      pk_sd_ecka_bytes: bytes,
                                      cert_chain_oce_ecka: List[bytes],
                                      sk_oce_ecka_bytes: bytes,
                                      session_keys_alg: openscp.aes_alg.AesAlg) -> Any:
        # -> com.samsung.openscp.Scp11KeyParams
        pk_sd_ecka = self._create_java_ec_public_key(pk_sd_ecka_bytes)
        oce_key_ref = com.samsung.openscp.KeyRef(oce_key_id, oce_key_version)
        sd_key_ref = com.samsung.openscp.KeyRef(sd_key_id, sd_key_version)
        sk_oce_ecka = self._create_java_ec_private_key(sk_oce_ecka_bytes)
        java_oce_cert_bytes_chain = [_python_bytes_to_java_bytes(cert_bytes) for cert_bytes in cert_chain_oce_ecka]
        java_oce_cert_chain = java.util.Arrays.asList(*java_oce_cert_bytes_chain)
        return com.samsung.openscp.Scp11KeyParams(
            sd_key_ref,
            pk_sd_ecka,
            oce_key_ref,
            sk_oce_ecka,
            java_oce_cert_chain,
            session_keys_alg.value
        )

    def _create_java_key_pair(self, public_key_bytes: bytes, private_key_bytes: bytes) -> Any:
        # -> java.security.KeyPair
        public_key = self._create_java_ec_public_key(public_key_bytes)
        private_key = self._create_java_ec_private_key(private_key_bytes)
        return java.security.KeyPair(public_key, private_key)

    def _create_java_ec_public_key(self, key_bytes: bytes) -> Any:  # -> java.security.PublicKey
        key_factory = java.security.KeyFactory.getInstance("EC")
        key_spec = java.security.spec.X509EncodedKeySpec(key_bytes)
        return key_factory.generatePublic(key_spec)

    def _create_java_ec_private_key(self, key_bytes: bytes) -> Any:  # -> java.security.PrivateKey
        key_factory = java.security.KeyFactory.getInstance("EC")
        key_spec = java.security.spec.PKCS8EncodedKeySpec(key_bytes)
        return key_factory.generatePrivate(key_spec)

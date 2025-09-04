from openscp import SmartCardConnection, SecurityDomainSession, ScpMode, Apdu, AesAlg


class Scp11ReaderTemplate:
    def __init__(self, sk_oce_ecka: bytes, cert_oce_ecka: bytes, session_keys_alg: AesAlg) -> None:
        self.sk_oce_ecka = sk_oce_ecka
        self.cert_oce_ecka = cert_oce_ecka
        self.session_keys_alg = session_keys_alg
        connection = self.Connection()
        self.session = SecurityDomainSession(connection)

    def open(self, aid: bytes) -> None:
        # Add here code to open eSE Reader class session with specified 'aid'
        session_key_id = 0x11
        session_key_version = 0x03
        try:
            certificates = self.session.get_certificate_bundle(session_key_id, session_key_version)
        except:
            raise Exception  # Throw your exception here
        if not certificates:
            raise Exception  # Throw your exception here
        oce_key_id = 0x10
        oce_key_version = 0x03
        cert_sd_ecka = certificates[-1]
        cert_oce_ecka_chain = [self.cert_oce_ecka]
        scp_mode = ScpMode.S8
        try:
            self.session.authenticate_scp11(session_key_id,
                                            session_key_version,
                                            oce_key_id,
                                            oce_key_version,
                                            cert_sd_ecka.get_public_key(),
                                            cert_oce_ecka_chain,
                                            self.sk_oce_ecka,
                                            self.session_keys_alg,
                                            scp_mode)
        except:
            raise Exception  # Throw your exception here

    def transmit(self, apdu: Apdu) -> bytes:
        try:
            return self.session.send_and_receive(apdu)
        except:
            raise Exception  # Throw your exception here

    def close(self) -> None:
        # Add here code to close eSE Reader session

    class Connection(SmartCardConnection):
        def send_and_receive(self, apdu: bytes) -> bytes:
            # Call here 'transmitPlainChannel()' method of your eSE Reader class to send & receive raw APDU
            try:
                return transmitPlainChannel(apdu)
            except:  # Use here exception specific to your eSE Reader class implementation
                self.close_connection()
                raise Exception  # Throw your exception here

        def is_extended_length_apdu_supported(self) -> bool:
            return True

        def close_connection(self) -> None:
            self.close()

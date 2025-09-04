from openscp import SmartCardConnection, SecurityDomainSession, ScpMode, Apdu


class Scp03ReaderTemplate:
    def __init__(self, enc: bytes, mac: bytes, dek: bytes) -> None:
        self.enc = enc
        self.mac = mac
        self.dek = dek
        connection = self.Connection()
        self.session = SecurityDomainSession(connection)

    def open(self, aid: bytes) -> None:
        # Add here code to open eSE Reader class session with specified 'aid'
        key_id = 0x01
        key_version = 0x30
        scp_mode = ScpMode.S8
        try:
            self.session.authenticate_scp03(key_id, key_version, self.enc, self.mac, self.dek, scp_mode)
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

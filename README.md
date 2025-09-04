![Logo](docs/img/openscp-icon.png)

# SCP03 and SCP11 protocols implementation for off-card entity

## General information

### Description

The library provides support for secure communication between off-card entity (OCE) and Security Domain (SD)
using GlobalPlatform's (GP) Secure Channel Protocols that are based on static symmetric keys (SCP03) and certificates (SCP11)

### Specifications

The feature set is according to the specifications listed below except for what is mentioned in known issues:

- [SCP03](https://globalplatform.org/specs-library/secure-channel-protocol-03-amendment-d-v1-2/) up to v1.2
- [SCP11](https://globalplatform.org/specs-library/secure-channel-protocol-11-amendment-f/) up to v1.4

### API documentation

Please refer to the API documentation in the "docs/html" directory for details

### Known issues

#### SCP03 not implemented features

- Lower security levels support - only maximum security level is supported now (C-DECRYPTION, R-ENCRYPTION, C-MAC, and R-MAC)
- Pseudo-random card challenge verification - verification is optional according to the specification
- BEGIN R-MAC session & END R-MAC session commands - implementation is optional according to the specification

#### SCP11 not implemented features

- SD certificate validation
- Usage of CA-KLCC Identifier in GET_DATA (Certificate Store), MUTUAL AUTHENTICATE.
  - For now, only "KID/KVN" is used
  - "CA-KLCC Identifier" and "KID/KVN" usage is mutually exclusive and shall be chosen by OCE
- Usage of Host and Card ID in Key Derivation process
  - For now, it is not used
  - HostID usage is chosen by OCE during MUTUAL AUTHENTICATE / INTERNAL AUTHENTICATE
- Lower security levels support - only maximum security level is supported now (C-DECRYPTION, R-ENCRYPTION, C-MAC, and R-MAC)
  - Key usage is chosen by OCE during MUTUAL AUTHENTICATE / INTERNAL AUTHENTICATE
- Some library exceptions might be not descriptive enough

***

## Environment information

### Requirements

- Python version 3.7+

### Dependencies

- [JPype](https://github.com/jpype-project/jpype)

### Install

``` bash
python3 -m pip install JPype1
python3 -m pip install openscp-*.tar.gz
```

***

## Example of usage

### SCP03 implementation guide
Below is step-by-step explanation of how to use SCP03 protocol to communicate with a smart card.
The similar approach can be used for SCP11.
Also please refer to SCP Reader class example at **examples/scp03_reader_template.py** file

#### Define SCP03 keys

Declare static SCP03 keys:

``` python
enc_key = bytes.fromhex("...")
mac_key = bytes.fromhex("...")
dek_key = bytes.fromhex("...")
```

Declare reference to these keys on the smart card:

``` python
key_id = 0x01
key_version = 0x30
```

#### Define connection class to smart card

Implement SmartCardConnection interface using your connection to the smart card:

``` python
class MySmartCardConnection(SmartCardConnection):
    def send_and_receive(self, apdu: bytes) -> bytes:
        # Use your physical channel to the smart card
        return rapdu

    def is_extended_length_apdu_supported(self) -> bool:
        # Return your smart card property
        return True

    def close_connection(self) -> None:
        # Close your physical chanel to the smart card
        pass
```

See the SmartCardConnection docstrings for additional information.

#### Create and use SCP03 session

Set SCP03 mode (S8 or S16) and initialize SCP03 protocol using variables declared above:

``` python
session = SecurityDomainSession(MySmartCardConnection())
session.authenticate_scp03(key_id, key_version, enc_key, mac_key, dek_key, ScpMode.S8)
```

Transmit APDUs:

``` python
# GlobalPlatform Card Specification, "11.4 GET STATUS Command"
get_status_capdu = Apdu(
    0x80, # CLA
    0xF2, # INS
    0x40, # P1 - list applets or security domains
    0x00, # P2
    bytes.fromhex("4F00")) # data - search qualifier: all IDs
rapdu_data = session.send_and_receive(get_status_capdu)
```

### SCP11 implementation guide

Below is step-by-step explanation of how to use SCP11 protocol to communicate with a smart card.
Also please refer to SCP Reader class example at **examples/scp11_reader_template.py** file

#### Define SCP11 credentials

Declare OCE SCP11 certificates chain and private key:

``` python
cert_chain_oce_ecka_p256 = [bytes.fromhex("..."), ...]
sk_oce_ecka_p256 = bytes.fromhex("...")
```

Declare AES algorithm for session keys that will be generated:

``` python 
aesAlg = AesAlg.AES_256
```

Declare reference to SD and OCE keys on the smart card:

``` python
session_key_id = 0x11
session_key_version = 0x03

oce_key_id = 0x10
oce_key_version = 0x03
```

#### Define connection class with SCP11 to smart card

Please see the corresponding section in the SCP03 guide above

#### Create and use SCP11 session

Get SD certificate public key from the smart card:

``` python
session = SecurityDomainSession(MySmartCardConnection())
certificates = session.get_certificate_bundle(session_key_id, session_key_version)
cert_sd_ecka = certificates[-1]
pk_sd_ecka = cert_sd_ecka.get_public_key()
```

Set SCP03 mode (S8 or S16) for session keys and initialize SCP11 protocol using variables declared above:

``` python
session.authenticate_scp11(session_key_id,
                            session_key_version,
                            oce_key_id,
                            oce_key_version,
                            pk_sd_ecka,
                            cert_chain_oce_ecka_p256
                            sk_oce_ecka_p256,
                            aesAlg,
                            ScpMode.S8)
```

See APDU transmission example in the corresponding section of the SCP03 guide above.

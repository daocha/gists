# AES helper class for pycrypto
# Copyright (c) Dennis Lee
# Date 22 Mar 2017

# Description:
# Python helper class to perform AES encryption, decryption with CBC Mode & PKCS7 Padding

# References:
# https://www.dlitz.net/software/pycrypto/api/2.6/
# http://japrogbits.blogspot.my/2011/02/using-encrypted-data-between-python"-and.html

from Cryptodome.Cipher import AES
from .pkcs7 import PKCS7Encoder
from base64 import b64encode, b64decode

encoder = PKCS7Encoder()
secret = "asdf;lkjqwert23423423vcdertgftg"
salt = "dksflesfsdfsfwe8923"


def encryptAsStr(plaintext, key, iv):
    ciphertext = encrypt(plaintext, key, iv)
    return b64encode(ciphertext).decode("utf-8")


def encrypt(plaintext, key, iv):
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    elif isinstance(key, (bytes, bytearray)):
        key_bytes = key
    else:
        raise ValueError("Unsupported type[:%s] for key." % type(key))

    if isinstance(iv, str):
        iv_bytes = iv.encode("utf-8")
    elif isinstance(iv, (bytes, bytearray)):
        iv_bytes = iv
    else:
        raise ValueError("Unsupported type[:%s] for iv." % type(iv))

    key_length = len(key_bytes)
    if (key_length >= 32):
        k = key_bytes[:32]
    elif (key_length >= 24):
        k = key_bytes[:24]
    else:
        k = key_bytes[:16]

    aes = AES.new(k, AES.MODE_CBC, iv_bytes[:16])
    pad_text = encoder.encode(plaintext)
    return aes.encrypt(pad_text)


def decryptAsStr(ciphertext, key, iv):
    return decrypt(b64decode(ciphertext), key, iv).decode("utf-8")


def decrypt(ciphertext, key, iv):
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    elif isinstance(key, (bytes, bytearray)):
        key_bytes = key
    else:
        raise ValueError("Unsupported type[:%s] for key." % type(key))

    if isinstance(iv, str):
        iv_bytes = iv.encode("utf-8")
    elif isinstance(iv, (bytes, bytearray)):
        iv_bytes = iv
    else:
        raise ValueError("Unsupported type[:%s] for iv." % type(iv))

    key_length = len(key_bytes)
    if (key_length >= 32):
        k = key_bytes[:32]
    elif (key_length >= 24):
        k = key_bytes[:24]
    else:
        k = key_bytes[:16]

    aes = AES.new(k, AES.MODE_CBC, iv_bytes[:16])
    pad_text = aes.decrypt(ciphertext)
    return encoder.decode(pad_text)


def encryptAES(plaintext):
    """
    Encryption with AES
    Args:
        plaintext: plaintext
    """
    return encryptAsStr(plaintext, secret, salt)


def decryptAES(ciphertext):
    """
    Decryption with AES
    Args:
        ciphertext: ciphertext
    """
    return decryptAsStr(ciphertext, secret, salt)

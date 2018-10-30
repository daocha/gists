# Date: 30 Oct 2018
# Author: Ray LI
""" Test case for AES encryption """

from dcha.security import aes


def test_encryption():
    """
        Test encryption and decryption
    """
    plantext = "testing+/45M=()*&^%$#"
    ciphertext = aes.encryptAES(plantext)
    decrypted_text = aes.decryptAES(ciphertext)
    assert plantext == decrypted_text

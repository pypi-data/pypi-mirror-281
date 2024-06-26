from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import json
import base64

class Cipher:
    def __init__(self, key, iv=None, mode=AES.MODE_CBC):
        self.key = key
        self.iv = iv
        self.mode = mode
        self.cipher = AES.new(self.key.encode("utf8"), self.mode, iv=self.iv.encode("utf8")) if self.iv else AES.new(self.key.encode("utf8"), self.mode)

    def encrypt(self, plaintext):
        if isinstance(plaintext, dict):
            plaintext = json.dumps(plaintext)
        elif not isinstance(plaintext, str):
            raise ValueError("Plaintext must be a string or a JSON object")

        
        ciphertext = self.cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        encrypted_bytes = binascii.hexlify(ciphertext)
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64

    def decrypt(self, ciphertext):
        ciphertext_bytes = base64.b64decode(ciphertext.encode('utf-8'))
        ciphertext_bytes = binascii.unhexlify(ciphertext_bytes)
        
        decrypted_text = unpad(self.cipher.decrypt(ciphertext_bytes), AES.block_size)

        try:
            decrypted_text = decrypted_text.decode('utf-8')
            if decrypted_text.startswith('{') and decrypted_text.endswith('}'):
                decrypted_text = json.loads(decrypted_text)
        except UnicodeDecodeError:
            pass

        return decrypted_text

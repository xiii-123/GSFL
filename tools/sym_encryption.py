from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def getSymKey(key_size=16):
    """
    生成指定长度的AES密钥
    :param key_size: 密钥长度，可以是16, 24, 或 32字节
    :return: 生成的密钥
    """
    if key_size not in [16, 24, 32]:
        raise ValueError("Invalid AES key size. It must be either 16, 24, or 32 bytes.")
    key = get_random_bytes(key_size)
    return key

def SymEncrypt(plaintext, key):
    """
    使用AES算法加密明文
    :param plaintext: 明文字符串
    :param key: AES密钥
    :return: 加密后的密文
    """
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def SymDecrypt(ciphertext, key):
    """
    使用AES算法解密密文
    :param ciphertext: 密文字节串
    :param key: AES密钥
    :return: 解密后的明文字符串
    """
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return plaintext

# 使用示例
if __name__ == "__main__":
    # 生成密钥
    key = getSymKey(16)  # 选择16字节（128位）密钥

    # 明文
    message = b'123456'

    # 加密
    encrypted_message = SymEncrypt(message, key)
    print(f"Encrypted message: {encrypted_message}")

    # 解密
    decrypted_message = SymDecrypt(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")

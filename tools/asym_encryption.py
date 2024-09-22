from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


def getAsyKeys():
    # 生成RSA密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # 将私钥和公钥序列化为PEM格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()


def AsyEncrypt(public_key: str, plaintext: str) -> str:
    # 反序列化公钥
    public_key_obj = serialization.load_pem_public_key(
        public_key.encode(),
        backend=default_backend()
    )

    # 使用公钥加密消息
    ciphertext = public_key_obj.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext.hex()


def AsyDecrypt(private_key: str, ciphertext: str) -> str:
    # 反序列化私钥
    private_key_obj = serialization.load_pem_private_key(
        private_key.encode(),
        password=None,
        backend=default_backend()
    )

    # 将十六进制编码的密文转换为字节
    ciphertext_bytes = bytes.fromhex(ciphertext)

    # 使用私钥解密消息
    plaintext = private_key_obj.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext.decode()

if __name__ == '__main__':
    # 使用示例
    private_key, public_key = getAsyKeys()

    # 打印私钥和公钥
    print("Private Key:\n", private_key)
    print("\nPublic Key:\n", public_key)

    private_key, public_key = getAsyKeys()

    # 打印私钥和公钥
    print("Private Key:\n", private_key)
    print("\nPublic Key:\n", public_key)

    private_key, public_key = getAsyKeys()

    # 打印私钥和公钥
    print("Private Key:\n", private_key)
    print("\nPublic Key:\n", public_key)

    

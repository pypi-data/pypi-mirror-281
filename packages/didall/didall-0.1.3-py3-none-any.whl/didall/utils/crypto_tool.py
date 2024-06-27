from datetime import datetime
import hashlib
import base64
import json
import os
import secrets
import logging
from typing import Any, Dict, Tuple
import base58
import struct
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# 生成32字节的随机数
def generate_random_hex(length=32):
    return secrets.token_hex(length)

def generate_16_char_from_random_num(random_num1: str, random_num2: str):
    content = random_num1 + random_num2
    random_bytes = content.encode('utf-8')
    
    # 使用HKDF派生8字节的随机数
    hkdf = HKDF(
        algorithm=hashes.SHA256(),  # 确保使用的是cryptography库中的哈希算法实例
        length=8,  # 生成8字节的密钥
        salt=None,
        info=b'',  # 可选的上下文信息，用于区分不同用途的密钥
        backend=default_backend()  # 使用默认的加密后端
    )
    
    derived_key = hkdf.derive(random_bytes)
    
    # 将派生的密钥编码为十六进制字符串
    derived_key_hex = derived_key.hex()
    
    return derived_key_hex

def get_hex_from_public_key(public_key: ec.EllipticCurvePublicKey) -> str:
    """将EC公钥转换为十六进制字符串"""
    # 获取公钥的字节表示形式
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    # 将字节转换为十六进制字符串
    return public_key_bytes.hex()

def get_public_key_from_hex(public_key_hex: str, curve: ec.EllipticCurve = ec.SECP256R1()) -> ec.EllipticCurvePublicKey:
    """从十六进制字符串中提取EC公钥，指定椭圆曲线"""
    # 将十六进制字符串转换为字节
    public_key_bytes = bytes.fromhex(public_key_hex)
    # 从字节创建公钥
    return ec.EllipticCurvePublicKey.from_encoded_point(curve, public_key_bytes)


# 生成ECDSA私钥和公钥对
def generate_ec_key_pair(curve: ec.EllipticCurve=ec.SECP256R1()) -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey, str]:
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    public_key_hex = '04' + format(public_numbers.x, '064x') + format(public_numbers.y, '064x')
    return private_key, public_key, public_key_hex

def generate_secp256r1_private_key() -> ec.EllipticCurvePrivateKey:
    """生成Secp256r1私钥"""
    return ec.generate_private_key(ec.SECP256R1())

def generate_secp256r1_public_key(private_key: ec.EllipticCurvePrivateKey) -> ec.EllipticCurvePublicKey:
    """根据Secp256r1私钥生成公钥"""
    return private_key.public_key()


def generate_bitcoin_address(public_key: ec.EllipticCurvePublicKey) -> str:
    """根据公钥生成比特币地址"""
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    sha256_pk = hashlib.sha256(public_key_bytes).digest()
    ripemd160_pk = hashlib.new('ripemd160', sha256_pk).digest()
    pubkey_hash = b'\x00' + ripemd160_pk
    checksum = hashlib.sha256(hashlib.sha256(pubkey_hash).digest()).digest()[:4]
    address = base58.b58encode(pubkey_hash + checksum).decode('utf-8')
    return address

def generate_signature_for_json(private_key: ec.EllipticCurvePrivateKey, did_document: Dict[str, Any]) -> str:
    # 将待签名数据转换为 JSON 字符串
    did_document_str = json.dumps(did_document, separators=(',', ':'), sort_keys=True)
    did_document_bytes = did_document_str.encode('utf-8')
    
    # 使用私钥对数据进行签名
    signature = private_key.sign(did_document_bytes, ec.ECDSA(hashes.SHA256()))
    
    # 分离 r 和 s 值
    r, s = decode_dss_signature(signature)
    
    # 将 r 和 s 转换为字节
    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    
    # Base64 URL 安全编码
    proof_value = base64.urlsafe_b64encode(r_bytes + s_bytes).rstrip(b'=').decode('utf-8')
    
    return proof_value

def verify_signature_for_json(public_key: ec.EllipticCurvePublicKey, did_document: Dict[str, Any], signature: str) -> bool:
    """验证JSON消息的签名"""
    try:
        # 将签名从Base64Url编码解码为字节串
        signature_bytes = base64.urlsafe_b64decode(signature + '==')
        
        # 拆分 r 和 s 值
        r_length = len(signature_bytes) // 2
        r_bytes = signature_bytes[:r_length]
        s_bytes = signature_bytes[r_length:]
        
        r = int.from_bytes(r_bytes, byteorder='big')
        s = int.from_bytes(s_bytes, byteorder='big')
        
        # 重新组装为 ASN.1 DER 编码格式
        der_encoded_signature = encode_dss_signature(r, s)
        
        # 将消息转换为字节串
        message_str = json.dumps(did_document, separators=(',', ':'), sort_keys=True)
        message_bytes = message_str.encode('utf-8')
        
        # 验证签名
        public_key.verify(der_encoded_signature, message_bytes, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception as e:
        logging.error(f"签名验证失败: {e}")
        return False
    
def generate_router_json(private_key: ec.EllipticCurvePrivateKey, did_document: Dict[str, Any]) -> Dict[str, Any]:
    """根据私钥和DID文档生成router JSON字典"""
    router_did = did_document.get("id")
    nonce = generate_random_hex(32)  # 假设有一个函数generate_random_hex用于生成随机的十六进制字符串
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # 从DID文档中获取verificationMethod
    verification_methods = did_document.get("verificationMethod", [])
    verification_method_id = next((vm["id"] for vm in verification_methods if vm["type"] == "EcdsaSecp256r1VerificationKey2019"), None)

    # 创建router字典
    router = {
        "router": router_did,
        "nonce": nonce,
        "proof": {
            "type": "EcdsaSecp256r1Signature2019",
            "created": current_time,
            "proofPurpose": "assertionMethod",
            "verificationMethod": verification_method_id
        }
    }

    # 使用私钥对router信息进行签名
    proof_value = generate_signature_for_json(private_key, router)
    router["proof"]["proofValue"] = proof_value

    return router

def verify_did_with_public_key(did: str, public_key: ec.EllipticCurvePublicKey) -> bool:
    """根据DID校验公钥"""
    try:
        # 提取比特币地址
        bitcoin_address = did.split(':')[-1]

        # 根据公钥生成比特币地址
        generated_address = generate_bitcoin_address(public_key)

        # 校验生成的比特币地址是否与DID中的地址匹配
        return bitcoin_address == generated_address
    except Exception as e:
        return False

def get_pem_from_private_key(private_key: ec.EllipticCurvePrivateKey) -> str:
    """从EllipticCurvePrivateKey私钥获取PEM格式的字符串"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')


# 从 PEM 格式的字符串加载私钥
def load_private_key_from_pem(pem_str: str) -> ec.EllipticCurvePrivateKey:
    return serialization.load_pem_private_key(
        pem_str.encode('utf-8'),
        password=None,
        backend=default_backend()
    )


def generate_shared_secret(private_key: ec.EllipticCurvePrivateKey, 
                           peer_public_key: ec.EllipticCurvePublicKey) -> bytes:
    # 使用对方的公钥和自己的私钥来生成共享秘密
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_secret

def hkdf_label(length: int, label: bytes, context: bytes) -> bytes:
    full_label = b"als10 " + label
    hkdf_label = struct.pack("!H", length) + struct.pack("!B", len(full_label)) + full_label + struct.pack("!B", len(context)) + context
    return hkdf_label

def get_key_length_from_cipher_suite(cipher_suite: str) -> int:
    if cipher_suite == "TLS_AES_128_GCM_SHA256":
        return 16
    elif cipher_suite == "TLS_AES_256_GCM_SHA384":
        return 32
    elif cipher_suite == "TLS_CHACHA20_POLY1305_SHA256":
        return 32
    else:
        raise ValueError(f"不支持的密码套件: {cipher_suite}")


def derive_tls13_data_keys(shared_secret: bytes, source_hello_random: bytes, 
                           destination_hello_random: bytes, 
                           key_length=16, hash_algorithm=hashes.SHA256()):
    backend = default_backend()

    # HKDF Extract stage
    hkdf_extract = HKDF(
        algorithm=hash_algorithm,
        length=hash_algorithm.digest_size,
        salt=b'\x00' * hash_algorithm.digest_size,  # Initial salt is zeros
        info=None,
        backend=backend
    )
    extracted_key = hkdf_extract.derive(shared_secret)

    # Derive-Secret function in TLS 1.3
    def derive_secret(secret: bytes, label: bytes, messages: bytes) -> bytes:
        hkdf_expand = HKDFExpand(
            algorithm=hash_algorithm,
            length=hash_algorithm.digest_size,
            info=hkdf_label(hash_algorithm.digest_size, label, messages),
            backend=backend
        )
        return hkdf_expand.derive(secret)

    # Generate handshake traffic secrets
    source_data_traffic_secret = derive_secret(extracted_key, b"s ap traffic", source_hello_random + destination_hello_random)
    destination_data_traffic_secret = derive_secret(extracted_key, b"d ap traffic", source_hello_random + destination_hello_random)

    # Expand to generate actual handshake keys
    source_data_key = HKDF(
        algorithm=hash_algorithm,
        length=key_length,  # 256-bit key for AES-256
        salt=None,
        info=hkdf_label(32, b"key", source_data_traffic_secret),
        backend=backend
    ).derive(source_data_traffic_secret)

    destination_data_key = HKDF(
        algorithm=hash_algorithm,
        length=key_length,  # 256-bit key for AES-256
        salt=None,
        info=hkdf_label(32, b"key", destination_data_traffic_secret),
        backend=backend
    ).derive(destination_data_traffic_secret)

    # Return derived handshake keys and secrets
    return (source_data_key, destination_data_key, source_data_traffic_secret, destination_data_traffic_secret)

# 生成TLS1.3应用层密钥，暂时不用
def derive_tls13_application_keys(client_handshake_traffic_secret, server_handshake_traffic_secret, hash_algorithm=hashes.SHA256()):
    backend = default_backend()

    # Derive application traffic secrets
    client_application_traffic_secret = HKDFExpand(
        algorithm=hash_algorithm,
        length=hash_algorithm.digest_size,
        info=hkdf_label(hash_algorithm.digest_size, b"c ap traffic", b""),
        backend=backend
    ).derive(client_handshake_traffic_secret)

    server_application_traffic_secret = HKDFExpand(
        algorithm=hash_algorithm,
        length=hash_algorithm.digest_size,
        info=hkdf_label(hash_algorithm.digest_size, b"s ap traffic", b""),
        backend=backend
    ).derive(server_handshake_traffic_secret)

    # Expand to generate actual application keys
    client_application_key = HKDF(
        algorithm=hash_algorithm,
        length=32,  # 256-bit key for AES-256
        salt=None,
        info=hkdf_label(32, b"key", client_application_traffic_secret),
        backend=backend
    ).derive(client_application_traffic_secret)

    server_application_key = HKDF(
        algorithm=hash_algorithm,
        length=32,  # 256-bit key for AES-256
        salt=None,
        info=hkdf_label(32, b"key", server_application_traffic_secret),
        backend=backend
    ).derive(server_application_traffic_secret)

    # Return derived application keys and secrets
    return {
        'client_application_key': client_application_key,
        'server_application_key': server_application_key,
        'client_application_traffic_secret': client_application_traffic_secret,
        'server_application_traffic_secret': server_application_traffic_secret
    }

# TLS_AES_128_GCM_SHA256加密函数
def encrypt_aes_gcm_sha256(data: bytes, key: bytes) -> Dict[str, str]:
    # 确保密钥长度为16字节（128位）
    if len(key) != 16:
        raise ValueError("Key must be 128 bits (16 bytes).")
    
    # 生成随机IV
    iv = os.urandom(12)  # 对于GCM，推荐的IV长度是12字节
    
    # 创建加密对象
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    
    # 加密数据
    ciphertext = encryptor.update(data) + encryptor.finalize()
    
    # 获取tag
    tag = encryptor.tag
    
    # 编码为Base64
    iv_encoded = base64.b64encode(iv).decode('utf-8')
    tag_encoded = base64.b64encode(tag).decode('utf-8')
    ciphertext_encoded = base64.b64encode(ciphertext).decode('utf-8')
    
    # 创建JSON对象
    encrypted_data = {
        "iv": iv_encoded,
        "tag": tag_encoded,
        "ciphertext": ciphertext_encoded
    }
        
    return encrypted_data

def decrypt_aes_gcm_sha256(encrypted_json: Dict[str, str], key: bytes) -> str:
    # Base64解码
    iv = base64.b64decode(encrypted_json["iv"])
    ciphertext = base64.b64decode(encrypted_json["ciphertext"])
    tag = base64.b64decode(encrypted_json["tag"])
    
    # 创建解密对象
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    
    # 解密数据
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    return plaintext.decode()



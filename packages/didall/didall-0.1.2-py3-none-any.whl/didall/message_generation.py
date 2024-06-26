# Cross-Platform Identity Authentication and End-to-End Encrypted Communication Technology Based on DID
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: http://pi-unlimited.com
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.
# Version: 0.1.0

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List
import hashlib
import hmac
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import constant_time
from didall.utils.crypto_tool import encrypt_aes_gcm_sha256, generate_16_char_from_random_num, generate_random_hex, generate_signature_for_json

def generate_register_message(version: str, 
                              routers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成注册router的消息。
    :param routers: 包含router信息的列表，每个router应包含router DID、nonce和proof。
    :return: 构造的注册消息字典。
    """
    registration_message = {
        "version": version,
        "type": "register",
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": generate_random_hex(16),
        "routers": routers
    }
    return registration_message


# 生成SourceHello消息
def generate_source_hello(version: str, session_id: str, source_private_key: ec.EllipticCurvePrivateKey, 
                          source_did: str, destination_did: str, random: str,
                          source_public_key_hex: str, key_share_list: List[Dict[str, Any]],
                          cipher_suite_list: List[str]) -> Dict[str, Any]:
        
    source_hello = {
        "version": version,
        "type": "sourceHello",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": generate_random_hex(16),
        "sessionId": session_id,
        "sourceDid": source_did,
        "destinationDid": destination_did,
        "verificationMethod": {
            "id": f"{source_did}#keys-1",
            "type": "EcdsaSecp256r1VerificationKey2019",
            "publicKeyHex": source_public_key_hex
        },
        "random": random,
        "supportedVersions": ["1.0"],
        "cipherSuites": cipher_suite_list,
        "supportedGroups": [
            "secp256r1"
            # "secp384r1",
            # "secp521r1"
        ],
        "keyShares": key_share_list
    }

    proof = {
        "type": "EcdsaSecp256k1Signature2019",
        "verificationMethod": f"{source_did}#keys-1",
        "created": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    
    source_hello["proof"] = proof
    
    # 使用源私钥签名消息
    proof["proofValue"] = generate_signature_for_json(source_private_key, source_hello)

    source_hello["proof"] = proof

    return source_hello

# 生成DestinationHello消息
def generate_destination_hello(version: str, session_id: str, source_private_key: ec.EllipticCurvePrivateKey, 
                               source_did: str, destination_did: str, random: str,
                               source_public_key_hex: str, key_share: Dict[str, Any],
                               cipher_suite: str) -> Dict[str, Any]:
    
    destination_hello = {
        "version": version,
        "type": "destinationHello",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": generate_random_hex(16),
        "sessionId": session_id,
        "sourceDid": source_did,
        "destinationDid": destination_did,
        "verificationMethod": {
            "id": f"{source_did}#keys-1",
            "type": "EcdsaSecp256r1VerificationKey2019",
            "publicKeyHex": source_public_key_hex
        },
        "random": random,
        "selectedVersion": version,
        "cipherSuite": cipher_suite,
        "keyShare": key_share
    }

    # 准备签名
    proof = {
        "type": "EcdsaSecp256k1Signature2019",
        "verificationMethod": f"{source_did}#keys-1",
        "created": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    
    destination_hello["proof"] = proof
    
    # 使用源私钥签名消息
    proof["proofValue"] = generate_signature_for_json(source_private_key, destination_hello)

    destination_hello["proof"] = proof

    return destination_hello


def generate_finished_message(version: str, session_id: str, source_did: str, destination_did: str, 
                              source_hello_random: str, destination_hello_random: str, 
                              data_secret: bytes) -> Dict[str, Any]:
    """
    生成 Finished 消息
    :param version: 当前协议使用的版本号
    :param session_id: 会话ID
    :param source_did: 源的DID标识符
    :param destination_did: 目的的DID标识符
    :param source_hello_random: 源Hello消息中的随机数
    :param destination_hello_random: 目的Hello消息中的随机数
    :param data_secret: 已协商的握手密钥
    :return: Finished 消息的字典
    """
    # 生成 secret_key_id
    secret_key_id = generate_16_char_from_random_num(source_hello_random, destination_hello_random)
    
    secret_key_id_dict = {
        "secretKeyId": secret_key_id,
    }
    # 生成 verifyData
    verify_data_dict = encrypt_aes_gcm_sha256(json.dumps(secret_key_id_dict).encode(), data_secret)
    
    # 构造 Finished 消息
    finished_message = {
        "version": version,
        "type": "finished",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": generate_random_hex(16),        
        "sessionId": session_id,
        "sourceDid": source_did,
        "destinationDid": destination_did,
        "verifyData": verify_data_dict
    }
    
    return finished_message

def generate_response_message(version: str, original_type: str, message_id: str, 
                              code: int, detail: str) -> Dict[str, Any]:
    """
    生成响应消息
    :param version: 当前协议使用的版本号
    :param original_type: 原始消息类型
    :param code: 响应代码
    :param detail: 响应详情
    :return: 响应消息的字典
    """
    response_message = {
        "version": version,
        "type": "response",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": message_id,
        "originalType": original_type,
        "code": code,
        "detail": detail
    }
    return response_message

def generate_encrypted_message(version: str,  message_id: str, source_did: str, 
                               destination_did: str, secret_key_id: str, 
                               data: bytes, data_secret: bytes) -> Dict[str, Any]:
    """
    生成加密消息
    """
    encrypted_data = encrypt_aes_gcm_sha256(data, data_secret)
    encrypted_message = {
        "version": version,
        "type": "message",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "messageId": message_id,
        "sourceDid": source_did,
        "destinationDid": destination_did,
        "secretKeyId": secret_key_id,
        "encryptedData": encrypted_data
    }
    return encrypted_message




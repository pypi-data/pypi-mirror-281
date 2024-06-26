import json
import hashlib
import base64
import base58
from typing import Dict, Any
from copy import deepcopy
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from didall.utils.did_generate import generate_bitcoin_address
from didall.utils.crypto_tool import verify_did_with_public_key, verify_signature_for_json

def extract_public_key(did_document: Dict[str, Any], key_id: str) -> ec.EllipticCurvePublicKey:
    """从DID文档中提取公钥"""
    for vm in did_document['verificationMethod']:
        if vm['id'] == key_id and vm['type'] == "EcdsaSecp256r1VerificationKey2019":
            public_key_hex = vm['publicKeyHex']
            public_key_bytes = bytes.fromhex(public_key_hex[2:])
            return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_key_bytes)
    raise ValueError(f"Public key {key_id} not found in DID document")

def verify_did_document(did_document: dict) -> (bool, str):
    """验证DID文档"""
    try:
        # 提取签名相关数据
        proof = did_document['proof']
        verification_method = proof['verificationMethod']
        signature = proof['proofValue']

        # 提取公钥
        public_key = extract_public_key(did_document, verification_method)

        # 提取did 
        did = did_document['id']

        # 验证公钥和did
        is_did_valid = verify_did_with_public_key(did, public_key)
        if not is_did_valid:
            return False, "public key is not valid"

        # 验证签名
        # 移除proof字段以获取原始消息
        original_message = deepcopy(did_document)
        del original_message['proof']['proofValue']
        is_signature_valid = verify_signature_for_json(public_key, original_message, signature)

        return is_signature_valid, "verify signature error" if not is_signature_valid else ""
    except ValueError as ve:
        return False, str(ve)
    except InvalidSignature:
        return False, "Bad Signature Error"


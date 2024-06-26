# Cross-Platform Identity Authentication and End-to-End Encrypted Communication Technology Based on DID
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: http://pi-unlimited.com
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.
# Version: 0.1.0

import unittest
import json
from didall.utils.did_generate import did_generate, sign_did_document_secp256r1
from didall.utils.did_verify import verify_did_document, extract_public_key
from cryptography.hazmat.primitives.asymmetric import ec
import logging

class TestDIDManagement(unittest.TestCase):

    def test_did_generation_and_verification(self):
        # 生成DID文档和密钥
        private_key, public_key, did, did_document_json = did_generate("wss://example.com/endpoint")
        did_document = json.loads(did_document_json)

        # 检查DID文档是否包含正确的DID
        self.assertIn(did, did_document_json)

        # 验证DID文档
        result, message = verify_did_document(did_document)
        self.assertTrue(result, msg="DID文档验证失败: " + message)

        # 测试签名功能
        signed_did_document = sign_did_document_secp256r1(private_key, did_document)
        self.assertIn('proofValue', signed_did_document['proof'], "签名未正确添加到DID文档")

        # 再次验证签名
        result, message = verify_did_document(signed_did_document)
        self.assertTrue(result, msg="重签名后的DID文档验证失败: " + message)
        logging.info("DID文档验证通过")

    def test_public_key_extraction(self):
        # 生成DID文档和密钥
        private_key, public_key, did, did_document_json = did_generate("wss://example.com/endpoint")
        did_document = json.loads(did_document_json)

        # 提取公钥
        extracted_public_key = extract_public_key(did_document, f"{did}#keys-1")
        self.assertIsInstance(extracted_public_key, ec.EllipticCurvePublicKey, "提取的公钥类型错误")

        logging.info("公钥提取成功")


if __name__ == '__main__':
    unittest.main()


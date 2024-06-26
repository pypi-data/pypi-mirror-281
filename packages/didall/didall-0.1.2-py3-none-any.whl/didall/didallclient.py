# Cross-Platform Identity Authentication and End-to-End Encrypted Communication Technology Based on DID
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: http://pi-unlimited.com
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.
# Version: 0.1.0

import logging
from typing import Tuple
import aiohttp
from didall.utils.crypto_tool import get_pem_from_private_key
from didall.utils.did_generate import did_generate
import requests

class DIDAllClient:
    def __init__(self, did_service_url: str, api_key: str):
        self.api_key = api_key
        self.did_service_url = did_service_url

    def generate_did_document(self, communication_service_endpoint: str, router_did: str = "") -> Tuple[str, str, str]:
        """
        生成DID文档, 不注册到DID服务

        Args:
            communication_service_endpoint (str): 通信服务的端点，用于DID文档。
            router (str, optional): 路由的did，默认为空字符串。

        Returns:
            Tuple[str, str, str]: 返回一个元组，包含私钥的PEM格式字符串、DID字符串和DID文档的JSON字符串。
        """
        private_key, _, did, did_document_json = did_generate(communication_service_endpoint, router_did)

        # 将私钥转换为PEM格式
        private_key_pem = get_pem_from_private_key(private_key)

        return private_key_pem, did, did_document_json

    async def generate_register_did_document(self, communication_service_endpoint: str, router_did: str = "") -> Tuple[str, str, str]:
        """
        注册DID文档到DID服务。

        本函数异步生成DID和相应的DID文档，并将其注册到配置的DID服务中。
        使用了aiohttp库来发送异步HTTP请求。

        Args:
            communication_service_endpoint (str): 通信服务的端点，用于DID文档。
            router_did (str, optional): 路由的did，默认为空字符串。

        Returns:
            Tuple[str, str, str]: 返回一个元组，包含私钥的PEM格式字符串、DID字符串和DID文档的JSON字符串。
            如果注册失败，将返回三个None。
        """

        # 生成私钥、公钥、DID和DID文档
        private_key, _, did, did_document_json = did_generate(communication_service_endpoint, router_did)

        # 将私钥转换为PEM格式
        private_key_pem = get_pem_from_private_key(private_key)

        # 准备请求头
        headers = {
            "Content-Type": "application/text",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 确保请求URL正确
        request_url = f"{self.did_service_url}/v1/did"  # 确保URL是正确的

        # 使用aiohttp发送异步POST请求
        async with aiohttp.ClientSession() as session:
            async with session.post(request_url, headers=headers, data=did_document_json) as response:
                if response.status == 200:
                    return private_key_pem, did, did_document_json
                else:
                    response_text = await response.text()
                    logging.error(f"Failed to create DID document: {response.status} {response_text}")
                    return None, None, None

    async def get_did_document(self, did: str):
        # 准备请求头
        headers = {
            "Accept": "application/text",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 构建完整的请求URL
        request_url = f"{self.did_service_url}/v1/did/{did}"

        # 使用aiohttp发送异步GET请求
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    response_text = await response.text()
                    logging.error(f"Failed to retrieve DID document: {response.status} {response_text}")
                    return None

    def register_did_document_sync(self, communication_service_endpoint: str, router: str = ""):
        # 生成私钥、公钥、DID和DID文档
        private_key, _, did, did_document_json = did_generate(communication_service_endpoint, router)

        # 将私钥转换为PEM格式
        private_key_pem = get_pem_from_private_key(private_key)

        # 准备请求头
        headers = {
            "Content-Type": "application/text",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 使用requests发送同步POST请求
        response = requests.post(f"{self.did_service_url}/v1/did", headers=headers, data=did_document_json)
        if response.status_code == 200:
            return private_key_pem, did, did_document_json
        else:
            logging.error(f"Failed to create DID document: {response.status_code} {response.text}")
            return None, None, None

    def get_did_document_sync(self, did: str):
        # 准备请求头
        headers = {
            "Accept": "application/text",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 发送同步GET请求
        response = requests.get(f"{self.did_service_url}/v1/did/{did}", headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Failed to retrieve DID document: {response.status_code} {response.text}")
            return None
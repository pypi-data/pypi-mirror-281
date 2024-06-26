# Cross-Platform Identity Authentication and End-to-End Encrypted Communication Technology Based on DID
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: http://pi-unlimited.com
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.
# Version: 0.1.0

import asyncio
import json
import logging
from typing import Callable, Tuple, Union
from didall.message_generation import generate_encrypted_message
from didall.wss_message_client import WssMessageClient
from didall.short_term_key_generater import ShortTermKeyGenerater
from didall.utils.crypto_tool import decrypt_aes_gcm_sha256, generate_random_hex

# TODO: 
# 密钥超期管理,使用的时候判断超期
# 密钥错误管理
# 发送是无法找到密钥，或者密钥过期
# 受到错误响应的时候，
class WssMessageSDK:
    def __init__(self, wss_url: str, api_key: str, routers: list[tuple[str, str]], 
                 short_term_key_callback: Callable[[tuple[str, str, str]], None]):
        '''
        初始化WssMessageSDK类。

        Args:
            wss_url (str): WebSocket服务的URL。
            api_key (str): 用于WebSocket服务的API密钥。
            routers (list[tuple[str, str]]): 路由列表，每个元组包含路由did的私钥和did文档
            short_term_key_callback (Callable[[tuple[str, str, str]], None]): 短期密钥回调函数，
                用于回调短期秘钥，元组三个字符串分别是：local did，remote did，密钥信息的JSON字符串，
                json定义同set_short_term_keys入参
        '''
        self.client = WssMessageClient(wss_url, api_key)
        self.short_term_keys: dict[str, dict] = {}
        self.short_term_keys_combined: dict[str, dict] = {}
        self.local_did_to_private_key: dict[str, str] = {}  # 增加一个字典，存储local DID和对应的私钥
        self.short_term_key_callback = short_term_key_callback
        self.short_term_key_generater_session_dict: dict[str, ShortTermKeyGenerater] = {}

    @classmethod
    async def create(cls, wss_url: str, api_key: str, routers: list[tuple[str, str]], 
                     short_term_key_callback: Callable[[tuple[str, str, str]], None]):
        """工厂方法，异步创建 WssMessageSDK 实例并注册路由"""
        instance = cls(wss_url, api_key, routers, short_term_key_callback)
        await instance.client.register_routers(routers)
        return instance

    def key_combined(self, local_did: str, remote_did: str) -> str:
        return f"{local_did}_{remote_did}"

    def insert_did_private_key(self, local_did: str, private_key_pem: str):
        """将local DID和对应的私钥插入到字典中"""
        self.local_did_to_private_key[local_did] = private_key_pem
        
    # 入参更改为json，通过json和外部通信，调用者不需要了解json的内部细节
    def set_short_term_keys(self, local_did: str, remote_did: str, secret_info_json: str):
        """
        根据JSON字符串设置短期密钥信息。短期秘钥在超期之前都可以使用，如果服务器重启，可以设置之前协商的短期密钥
        JSON字符串包含发送加密密钥、接收解密密钥、密钥ID、密钥过期时间和加密套件。

        Args:
            local_did (str): 本地DID。
            remote_did (str): 远端DID。
            secret_info_json (str): 包含密钥信息的JSON字符串。同negotiate_short_term_keys返回值
        """
        secret_info = json.loads(secret_info_json)
        secret_key_id = secret_info['secret_key_id']
        key_combined = self.key_combined(local_did, remote_did)
        self.short_term_keys_combined[key_combined] = {
            "local_did": local_did,
            "remote_did": remote_did,
            "secret_key_id": secret_key_id,
            "send_encryption_key": secret_info['send_encryption_key'],
            "receive_decryption_key": secret_info['receive_decryption_key'],
            "key_expires": secret_info['key_expires'],
            "cipher_suite": secret_info['cipher_suite']
        }
        self.short_term_keys[secret_key_id] = {
            "local_did": local_did,
            "remote_did": remote_did,
            "send_encryption_key": secret_info['send_encryption_key'],
            "receive_decryption_key": secret_info['receive_decryption_key'],
            "key_expires": secret_info['key_expires'],
            "cipher_suite": secret_info['cipher_suite']
        }

    async def negotiate_short_term_keys(self, local_did: str, 
                                        did_private_key_pem: str, 
                                        remote_did: str) -> str:
        """
        协商短期密钥并返回包含密钥信息的JSON字符串。
        如果协商成功，返回包含本地DID、远端DID和密钥信息的JSON字符串；
        如果协商失败，返回包含错误信息的JSON字符串。

        Args:
            local_did (str): 本地DID。
            did_private_key_pem (str): 本地DID的私钥，PEM格式。
            remote_did (str): 远端DID。

        Returns:
            str: 密钥信息JSON字符串。生成的JSON字段说明：
                send_encryption_key: 发送方使用的加密密钥，以十六进制字符串表示。
                receive_decryption_key: 接收方使用的解密密钥，以十六进制字符串表示。
                secret_key_id: 密钥的唯一标识符。
                key_expires: 密钥的过期时间，以Unix时间戳表示。
                cipher_suite: 使用的加密套件名称。

        备注：函数返回成功后，不再调用short_term_key_callback函数。
        """
        json_send_func = self.client.send_data  # 假设 WssMessageClient 有一个发送 JSON 消息的方法
        key_gen = ShortTermKeyGenerater(local_did, did_private_key_pem, remote_did, json_send_func, is_initiator=True)
        
        self.short_term_key_generater_session_dict[key_gen.session_id] = key_gen
        success = await key_gen.generate_short_term_key_active()
        self.short_term_key_generater_session_dict.pop(key_gen.session_id)

        if success:
            remote_did, send_encryption_key, \
            receive_decryption_key, secret_key_id, \
                key_expires, cipher_suite = key_gen.get_final_short_term_key()
            secret_info_json = json.dumps({
                "send_encryption_key": send_encryption_key.hex(),
                "receive_decryption_key": receive_decryption_key.hex(),
                "secret_key_id": secret_key_id,
                "key_expires": key_expires,
                "cipher_suite": cipher_suite
                })
            self.set_short_term_keys(local_did, remote_did, secret_info_json)
            self.short_term_key_callback(local_did, remote_did, secret_info_json)
            return secret_info_json
            
        else:
            logging.error(f"密钥协商失败: {local_did} -> {remote_did}")
            return None
        
    async def source_hello_process(self, json_data: dict):
        local_did = json_data['destinationDid'] # 受到对端的hello消息，destinationDID是本地did
        did_private_key_pem = self.local_did_to_private_key.get(local_did, None)
        if did_private_key_pem is None:
            logging.error(f"未找到本地DID对应的私钥: {local_did}")
            return
        
        remote_did = json_data['sourceDid']
        session_id = json_data['sessionId']
        json_send_func = self.client.send_data
        
        key_gen = ShortTermKeyGenerater(local_did, did_private_key_pem, 
                                        remote_did, json_send_func, 
                                        is_initiator=False, session_id=session_id)
        self.short_term_key_generater_session_dict[session_id] = key_gen
        key_gen.receive_json_message(json_data)

        success = await key_gen.generate_short_term_key_passive()
        self.short_term_key_generater_session_dict.pop(key_gen.session_id)
 
        if success:
            remote_did, send_encryption_key, \
            receive_decryption_key, secret_key_id, \
                key_expires, cipher_suite = key_gen.get_final_short_term_key()
            secret_info_json = json.dumps({
                    "send_encryption_key": send_encryption_key.hex(),
                    "receive_decryption_key": receive_decryption_key.hex(),
                    "secret_key_id": secret_key_id,
                    "key_expires": key_expires,
                    "cipher_suite": cipher_suite
                })
            self.set_short_term_keys(local_did, remote_did, secret_info_json)
            self.short_term_key_callback(local_did, remote_did, secret_info_json)
        else:
            logging.error(f"密钥协商失败: {remote_did} -> {local_did}")


    def ecrypted_message_process(self, json_data: dict):
        
        secret_key_id = json_data['secretKeyId']
        key_info = self.short_term_keys.get(secret_key_id, None)

        if key_info is None:
            logging.error(f"can not find secret Keyinfo: {secret_key_id}")
            # TODO: 后面可以发送错误消息
            return

        encrypted_data = json_data['encryptedData']
        secret_key = bytes.fromhex(key_info['receive_decryption_key'])
        try:
            plaintext = decrypt_aes_gcm_sha256(encrypted_data, secret_key)
            logging.info(f"解密消息成功: {plaintext}")
            return plaintext
        except Exception as e:
            logging.error(f"解密消息失败: {e}")
            return None

    async def recv_data(self) -> Tuple[str, str, str]:
        """异步接收数据"""
        while True:
            json_data = await self.client.receive_data()
            msg_type = json_data['type']
            if msg_type == "sourceHello":
                asyncio.create_task(self.source_hello_process(json_data))
                # TODO: 这里要记录下task。后面可能需要取消等操作
            elif msg_type in ["destinationHello", "finished"]:
                session_id = json_data['sessionId']
                if session_id in self.short_term_key_generater_session_dict:
                    self.short_term_key_generater_session_dict[session_id].receive_json_message(json_data)
                else:
                    logging.error(f"can not find session_id: {session_id}")
            elif msg_type == 'message':
                msg = self.ecrypted_message_process(json_data)
                if msg is not None:
                    return json_data['sourceDid'], json_data['destinationDid'], msg
            else:
                logging.error(f"unknown message type: {msg_type}")

    async def send_data(self, content: Union[str, bytes], source_did: str, destination_did: str):
        """
        发送加密消息。输入数据可以是str或bytes，如果是str，则转换为bytes。
        从short_term_keys_combined中获取密钥信息，使用generate_encrypted_message创建消息，并调用client方法发送数据。

        Args:
            content (Union[str, bytes]): 要发送的消息内容。
            source_did (str): 源DID。
            destination_did (str): 目的DID。

        Returns:
            None
        """
        if isinstance(content, str):
            content = content.encode('utf-8')

        key_combined = self.key_combined(source_did, destination_did)
        key_info = self.short_term_keys_combined.get(key_combined, None)
        if key_info is None:
            # TODO: 这里要做个异常处理
            logging.error(f"密钥信息不存在: {key_combined}")
            return
        secret_key_id = key_info['secret_key_id']
        data_secret = bytes.fromhex(key_info['send_encryption_key'])

        encrypted_message = generate_encrypted_message(
            version="1.0",
            message_id=generate_random_hex(16),
            source_did=source_did,
            destination_did=destination_did,
            secret_key_id=secret_key_id,
            data=content,
            data_secret=data_secret
        )

        await self.client.send_data(encrypted_message)


# 示例使用
async def main():
    sdk = await WssMessageSDK.create("wss://example.com/ws", "your_api_key", [("private_key_pem1", "did_doc1"), ("private_key_pem2", "did_doc2")], lambda x: print(f"Callback: {x}"))
    source_did, destination_did, data = await sdk.recv_data()
    print(source_did, destination_did, data)
    await sdk.negotiate_short_term_keys("did:example:local", "your_private_key_pem", "did:example:remote")

if __name__ == "__main__":
    asyncio.run(main())

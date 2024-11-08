# client
import os
import sys
root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)
from tools import getAsyKeys, AsyDecrypt, AsyEncrypt, GAS_PRICE
from tools import SymEncrypt, SymDecrypt, getSymKey
from tools import CONTRACT_ABI, CONTRACT_ADDRESS, WEB3_HTTPProvider, PRIVATE_KEY
from web3 import Web3, HTTPProvider
from charm.schemes.grpsig.groupsig_bgls04 import ShortSig
from charm.toolbox.pairinggroup import PairingGroup
from tools import deserializeGSK, store, retrieve, deserializeGPK, serializeSig
from datetime import datetime
import time

class client:
    def __init__(self, name, description):
        # 基本信息
        self.name = name
        self.descripton = description

        # 公私钥，用于非对称加密
        self.secKey, self.pubKey = getAsyKeys()

        # 以太坊私钥,用于发交易
        self.private_key = PRIVATE_KEY

        # 以太坊合约对象
        self.w3 = Web3(Web3.HTTPProvider(WEB3_HTTPProvider)) 
        self.contract = self.w3.eth.contract(address = CONTRACT_ADDRESS, abi = CONTRACT_ABI)

        # 群签名对象
        self.group = PairingGroup('MNT224')
        self.shortSig = ShortSig(self.group)
        self.gpk = None


    # 模型训练，获得模型参数omega
    def train(self):
        # 获取当前日期和时间
        now = datetime.now()

        # 格式化日期和时间
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_datetime + ' sent this message.'

    # 将文件对称加密，然后上传到DFS，并返回address和key
    def __uploadDFS(self, data):
        key = getSymKey()
        data_x = SymEncrypt(data, key)
        address = store(data_x)
        return address,key
    
    # 从DFS取数据
    def __downloadDFS(self, address, path):
        res = retrieve(address, path)
        return res


    # 将data存入DFS，得到的address和key非对称加密，然后签名，将message和sig上传到区块链上
    def dataUpload(self, data, nonce):
        address, key = self.__uploadDFS(data)
        message = AsyEncrypt(self.serverPubKey, address+key)

        sig = self.shortSig.sign(self.gpk, self.gsk, message)
        # 构建注册交易
        txn_data1 = self.contract.functions.messageUpload(message, serializeSig(self.group, sig)).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(GAS_PRICE, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        return tx_hash.hex()

    def testdataUpload(self, data, nonce):
        # 构建注册交易
        nonce = self.w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")
        txn_data1 = self.contract.functions.messageUpload('this is a message', b'hello,world').build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(GAS_PRICE, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        return tx_hash.hex()

    # 注册
    def register(self, nonce):
        
        # 构建注册交易
        txn_data1 = self.contract.functions.createClient(self.pubKey, self.name, self.descripton).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(GAS_PRICE, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        return tx_hash.hex()

    # 监听gskReturn,获取gsk
    def __monitorGskReturn(self):
        print('monitoring gskReturn')

        # 订阅事件
        event_filter = self.contract.events.gskReturn.create_filter(fromBlock='latest')

        # 监听事件
        while True:
            for entry in event_filter.get_new_entries():
                data = entry.args
                # 如果公钥和自己相同，则接受；否则继续监听
                if data['pubKey'] == self.pubKey:
                    self.gpk = deserializeGPK(self.group,data['gpk'])
                    message = data['message']
                    # 使用私钥解密message，获得addrress和key
                    temp = AsyDecrypt(self.secKey,message)
                    address = temp[:64]
                    key = temp[64:]
                    # 使用address从DFS中下载gsk,并读出密文
                    self.__downloadDFS(address, './gsk.txt')
                    with open('./gsk.txt', 'r') as f:
                        ciphertext = f.read()
                    # 将密文解密成为明文
                    plaintext = SymDecrypt(key, ciphertext)
                    # 将明文转为bytes
                    temp = plaintext.encode('utf-8')
                    self.gsk = deserializeGSK(self.group, temp)
                    print(f'received gpk:{self.gpk}, gsk:{self.gsk}')
                    return
                    
       
    
    def joinGroup(self, groupName, nonce):
        # 构建注册交易
        txn_data1 = self.contract.functions.joinGroup(groupName).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(GAS_PRICE, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        self.serverPubKey = self.contract.functions.getServerPubKey(groupName).call()

        self.__monitorGskReturn()
    
    def getGpk(self):
        return self.gpk

if __name__ == '__main__':
    print(f'client init')
    c = client('c1', 'this is c1')

    w3 = Web3(Web3.HTTPProvider(WEB3_HTTPProvider)) 
    nonce = w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")

    print(f'client register, nonce:{nonce}')
    c.register(nonce)

    print(f'client joinGroup, nonce:{nonce+1}')
    c.joinGroup('group1', nonce+1)

    # print('waiting for block confirm')
    # time.sleep()

    print('uploadData')
    nonce = w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")

    for i in range(10):
        print(f'nonce:{nonce+i}')
        data = c.train()
        c.dataUpload(data, nonce+i)
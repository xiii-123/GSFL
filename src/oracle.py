import os
import sys
root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)
from tools import CONTRACT_ABI, CONTRACT_ADDRESS, SEPOLIA_ADDRESS, serializeGSK, serializeGPK
from web3 import Web3, HTTPProvider
from tools.DFS import store
from tools import SymEncrypt, AsyEncrypt, gas_price
from charm.schemes.grpsig.groupsig_bgls04 import ShortSig
from charm.toolbox.pairinggroup import PairingGroup
import threading
import concurrent
import time

class oracle:

    # 创建一个事件对象，用于通知线程何时停止
    stop_event = threading.Event()

    def __init__(self, total = 100) -> None:
        # 以太坊合约对象
        self.w3 = Web3(Web3.HTTPProvider(SEPOLIA_ADDRESS)) 
        self.contract = self.w3.eth.contract(address = CONTRACT_ADDRESS, abi = CONTRACT_ABI)
        self.private_key = ""
        self.group = PairingGroup('MNT224')
        self.count = 0
        self.total = total
        self.serverPubKey = None

    def nextGsk(self):
        num = self.count
        if num > self.total:
            raise ValueError("群组成员数量已达到上限！")
        self.count = self.count+1
        return self.gsk[num]

    # 监听joinGroup事件，发现事件则调用uploadDFS和uploadBlockchain
    def monitorJoinGroup(self):
        print(f'monitoring joinGroup')
        # 订阅事件
        event_filter = self.contract.events.groupJoin.create_filter(fromBlock='latest')

        # 监听事件
        lock = threading.Lock()
        while True:
            for entry in event_filter.get_new_entries():
                data = entry.args
                pubKey = data['pubKey']
                print(f'{pubKey[28:92]} calls joinGroup')
                with lock:
                    gsk = self.nextGsk()
                gsk_t = serializeGSK(self.group, gsk)
                # 先将gsk_t转为str再存入DFS
                
                address, key = self.__uploadDFS(gsk_t.decode('utf-8'))
                self.__returnGsk(address, key, pubKey)

    # 监听createGroup事件，发现则创建群
    def monitorCreateGroup(self):
        print(f'monitoring createGroup')
        # 订阅事件
        event_filter = self.contract.events.groupCreate.create_filter(fromBlock='latest')

        # 监听事件
        while True:
            for entry in event_filter.get_new_entries():
                data = entry.args
                pubKey = data['pubKey']
                print(f'{pubKey[28:92]} calls createGroup')
                self.serverPubKey = pubKey
                self.shortSig = ShortSig(self.group)
                self.gpk,self.gmsk,self.gsk = self.shortSig.keygen(self.total)
                self.__returnGpk(pubKey)
                print(f'group created')
    
    def __uploadDFS(self, data):
        data_x,key = SymEncrypt(data)
        address = store(data_x)
        return address,key

    # 发送交易，向client返回gsk,gpk
    def __returnGsk(self, address, key, pubKey):
        print(f'calls returnGsk')
        message = AsyEncrypt(pubKey, address+key)

        # 构建注册交易
        nonce = self.w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")
        txn_data1 = self.contract.functions.returnGsk(message, pubKey, serializeGPK(self.group, self.gpk)).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(gas_price, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        return tx_hash.hex()
    
    # 发送交易,向server返回gpk
    def __returnGpk(self, pubKey):
        print(f'calls returnGpk')
        # 构建注册交易
        nonce = self.w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")
        txn_data1 = self.contract.functions.returnGpk(pubKey, serializeGPK(self.group, self.gpk)).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(gas_price, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        return tx_hash.hex()
    
    def start(self, num=2):
        # 多线程运行
        with concurrent.futures.ThreadPoolExecutor(max_workers=num) as executor:
            # 提交线程函数到线程池
            executor.submit(self.monitorCreateGroup)
            executor.submit(self.monitorJoinGroup)

        print("Oracle is running...")
        try:
            while not self.stop_event.is_set():
                time.sleep(2)
        except KeyboardInterrupt:
            print("Oracle is interrupted.")
            self.stop_event.set()
    
if __name__ == '__main__':
    o = oracle()
    o.start()
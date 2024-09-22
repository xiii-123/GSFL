# server
import os
import sys
root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)
from tools import getAsyKeys, AsyDecrypt, AsyEncrypt, deserializeSig, deserializeGPK
from tools import SymEncrypt, SymDecrypt, gas_price
from tools.DFS import store, retrieve
from tools import CONTRACT_ABI, CONTRACT_ADDRESS, SEPOLIA_ADDRESS
from web3 import Web3, HTTPProvider
from charm.schemes.grpsig.groupsig_bgls04 import ShortSig
from charm.toolbox.pairinggroup import PairingGroup
import threading
import time
import concurrent.futures
from datetime import datetime

class server:

    lock = threading.Lock()

    def __init__(self, name, description, paramsDir = '.'):
        # 基本信息
        self.name = name
        self.descripton = description
        self.paramsDir = paramsDir

        # 公私钥，用于非对称加密
        self.secKey, self.pubKey = getAsyKeys()

        # 以太坊私钥,用于发交易
        self.private_key = ""

        # 以太坊合约对象
        self.w3 = Web3(Web3.HTTPProvider(SEPOLIA_ADDRESS)) 
        self.contract = self.w3.eth.contract(address = CONTRACT_ADDRESS, abi = CONTRACT_ABI)

        # 群签名对象
        self.group = PairingGroup('MNT224')
        self.shortSig = ShortSig(self.group)

        self.count = 0

    # 注册
    def register(self, nonce):
        # 构建注册交易
        txn_data1 = self.contract.functions.createServer(self.pubKey, self.name, self.descripton).build_transaction({
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
    
    def createGroup(self, name, descripton, nonce):
        # 构建交易
        txn_data1 = self.contract.functions.createGroup(name, descripton).build_transaction({
            'from': "0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0",
            'gas': 2000000,  # 根据情况调整 gas 限制
            'gasPrice': self.w3.to_wei(gas_price, 'gwei'),
            'nonce': nonce,
        })

        # 对交易进行签名
        signed_txn1 = self.w3.eth.account.sign_transaction(txn_data1, self.private_key)

        # 发送签名后的交易
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn1.rawTransaction)

        self.__MonitorGpkReturn()

        return tx_hash.hex()
    
    def __MonitorGpkReturn(self):
        # 订阅事件
        event_filter = self.contract.events.gpkReturn.create_filter(fromBlock='latest')

        # 监听事件
        # 监听事件
        while True:
            for entry in event_filter.get_new_entries():
                data = entry.args
                # 如果公钥和自己相同，则接受；否则继续监听
                if data['pubKey'] == self.pubKey:
                    self.gpk = deserializeGPK(self.group, data['gpk'])
                    print(f'recieved gpk:{self.gpk}')
                    return

    # 将收集到的模型参数聚合更新,得到新模型
    def train(self):
        print(f'model update!')

    # 创建一个事件对象，用于通知线程何时停止
    stop_event = threading.Event()

    # 监听messageArrived事件,返回message
    def monitorDataArrived(self, num=2):
        # 多线程运行
        # with concurrent.futures.ThreadPoolExecutor(max_workers=num) as executor:
        #     # 使用 map 方法将任务并行化
        #     # map 方法会自动分配任务到线程池中的线程
        #     executor.submit(self.__threadFunc)

        #     try:
        #         while not self.stop_event.is_set():
        #             time.sleep(2)
        #     except KeyboardInterrupt:
        #         print("Server is interrupted.")
        #         self.stop_event.set()
        self.__threadFunc()

    # 线程函数，用来监听messageArrived事件，并且将得到的结果加入dataset
    def __threadFunc(self):
        print("Server is running...")
        # 订阅事件
        event_filter = self.contract.events.messageArrived.create_filter(fromBlock='latest')

        # 监听事件
        while True:
            for entry in event_filter.get_new_entries():
                print(f'received message')
                data = entry.args
                # 如果sig验证成功，则接受；否则继续监听
                if self.shortSig.verify(self.gpk, data['message'], deserializeSig(self.group,data['sig'])) == True:
                    print(f'message verified')
                    message = data['message']
                    # 使用私钥解密message，获得addrress和key
                    temp = AsyDecrypt(self.secKey,message)
                    address = temp[:64]
                    key = temp[64:]
                    # 从DFS中取出文件并读出内容
                    retrieve(address, './temp.txt')
                    with open('./temp.txt', 'rb') as f:
                        temp = f.read()
                    os.remove('./temp.txt')

                    # 将密文解密并写入文件
                    with self.lock:
                        num = self.count
                        self.count = self.count+1
                    plaintext = SymDecrypt(temp, key)
                    with open(self.paramsDir+'/model_param-'+str(num)+'.pth', 'wb') as f:
                        f.write(plaintext)
                    # 获取当前时间
                    current_time = datetime.now().time()

                    # 输出当前时间
                    print(f'received file on {current_time}')
                    

    
if __name__ == '__main__':
    print('server init')
    s = server('server1', 'this is server1','./paramDir')

    w3 = Web3(Web3.HTTPProvider(SEPOLIA_ADDRESS)) 
    nonce = w3.eth.get_transaction_count("0xD842076A53CFE48DeE2F63Fab5BFEd66cBE4CBe0")

    print('server register')
    print(s.register(nonce))
    
    print('server createGroup')
    print(s.createGroup('group1', 'this is group1', nonce+1))

    print('server monitorDataArrived')
    s.monitorDataArrived()

from .asym_encryption import getAsyKeys, AsyDecrypt, AsyEncrypt
from .bbs_sig import serializeGPK, deserializeGPK, serializeGSK, deserializeGSK, serializeSig, deserializeSig
from .sym_encryption import SymDecrypt, SymEncrypt, getSymKey
from .DFS import store, retrieve
from .w3tools import parse_data

CONTRACT_ADDRESS = '0xF5CE3a021C55FEc750F52d06A4a0F995862f3692'

# 合约ABI
CONTRACT_ABI = '[{"inputs":[{"internalType":"string","name":"_pubKey","type":"string"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_description","type":"string"}],"name":"createClient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_description","type":"string"}],"name":"createGroup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_pubKey","type":"string"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_description","type":"string"}],"name":"createServer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"pubKey","type":"string"},{"indexed":false,"internalType":"bytes","name":"gpk","type":"bytes"}],"name":"gpkReturn","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"pubKey","type":"string"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"string","name":"description","type":"string"}],"name":"groupCreate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"pubKey","type":"string"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"string","name":"description","type":"string"}],"name":"groupJoin","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"string","name":"pubKey","type":"string"},{"indexed":false,"internalType":"bytes","name":"gpk","type":"bytes"}],"name":"gskReturn","type":"event"},{"inputs":[{"internalType":"string","name":"_groupName","type":"string"}],"name":"joinGroup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"bytes","name":"sig","type":"bytes"}],"name":"messageArrived","type":"event"},{"inputs":[{"internalType":"string","name":"_message","type":"string"},{"internalType":"bytes","name":"_sig","type":"bytes"}],"name":"messageUpload","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_pubKey","type":"string"},{"internalType":"bytes","name":"_gpk","type":"bytes"}],"name":"returnGpk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_message","type":"string"},{"internalType":"string","name":"_pubKey","type":"string"},{"internalType":"bytes","name":"_gpk","type":"bytes"}],"name":"returnGsk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGroups","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"components":[{"internalType":"string","name":"pubKey","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"}],"internalType":"structServerClientGroupSystem.Server","name":"server","type":"tuple"},{"internalType":"address[]","name":"clientList","type":"address[]"}],"internalType":"structServerClientGroupSystem.Group[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_groupName","type":"string"}],"name":"getServer","outputs":[{"components":[{"internalType":"string","name":"pubKey","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"}],"internalType":"structServerClientGroupSystem.Server","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_groupName","type":"string"}],"name":"getServerPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'

# 以太坊节点地址
WEB3_HTTPProvider = ''

GAS_PRICE = ''

PRIVATE_KEY = ''
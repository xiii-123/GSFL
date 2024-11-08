import json
import hashlib
import os
import shutil
import time
import random
# JSON文件路径
# 获取当前文件的绝对路径
current_path = os.path.abspath(__file__)

# 获取当前文件的父路径
parent_path = os.path.dirname(current_path)
DFS_path = os.path.dirname(parent_path)+'/DFS'
filename_path = DFS_path+'/filename.json'
# json_file_path = './data.json'

def simulate_ipfs_transfer(file_size, rtt_variation_percentage=0.1, bandwidth_variation_percentage=0.1):
    """
    模拟IPFS传输文件的时延。

    :param file_size_bytes: 文件大小（字节）
    :param network_bandwidth_mbps: 网络带宽（兆比特每秒）
    :param base_rtt_ms: 基础往返时间（毫秒）
    :param node_performance: 节点性能（0到1之间，1表示最佳性能）
    :param popularity: 文件受欢迎程度（0到1之间，1表示非常受欢迎）
    :param dht_efficiency: DHT效率（0到1之间，1表示最佳效率）
    :param encryption_overhead: 加密和验证开销（毫秒）
    :param network_conditions: 网络条件（0到1之间，1表示最佳条件）
    :param rtt_variation_percentage: RTT波动的百分比
    :param bandwidth_variation_percentage: 带宽波动的百分比
    :return: 传输时间（毫秒）
    """
    file_size_bytes = file_size * 1024 * 1024  # 转换为字节
    network_bandwidth_mbps = 100  # 网络带宽100Mbps
    base_rtt_ms = 50  # 基础RTT 50ms
    encryption_overhead = 20  # 加密和验证开销20ms

    # 假设其他因素在一般情况下的波动范围
    node_performance = random.uniform(0.5, 0.6)  # 节点性能在一般到最佳之间
    popularity = random.uniform(0.3, 0.4)  # 文件受欢迎程度在一般到非常受欢迎之间
    dht_efficiency = random.uniform(0.6, 0.7)  # DHT效率在一般到最佳之间
    network_conditions = random.uniform(0.7, 0.8)  # 网络条件在一般到最佳之间
    
    # 随机波动网络带宽
    network_bandwidth_mbps *= (1 + random.uniform(-bandwidth_variation_percentage, bandwidth_variation_percentage))
    
    # 将文件大小从字节转换为比特
    file_size_bits = file_size_bytes * 8
    
    # 将网络带宽从兆比特每秒转换为比特每毫秒
    network_bandwidth_bits_per_ms = network_bandwidth_mbps * 1_000_000 / 1_000
    
    # 节点性能影响传输速度
    content_transfer_time_ms = file_size_bits / network_bandwidth_bits_per_ms * (1 - node_performance)
    
    # 随机波动RTT
    rtt_ms = base_rtt_ms * (1 + random.uniform(-rtt_variation_percentage, rtt_variation_percentage))
    
    # DHT效率影响查找速度
    dht_lookup_time_ms = 100 * (1 - dht_efficiency)  # 假设基础DHT查找时间为100ms
    
    # 文件受欢迎程度影响查找速度
    popularity_effect_ms = 100 * (1 - popularity)  # 假设受欢迎程度影响最多100ms
    
    # 网络条件影响整体传输时间
    network_conditions_effect_ms = (content_transfer_time_ms + rtt_ms + dht_lookup_time_ms + popularity_effect_ms) * (1 - network_conditions)
    
    # 总传输时间包括内容传输时间、RTT、DHT查找时间、受欢迎程度影响和网络条件影响
    total_time_ms = content_transfer_time_ms + rtt_ms + dht_lookup_time_ms + popularity_effect_ms + network_conditions_effect_ms + encryption_overhead

    res = int(total_time_ms/1000)
    
    return res


def store(path: str) -> str:
    """
    输入文件名，将其存储至DFS，且在filename.json中记录哈希值到文件名的映射
    """
    # 睡眠，模拟DFS延迟
    # time.sleep(simulate_ipfs_transfer(os.path.getsize(path)))

    # 构造filename，date_time+文件名
    current_timestamp = time.time()  # 获取当前时间的浮点数timestamp
    milliseconds = int(current_timestamp * 1000)  # 将timestamp转换为毫秒
    prefix = milliseconds % 10000000000  # 获取后10位数字
    filename = path.split('/')[-1]
    filename = str(prefix)+'-'+filename

    # 将文件复制到DFS目录
    shutil.copy(path, DFS_path+'/'+filename)

    # 计算字符串的哈希值
    data_hash = hashlib.sha256(filename.encode()).hexdigest()
    
    # 读取现有JSON数据
    if os.path.exists(filename_path):
        with open(filename_path, 'r') as f:
            s = f.read()
            s = '{}' if len(s) == 0 else s
            json_data = json.loads(s)
    else:
        json_data = {}
    
    # 添加或更新键值对
    json_data[data_hash] = filename
    
    # 将更新后的数据写回文件
    with open(filename_path, 'w') as f:
        json.dump(json_data, f)
    return data_hash

def retrieve(address: str, path) -> bool:
    """
    根据地址，将文件复制到指定路径
    """
    # 睡眠，模拟DFS延迟
    # time.sleep(simulate_ipfs_transfer(os.path.getsize(path)))

    # 读取文件内容
    with open(filename_path, 'r') as file:
        store_data_json = file.read()
    
    # 将JSON格式数据转换为字典
    store_data = json.loads(store_data_json)

    
    # 检查是否有匹配的键
    if address in store_data:
        value = store_data[address]
        shutil.copy(DFS_path+'/'+value, path)
        return True

    else:
        return False

if __name__ == '__main__':
    key = store('test.txt')
    # retrieve('6fafb94276516b2b83709a810487f90f81880be691c7d85b05f72f2e8520b816', 'test.txt')
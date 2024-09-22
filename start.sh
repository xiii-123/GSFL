#!/bin/bash

# 获取当前目录的路径
dfs_path=$(pwd)/DFS

# 检查config.yml文件是否存在
if [ -f "config.yml" ]; then
    # 删除已有的DFS-path配置（如果存在）
    sed -i '/^DFS_path:/d' config.yml
    
    # 将当前目录路径添加到config.yml文件中
    echo "DFS_path: \"$dfs_path\"" >> config.yml
    echo "DFS directory path has been added to config.yml as DFS_path."
else
    # 如果config.yml文件不存在，则创建一个新的文件并添加DFS-path
    echo "DFS_path: \"$dfs_path\"" > config.yml
    echo "config.yml has been created with DFS-path set to the DFS directory."
fi

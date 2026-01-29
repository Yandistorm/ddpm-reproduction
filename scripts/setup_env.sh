#!/bin/bash
# Linux/服务器环境快速设置脚本

echo "========================================"
echo "DDPM环境设置脚本"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

python3 --version

# 创建虚拟环境
echo ""
echo "[1/4] 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "虚拟环境创建成功"
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "[2/4] 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo ""
echo "[3/4] 升级pip..."
pip install --upgrade pip

# 安装依赖
echo ""
echo "[4/4] 安装依赖包..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "环境设置完成！"
echo "========================================"
echo ""
echo "下一步:"
echo "1. 准备数据集到 ./data/images 目录"
echo "2. 运行测试: python scripts/test_model.py"
echo "3. 开始训练: python train.py"
echo ""

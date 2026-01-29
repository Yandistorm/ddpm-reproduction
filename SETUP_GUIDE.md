# DDPM复现完整准备指南

## 📋 准备清单

### 本地Windows环境准备

**注意：如果你的显卡是AMD（如6650XT），PyTorch对AMD的支持有限：**
- Windows上可以用DirectML，但性能不如NVIDIA
- 建议本地只做代码测试，实际训练在服务器（NVIDIA GPU）上进行

#### 1. 环境安装（5-10分钟）

**标准安装（NVIDIA GPU或服务器用）：**
```bash
# 方法1: 使用自动化脚本（推荐）
scripts\setup_env.bat

# 方法2: 手动安装
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**AMD显卡安装（本地测试用）：**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements_amd.txt
```

#### 2. 测试环境（1分钟）

```bash
# 激活虚拟环境
venv\Scripts\activate

# NVIDIA GPU / 服务器测试
python scripts\test_model.py

# AMD GPU / CPU测试
python scripts\test_amd.py
```

#### 3. 准备数据集

**选项A: 使用CIFAR-10（快速测试）**
```bash
python scripts\download_cifar10.py
```

**选项B: 使用自定义数据集**
```
1. 创建目录: mkdir data\images
2. 将你的训练图片放入 data\images 文件夹
3. 支持格式: jpg, png, jpeg等
4. 建议: 至少1000张图片，图片尺寸一致
```

#### 4. 本地测试训练（可选）

```bash
# 修改train.py中的参数进行小规模测试
# 建议设置: TRAIN_STEPS = 1000, BATCH_SIZE = 4
python train.py
```

### 推送到GitHub

#### 1. 初始化Git仓库（如果还没有）

```bash
git init
git add .
git commit -m "Initial commit: DDPM复现项目"
```

#### 2. 创建GitHub仓库

1. 访问 https://github.com/new
2. 创建新仓库（例如: ddpm-reproduction）
3. 不要初始化README（因为本地已有）

#### 3. 推送代码

```bash
git remote add origin https://github.com/你的用户名/ddpm-reproduction.git
git branch -M main
git push -u origin main
```

**注意**: 
- 数据集不会被推送（已在.gitignore中排除）
- 训练结果不会被推送（已在.gitignore中排除）

### 服务器环境准备

#### 1. 登录服务器

```bash
ssh 用户名@服务器IP
```

#### 2. 克隆代码

```bash
git clone https://github.com/你的用户名/ddpm-reproduction.git
cd ddpm-reproduction
```

#### 3. 安装环境

```bash
# 使用自动化脚本
bash scripts/setup_env.sh

# 或手动安装
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. 上传数据集到服务器

**方法1: 从本地上传（Windows）**
```bash
# 使用scp（需要安装OpenSSH或使用Git Bash）
scp -r data/images 用户名@服务器IP:/path/to/ddpm-reproduction/data/

# 或使用WinSCP等图形化工具
```

**方法2: 在服务器上下载**
```bash
# 如果数据集有公开下载链接
cd data
wget 数据集下载链接
unzip 数据集.zip -d images/
```

**方法3: 使用云存储**
```bash
# 例如使用阿里云OSS、腾讯云COS等
# 先上传到云存储，再从服务器下载
```

#### 5. 测试环境

```bash
source venv/bin/activate
python scripts/test_model.py
```

#### 6. 开始训练

**单GPU训练**
```bash
python train.py
```

**多GPU训练（推荐）**
```bash
# 首次配置
accelerate config
# 按提示选择: 多GPU、GPU数量等

# 启动训练
accelerate launch train.py
```

#### 7. 后台运行（推荐）

```bash
# 使用nohup
nohup python train.py > train.log 2>&1 &

# 或使用screen
screen -S ddpm_train
python train.py
# 按 Ctrl+A+D 退出screen
# 重新连接: screen -r ddpm_train

# 或使用tmux
tmux new -s ddpm_train
python train.py
# 按 Ctrl+B+D 退出tmux
# 重新连接: tmux attach -t ddpm_train
```

## 📊 训练监控

### 查看训练进度

```bash
# 查看日志
tail -f train.log

# 查看生成的样本
ls -lh results/
```

### 从本地查看结果

```bash
# 下载生成的样本到本地
scp 用户名@服务器IP:/path/to/ddpm-reproduction/results/*.png ./local_results/
```

## ⚙️ 配置调整建议

### 根据显存调整参数

| 显存大小 | IMAGE_SIZE | BATCH_SIZE | 建议 |
|---------|-----------|-----------|------|
| 8GB     | 64        | 32        | 基础配置 |
| 12GB    | 128       | 16        | 标准配置 |
| 16GB    | 128       | 32        | 推荐配置 |
| 24GB+   | 256       | 16        | 高质量配置 |

### 快速测试配置

在 `train.py` 中修改:
```python
TRAIN_STEPS = 10000  # 快速测试
CALCULATE_FID = False  # 关闭FID计算
BATCH_SIZE = 8  # 减小批次
```

### 生产训练配置

```python
TRAIN_STEPS = 700000  # 完整训练
CALCULATE_FID = True  # 开启FID评估
BATCH_SIZE = 32  # 根据显存调整
AMP = True  # 混合精度加速
```

## 🔧 常见问题

### 1. CUDA out of memory
- 减小 `BATCH_SIZE`
- 减小 `IMAGE_SIZE`
- 关闭 `CALCULATE_FID`

### 2. 训练速度慢
- 使用多GPU: `accelerate launch train.py`
- 开启混合精度: `AMP = True`
- 增大批次大小（如果显存允许）

### 3. 数据集太大无法上传
- 使用云存储中转
- 在服务器上直接下载
- 使用rsync增量同步

### 4. SSH连接断开导致训练中断
- 使用 `screen` 或 `tmux`
- 使用 `nohup` 后台运行

## 📝 检查清单

### 本地准备
- [ ] Python环境安装完成
- [ ] 依赖包安装成功
- [ ] 模型测试通过
- [ ] 数据集准备完成
- [ ] 代码推送到GitHub

### 服务器准备
- [ ] 代码克隆成功
- [ ] 虚拟环境创建
- [ ] 依赖安装完成
- [ ] 数据集上传完成
- [ ] GPU可用性确认
- [ ] 测试运行通过

### 开始训练
- [ ] 配置参数检查
- [ ] 后台运行设置
- [ ] 日志监控配置
- [ ] 定期检查训练进度

## 🎯 预期时间

- 本地环境准备: 10-20分钟
- 数据集准备: 根据数据集大小，10分钟-数小时
- 服务器环境准备: 10-30分钟
- 数据集上传: 根据网速和大小，10分钟-数小时
- 训练时间: 根据配置，数小时-数天

## 📚 参考资源

- [DDPM原始论文](https://arxiv.org/abs/2006.11239)
- [Hugging Face教程](https://huggingface.co/blog/annotated-diffusion)
- [Accelerate文档](https://huggingface.co/docs/accelerate)

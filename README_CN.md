# DDPM论文复现项目

这是基于 [denoising-diffusion-pytorch](https://github.com/lucidrains/denoising-diffusion-pytorch) 的DDPM论文复现项目。

## 环境准备

### 1. 本地Windows环境

```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 或者直接安装包
pip install -e .
```

### 2. 准备数据集

将训练图片放在 `./data/images` 目录下，支持常见图片格式（jpg, png等）。

```
data/
└── images/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

### 3. 本地测试训练

```bash
# 单GPU训练
python train.py

# 如果需要修改配置，编辑 train.py 中的参数
```

## 服务器训练

### 1. 推送到GitHub

```bash
git add .
git commit -m "准备DDPM训练环境"
git push origin main
```

### 2. 在服务器上克隆

```bash
# SSH登录服务器后
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 上传数据集到服务器

```bash
# 方法1: 使用scp从本地上传
scp -r ./data/images 用户名@服务器IP:/path/to/project/data/

# 方法2: 在服务器上直接下载数据集
# 根据你的数据集来源进行下载
```

### 4. 多GPU训练（推荐）

```bash
# 配置accelerate
accelerate config

# 启动训练
accelerate launch train.py
```

### 5. 单GPU训练

```bash
python train.py
```

## 训练监控

训练过程中会在 `./results` 目录下保存：
- 模型检查点（checkpoint）
- 生成的样本图片
- 训练日志

## 配置说明

主要参数在 `train.py` 中：
- `IMAGE_SIZE`: 图片尺寸（默认128）
- `BATCH_SIZE`: 批次大小（根据显存调整）
- `TRAIN_STEPS`: 训练步数（默认700000）
- `LEARNING_RATE`: 学习率（默认8e-5）
- `DATA_PATH`: 数据集路径

## 常见问题

### 显存不足
- 减小 `BATCH_SIZE`
- 减小 `IMAGE_SIZE`
- 关闭 `CALCULATE_FID`
- 关闭 `AMP`（混合精度）

### 训练速度慢
- 使用多GPU训练（accelerate）
- 开启 `AMP`（混合精度）
- 增大 `BATCH_SIZE`（如果显存允许）

## 参考

- 原始论文: [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- 代码库: [denoising-diffusion-pytorch](https://github.com/lucidrains/denoising-diffusion-pytorch)

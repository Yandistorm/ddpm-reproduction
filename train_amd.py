"""
AMD显卡/CPU训练脚本（Windows DirectML）
适用于AMD显卡或CPU训练

使用方法:
    python train_amd.py
"""
import torch
import torch_directml  # AMD GPU支持
from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer

# 检测设备
if torch_directml.is_available():
    device = torch_directml.device()
    print(f"使用DirectML设备（AMD GPU）")
else:
    device = torch.device('cpu')
    print(f"使用CPU训练（会比较慢）")

# 配置参数 - AMD显卡/CPU建议使用较小的配置
IMAGE_SIZE = 64  # 降低图片尺寸
BATCH_SIZE = 4   # 小批次
TRAIN_STEPS = 10000  # 测试用，完整训练建议在服务器
LEARNING_RATE = 8e-5
GRADIENT_ACCUMULATE_EVERY = 2
EMA_DECAY = 0.995
AMP = False  # DirectML可能不支持混合精度
CALCULATE_FID = False  # 关闭FID计算以节省资源

# 数据路径
DATA_PATH = './data/images'

print(f"\n训练配置:")
print(f"  图片尺寸: {IMAGE_SIZE}x{IMAGE_SIZE}")
print(f"  批次大小: {BATCH_SIZE}")
print(f"  训练步数: {TRAIN_STEPS}")
print(f"  设备: {device}")
print(f"\n注意: AMD显卡训练速度会比NVIDIA慢，建议用于测试")
print(f"      完整训练建议在配有NVIDIA GPU的服务器上进行\n")

# 模型定义
model = Unet(
    dim=64,
    dim_mults=(1, 2, 4),  # 减少层数
    flash_attn=False
)

# 扩散模型
diffusion = GaussianDiffusion(
    model,
    image_size=IMAGE_SIZE,
    timesteps=1000,
    sampling_timesteps=250
)

# 训练器
trainer = Trainer(
    diffusion,
    DATA_PATH,
    train_batch_size=BATCH_SIZE,
    train_lr=LEARNING_RATE,
    train_num_steps=TRAIN_STEPS,
    gradient_accumulate_every=GRADIENT_ACCUMULATE_EVERY,
    ema_decay=EMA_DECAY,
    amp=AMP,
    calculate_fid=CALCULATE_FID,
    results_folder='./results',
    save_and_sample_every=500,
)

if __name__ == '__main__':
    print("开始训练...")
    trainer.train()

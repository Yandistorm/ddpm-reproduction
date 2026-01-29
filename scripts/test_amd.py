"""
测试AMD显卡/CPU环境
"""
import torch

print("PyTorch版本:", torch.__version__)

# 测试DirectML
try:
    import torch_directml
    if torch_directml.is_available():
        device = torch_directml.device()
        print("✓ DirectML可用（AMD GPU支持）")
        print(f"  设备: {device}")
        
        # 简单测试
        x = torch.randn(2, 3, 64, 64).to(device)
        print(f"  测试张量: {x.shape}")
        print("✓ AMD GPU可以正常使用")
    else:
        print("✗ DirectML不可用")
        device = torch.device('cpu')
        print(f"  将使用CPU: {device}")
except ImportError:
    print("✗ torch-directml未安装")
    print("  安装命令: pip install torch-directml")
    device = torch.device('cpu')
    print(f"  将使用CPU: {device}")

# 测试基本功能
print("\n测试基本PyTorch功能...")
from denoising_diffusion_pytorch import Unet, GaussianDiffusion

model = Unet(
    dim=64,
    dim_mults=(1, 2, 4),
    flash_attn=False
)

diffusion = GaussianDiffusion(
    model,
    image_size=64,
    timesteps=100  # 减少步数用于测试
)

print("✓ 模型创建成功")

# 测试前向传播
training_images = torch.rand(2, 3, 64, 64)
loss = diffusion(training_images)
print(f"✓ 前向传播成功，Loss: {loss.item():.4f}")

print("\n环境测试完成！")
print("\n建议:")
if 'directml' in str(device):
    print("- AMD GPU可用，但训练速度会比NVIDIA慢")
    print("- 适合小规模测试和实验")
    print("- 完整训练建议在NVIDIA GPU服务器上进行")
else:
    print("- 当前使用CPU训练，速度会很慢")
    print("- 仅适合代码测试")
    print("- 实际训练强烈建议在GPU服务器上进行")

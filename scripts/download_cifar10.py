"""
下载CIFAR-10数据集并转换为图片格式
"""
import os
from torchvision import datasets
from PIL import Image
from tqdm import tqdm

def download_and_extract_cifar10(output_dir='./data/images'):
    """下载CIFAR-10并保存为图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("正在下载CIFAR-10数据集...")
    dataset = datasets.CIFAR10(root='./data/cifar10', train=True, download=True)
    
    print(f"正在提取图片到 {output_dir}...")
    for idx, (img, label) in enumerate(tqdm(dataset)):
        img.save(os.path.join(output_dir, f'cifar10_{idx:05d}.png'))
    
    print(f"完成！共提取 {len(dataset)} 张图片")

if __name__ == '__main__':
    download_and_extract_cifar10()

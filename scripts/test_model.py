"""
Test if model can run properly
"""
import torch
from denoising_diffusion_pytorch import Unet, GaussianDiffusion

def test_model():
    print("Testing model initialization...")
    
    # Create model
    model = Unet(
        dim=64,
        dim_mults=(1, 2, 4, 8),
        flash_attn=False
    )
    
    diffusion = GaussianDiffusion(
        model,
        image_size=128,
        timesteps=1000
    )
    
    print("Model created successfully!")
    
    # Test forward pass
    print("Testing forward pass...")
    batch_size = 2
    training_images = torch.rand(batch_size, 3, 128, 128)
    
    loss = diffusion(training_images)
    print(f"Loss: {loss.item():.4f}")
    
    # Test sampling
    print("Testing sampling...")
    sampled_images = diffusion.sample(batch_size=2)
    print(f"Sampled image shape: {sampled_images.shape}")
    
    print("\n✓ All tests passed! Model is working properly.")

if __name__ == '__main__':
    test_model()

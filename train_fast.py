"""
Fast training for small dataset (391 images)
Optimized for quick results
"""
import torch
from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer

# Fast training configuration
IMAGE_SIZE = 128
BATCH_SIZE = 32  # Increased batch size
TRAIN_STEPS = 20000  # Reduced from 700000
LEARNING_RATE = 1e-4  # Slightly higher LR
GRADIENT_ACCUMULATE_EVERY = 1  # No accumulation
EMA_DECAY = 0.995
AMP = True
CALCULATE_FID = False  # Disabled for speed

DATA_PATH = './data/images'

model = Unet(
    dim=64,
    dim_mults=(1, 2, 4, 8),
    flash_attn=False
)

diffusion = GaussianDiffusion(
    model,
    image_size=IMAGE_SIZE,
    timesteps=1000,
    sampling_timesteps=100  # Reduced from 250 for faster sampling
)

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
    save_and_sample_every=500,  # Save more frequently
)

if __name__ == '__main__':
    print("Fast training mode:")
    print(f"  Steps: {TRAIN_STEPS}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Sampling steps: 100")
    print(f"  Save every: 500 steps")
    trainer.train()

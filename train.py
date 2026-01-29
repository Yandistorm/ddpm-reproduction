"""
DDPM Training Script
Usage:
    Single GPU: python train.py
    Multi GPU: accelerate config then accelerate launch train.py
"""
import torch
from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer

# Configuration
IMAGE_SIZE = 128
BATCH_SIZE = 16
TRAIN_STEPS = 700000
LEARNING_RATE = 8e-5
GRADIENT_ACCUMULATE_EVERY = 2
EMA_DECAY = 0.995
AMP = True  # Mixed precision training
CALCULATE_FID = True  # Calculate FID metric

# Data path - modify to your dataset path
DATA_PATH = './data/images'

# Model definition
model = Unet(
    dim=64,
    dim_mults=(1, 2, 4, 8),
    flash_attn=False  # Set to True if GPU supports it
)

# Diffusion model
diffusion = GaussianDiffusion(
    model,
    image_size=IMAGE_SIZE,
    timesteps=1000,
    sampling_timesteps=250  # DDIM for faster sampling
)

# Trainer
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
    save_and_sample_every=1000,  # Save every 1000 steps
)

if __name__ == '__main__':
    trainer.train()

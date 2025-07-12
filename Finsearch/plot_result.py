import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

npz = 'sb3_logs/evaluations.npz'

data = np.load(npz)

print("Keys in evaluations.npz:")
for key in data.files:
    print(f"  {key}: shape {data[key].shape}")


plt.figure(figsize=(15, 5))
  
timestep = data['timesteps']
mean_rewards = np.mean(data['results'],axis=1)
std_rewards = np.std(data['results'], axis=1)

plt.plot(timestep, mean_rewards, label="Mean Reward")
# This 'fill_between' function creates the confidence interval band.
plt.fill_between(timestep, mean_rewards - std_rewards, mean_rewards + std_rewards, alpha=0.2, color='blue', label="Standard Deviation")

plt.tight_layout()
plt.show()
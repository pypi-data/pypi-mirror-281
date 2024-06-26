import matplotlib.pyplot as plt
import jsonlines as json
import numpy as np
from scipy.ndimage import uniform_filter1d

# Load data from log.jsonl
with open('log.jsonl', 'r') as f:
    data = list(json.Reader(f))

# Extract losses and epochs
losses = [entry['loss'] for entry in data]
epochs = [entry['epoch'] for entry in data]

# Compute moving average (smoothing)
window_size = 10  # Adjust the window size as needed
smoothed_losses = uniform_filter1d(losses, size=window_size)

# Plot the original loss
plt.figure(figsize=(10, 6))
plt.plot(epochs, losses, label='Loss', color='b')

# Plot the smoothed loss
plt.plot(epochs, smoothed_losses, label='Smoothed Loss', color='r', linestyle='--')

# Add title and labels
plt.title('Loss Function over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# Add grid and legend
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

# Save the plot
plt.savefig('loss_vs_epoch.png')

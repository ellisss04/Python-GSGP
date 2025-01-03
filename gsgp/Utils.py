import numpy as np
import pandas as pd


# Define the target function
def target_function(x):
    return x**3 + x**2 + x


def sym_reg_generator():
    # Generate input values
    x_values = np.arange(-1.0, 1.0, 0.1)  # Range [-1.0, 1.0] with step size 0.1
    y_values = target_function(x_values)

    noise = np.random.normal(0, 0.1, len(y_values))  # Noise with mean 0 and std 0.1
    y_noisy = y_values + noise

    dataset = pd.DataFrame({'x': x_values, 'y': y_noisy})

    return dataset

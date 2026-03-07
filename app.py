import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from clt_engine import generate_population, get_sample_means

st.title("Central Limit Theorem Simulator")
# 1. Define the options
options = [
    'Uniform U(0, 1)', 
    'Chi-square (df=1)', 
    'Gamma (2, 2)', 
    'Laplace (1, 1)', 
    'Binomial (1, 0.1)', 
    'Poisson (5)'
]
st.text("haha")
# 2. Create the dropdown (selectbox)
selected_dist = st.selectbox("Choose a distribution to sample from:", options)
ns = st.number_input("Number of samples:", min_value=1, value=100)
ss = st.number_input("Sample size:", min_value=1, value=30)

if st.button("Run Simulation"):
    # 1. Get Data
    pop, d_name = generate_population(selected_dist)
    means = get_sample_means(pop, int(ns), int(ss))
    
    # 2. Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    
    # Population Plot
    ax1.hist(pop, bins=50, alpha=0.6)
    ax1.set_title(f"Original Population: {d_name}")
    # Sample Means Plot 
    y_jitter = np.random.normal(0, 0.1, size=len(means)) # Adds vertical spread
    ax2.scatter(means, y_jitter, c=means, cmap='coolwarm', alpha=0.6, s=10)

    # Add the Normal Curve overlay as before
    mu, std = norm.fit(means)
    # 1. Setup Bins
    # We use 20 bins to group the sample means
    counts, bin_edges = np.histogram(means, bins=20)
    bin_width = bin_edges[1] - bin_edges[0]

    # IMPORTANT: This tracks the height of each column so bricks stack!
    stack_heights = np.zeros(len(counts))

    # Create a list of random color indices from the HSV colormap
    color_indices = np.arange(len(means))
    np.random.shuffle(color_indices)
    cmap = plt.cm.get_cmap('hsv', len(means))

    # 2. Draw the "Bricks"
    for i, m in enumerate(means):
        # Find which bin this specific mean 'm' belongs to
        bin_idx = np.digitize(m, bin_edges) - 1
        
        # Boundary check to ensure the index stays within the array
        bin_idx = max(0, min(bin_idx, len(counts) - 1))
        
        # Draw a single brick
        # 'bottom' is set to the current height of that specific bin
        ax2.bar(bin_edges[bin_idx] + bin_width/2, 
                height=1, 
                width=bin_width * 0.9, 
                bottom=stack_heights[bin_idx], 
                color=cmap(color_indices[i]), 
                edgecolor='black', 
                linewidth=0.3)
        
        # Increment the height for that bin so the next brick sits on top
        stack_heights[bin_idx] += 1
    
    stack_heights[bin_idx] += 1
    # 3. Add the Normal Distribution Line (The "Bell")
    if len(means) > 1:
        mu, std = norm.fit(means)
        # Create x-values for the curve
        x = np.linspace(min(bin_edges), max(bin_edges), 100)
        
        # Calculate the PDF
        y = norm.pdf(x, mu, std)
        
        # SCALE THE CURVE: Multiply by total samples and bin width 
        # to convert density to the "brick count" scale
        y_scaled = y * int(ns) * bin_width
        
        ax2.plot(x, y_scaled, color='black', linestyle='--', linewidth=3, label='Normal Curve')
        ax2.legend()

    ax2.set_ylabel("Number of Samples")
    ax2.set_title(f"CLT: Individual Samples Stacking into a Normal Curve")

    
    st.pyplot(fig)
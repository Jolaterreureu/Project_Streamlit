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
    pop, d_name = generate_population(a1)
    means = get_sample_means(pop, int(ns), int(ss))
    
    # 2. Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    
    # Population Plot
    ax1.hist(pop, bins=50, alpha=0.6)
    ax1.set_title(f"Original Population: {d_name}")
    
    # Sample Means Plot (The CLT Magic)
    ax2.hist(means, bins=20, density=True, alpha=0.6, color='skyblue')
    
    # Add the Normal Curve overlay
    mu, std = norm.fit(means)
    x = np.linspace(min(means), max(means), 100)
    ax2.plot(x, norm.pdf(x, mu, std), 'g-', lw=2)
    ax2.set_title(f"Distribution of Sample Means (n={ss})")
    
    st.pyplot(fig)
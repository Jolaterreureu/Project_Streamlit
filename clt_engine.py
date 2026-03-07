import numpy as np

def generate_population(dist_index):
    """Generates the initial large population based on selection."""
    size = 1000000
    if dist_index == 'Uniform U(0, 1)':
        return np.random.rand(size), 'Uniform U(0,1)'
    elif dist_index == 'Chi-square (df=1)':
        return np.random.chisquare(1, size), 'Chisquare (df=1)'
    elif dist_index == 'Gamma (2, 2)':
        return np.random.gamma(2, 2, size), 'Gamma (2, 2)'
    elif dist_index == 'Laplace (1, 1)':
        return np.random.laplace(1, 1, size), 'Laplace (1, 1)'
    elif dist_index == 'Binomial (1, 0.1)':
        return np.random.negative_binomial(1, 0.1, size), 'Binomial (1, 0.1)'
    elif dist_index == 'Poisson (5)':
        return np.random.poisson(5, size), 'Poisson (5)'
    return None, "Unknown"

def get_sample_means(population, n_samples, sample_size):
    """Performs the sampling and returns an array of means."""
    means = np.zeros(n_samples)
    for i in range(n_samples):
        # Using np.random.choice is much faster for numpy arrays
        sample = np.random.choice(population, size=sample_size, replace=False)
        means[i] = np.mean(sample)
    return means
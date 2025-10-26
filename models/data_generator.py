
import numpy as np
import pandas as pd

def generate_heteroscedastic_data(num_samples=100):
    """
    Gera um conjunto de dados com heterocedasticidade.
    A variância do erro aumenta com o valor de X.
    """
    np.random.seed(42)  # Para reprodutibilidade
    X = np.random.rand(num_samples, 1) * 20
    
    # O erro tem uma variância que depende de X
    error_variance = (X.flatten() ** 2) * 0.1
    error_term = np.random.normal(0, np.sqrt(error_variance))
    
    # Relação linear mais o termo de erro heterocedástico
    y = 2.5 + 1.8 * X.flatten() + error_term
    
    return pd.DataFrame({'X': X.flatten(), 'y': y})

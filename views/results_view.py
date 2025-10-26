

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_diagnostic_plots(ols_model, wls_model, file_path):
    """Cria e salva gráficos de resíduos para os modelos OLS e WLS."""
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico 1: Antes da Correção (OLS)
    sns.scatterplot(x=ols_model.fittedvalues, y=ols_model.resid, ax=axes[0])
    axes[0].axhline(0, ls='--', color='red')
    axes[0].set_title('Análise de Resíduos: Antes da Correção (OLS)', fontsize=14)
    axes[0].set_xlabel('Valores Previstos', fontsize=12)
    axes[0].set_ylabel('Resíduos', fontsize=12)

    # Gráfico 2: Depois da Correção (WLS) - Usando resíduos Pearson
    sns.scatterplot(x=wls_model.fittedvalues, y=wls_model.resid_pearson, ax=axes[1]) # CORRIGIDO
    axes[1].axhline(0, ls='--', color='red')
    axes[1].set_title('Análise de Resíduos: Depois da Correção (WLS) - Pearson', fontsize=14)
    axes[1].set_xlabel('Valores Previstos', fontsize=12)
    axes[1].set_ylabel('Resíduos Pearson', fontsize=12)

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    print(f"\nGráfico de diagnóstico salvo em: {file_path}")

def format_and_save_results(ols_model, wls_model, ols_tests, wls_tests, file_path):
    """
    Formata os resultados comparando OLS e WLS.
    """
    print("--- Tabela Comparativa: OLS vs. WLS (Heterocedasticidade Corrigida) ---")
    print("Nota: p-valores altos (>0.05) nos testes do modelo WLS indicam que a heterocedasticidade foi corrigida com sucesso.")

    results_data = {
        'Métrica': [
            'R² Ajustado',
            'Coef. Intercepto', 'Std Err (Intercepto)',
            'Coef. X', 'Std Err (X)',
            '---',
            'Teste Breusch-Pagan (p-valor)',
            'Teste de White (p-valor)',
            'Teste de Park (p-valor)',
            'Teste de Glejser (p-valor)'
        ],
        'Modelo OLS (Original)': [
            f"{ols_model.rsquared_adj:.4f}",
            f"{ols_model.params[0]:.4f}", f"{ols_model.bse[0]:.4f}",
            f"{ols_model.params[1]:.4f}", f"{ols_model.bse[1]:.4f}",
            '---',
            f"{ols_tests['breusch_pagan']['lm_p_value']:.4f}",
            f"{ols_tests['white']['lm_p_value']:.4f}",
            f"{ols_tests['park']['p_value']:.4f}",
            f"{ols_tests['glejser']['p_value']:.4f}"
        ],
        'Modelo WLS (Corrigido)': [
            f"{wls_model.rsquared_adj:.4f}",
            f"{wls_model.params[0]:.4f}", f"{wls_model.bse[0]:.4f}",
            f"{wls_model.params[1]:.4f}", f"{wls_model.bse[1]:.4f}",
            '---',
            f"{wls_tests['breusch_pagan']['lm_p_value']:.4f}",
            f"{wls_tests['white']['lm_p_value']:.4f}",
            f"{wls_tests['park']['p_value']:.4f}",
            f"{wls_tests['glejser']['p_value']:.4f}"
        ]
    }
    
    df_results = pd.DataFrame(results_data)
    
    print(df_results.to_string(index=False))
    
    df_results.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"\nResultados comparativos salvos em: {file_path}")

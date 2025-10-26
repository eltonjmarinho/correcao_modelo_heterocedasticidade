import os
import pandas as pd
from models.data_generator import generate_heteroscedastic_data
from models.regression_model import estimate_ols, estimate_wls, run_diagnostic_tests
from views.results_view import format_and_save_results, create_diagnostic_plots

def run_analysis():
    """Orquestra a análise completa usando OLS e WLS e salva os dados gerados."""
    # Garantir que os diretórios de saída existam
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    # 1. Gerar e salvar os dados
    data = generate_heteroscedastic_data()
    data_path = "data/dados_gerados.csv"
    data.to_csv(data_path, index=False, encoding='utf-8-sig')
    print(f"Dados gerados salvos em: {data_path}")

    # 2. Estimar modelo OLS original e diagnosticar
    ols_model = estimate_ols(data)
    ols_tests = run_diagnostic_tests(ols_model, data) # Passa o data
    
    # 3. Estimar modelo WLS como correção
    wls_model = estimate_wls(data)
    wls_tests = run_diagnostic_tests(wls_model, data) # Passa o data

    # 4. Apresentar e salvar os resultados comparativos
    table_path = "results/tabela_comparativa_wls_completa.csv"
    format_and_save_results(ols_model, wls_model, ols_tests, wls_tests, table_path)

    # 5. Gerar e salvar a análise gráfica
    plot_path = "results/analise_grafica_residuos_wls.png"
    create_diagnostic_plots(ols_model, wls_model, plot_path)
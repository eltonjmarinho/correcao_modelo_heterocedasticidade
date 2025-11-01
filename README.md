# Correção de Heterocedasticidade em Modelos de Regressão

Este projeto demonstra a construção de uma base de dados com heterocedasticidade, a estimação de um modelo OLS (Mínimos Quadrados Ordinários), a aplicação de um método de correção para a heterocedasticidade (Mínimos Quadrados Ponderados - WLS) e a comparação dos resultados.

## Estrutura do Projeto (MVC)
O projeto segue uma estrutura Model-View-Controller (MVC) para organização do código:
- `models/`: Contém a lógica de geração de dados e os modelos de regressão.
- `views/`: Responsável pela formatação e salvamento dos resultados (tabelas e gráficos).
- `controllers/`: Orquestra o fluxo da aplicação, chamando as funções dos modelos e das views.
- `data/`: Pasta para salvar os dados gerados.
- `results/`: Pasta para salvar os resultados da análise (tabelas comparativas e gráficos).

## Como Configurar e Rodar

### 1. Pré-requisitos
Certifique-se de ter o Python 3.x instalado.

### 2. Instalação das Dependências
Instale as bibliotecas Python necessárias usando o `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Executar a Análise
Para rodar a análise completa, execute o script principal:
```bash
python main.py
```

#### Rodando em um Notebook (Jupyter, Colab)
Se você estiver rodando a partir de um notebook em um subdiretório (ex: `notebooks/`), você pode usar:
```python
%run ../main.py
```
Ou, para garantir que os diretórios sejam criados corretamente e o script seja executado a partir da raiz do projeto:
```python
import os
os.makedirs('data', exist_ok=True)
os.makedirs('results', exist_ok=True)
%run main.py
```

## Saída da Análise

Ao executar `main.py`, o script irá:
- Gerar uma base de dados com heterocedasticidade e salvá-la em `data/dados_gerados.csv`.
- Estimar um modelo OLS e um modelo WLS.
- Realizar diversos testes de heterocedasticidade (Breusch-Pagan, White, Park, Glejser) para ambos os modelos.
- Imprimir uma tabela comparativa dos resultados no terminal.
- Salvar a tabela comparativa em `results/tabela_comparativa_wls_completa.csv`.
- Gerar e salvar um gráfico de resíduos comparando OLS e WLS em `results/analise_grafica_residuos_wls.png`.

## Interpretação dos Resultados

A tabela comparativa e o gráfico de resíduos permitirão:
- **Diagnosticar a heterocedasticidade**: Os p-valores baixos nos testes para o modelo OLS original confirmam o problema.
- **Verificar a correção**: Os p-valores altos nos testes para o modelo WLS (quando aplicados corretamente aos resíduos transformados) indicam que a heterocedasticidade foi corrigida. Visualmente, o gráfico de resíduos do WLS deve apresentar uma dispersão aleatória.

- **Comparar a eficiência**: O modelo WLS geralmente apresentará erros-padrão menores e um R² Ajustado maior, indicando estimativas mais precisas e um melhor ajuste.

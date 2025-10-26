import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

def estimate_ols(data):
    """Estima um modelo de Mínimos Quadrados Ordinários (OLS)."""
    X = sm.add_constant(data['X'])
    y = data['y']
    model = sm.OLS(y, X).fit()
    return model

def estimate_wls(data):
    """Estima um modelo de Mínimos Quadrados Ponderados (WLS) para corrigir a heterocedasticidade."""
    X = sm.add_constant(data['X'])
    y = data['y']
    
    # Estima a variância do erro para encontrar os pesos
    ols_resid = sm.OLS(y, X).fit().resid
    log_resid_sq = np.log(ols_resid**2)
    aux_model = sm.OLS(log_resid_sq, X).fit()
    weights = 1.0 / np.exp(aux_model.fittedvalues)
    
    # Estima o modelo WLS com os pesos calculados
    wls_model = sm.WLS(y, X, weights=weights).fit()
    return wls_model

def _get_transformed_ols_model_from_wls(wls_model):
    """
    Retorna um modelo OLS equivalente ao WLS, com variáveis transformadas.
    Os testes de heterocedasticidade devem ser aplicados a este modelo.
    """
    y = wls_model.model.endog
    X = wls_model.model.exog
    weights = wls_model.model.weights
    
    sqrt_weights = np.sqrt(weights).reshape(-1, 1) # Corrigido: remodelar para (100, 1)
    y_transformed = y * sqrt_weights.flatten() # y é 1D, então flatten() para multiplicar corretamente
    X_transformed = X * sqrt_weights
    
    transformed_ols_model = sm.OLS(y_transformed, X_transformed).fit()
    return transformed_ols_model

def run_diagnostic_tests(model, data):
    """Executa testes de diagnóstico de heterocedasticidade.
    Se for um modelo WLS, os testes são aplicados ao modelo OLS transformado equivalente.
    """
    # A matriz exog para os testes deve ser a original (com a constante)
    original_exog = model.model.exog

    if isinstance(model.model, sm.WLS):
        test_model_for_resid = _get_transformed_ols_model_from_wls(model)
    else:
        test_model_for_resid = model
        
    # Teste de Breusch-Pagan
    bp_test = het_breuschpagan(test_model_for_resid.resid, original_exog)
    
    # Teste de White
    white_test = het_white(test_model_for_resid.resid, original_exog)

    # Teste de Park: log(resid^2) vs log(X)
    # Cuidado com log(0) ou log(negativo) - assumindo X > 0
    log_resid_sq = np.log(test_model_for_resid.resid**2)
    log_X = np.log(data['X'])
    park_aux_model = sm.OLS(log_resid_sq, sm.add_constant(log_X)).fit()
    park_p_value = park_aux_model.pvalues[1] # p-valor do coeficiente de log(X)

    # Teste de Glejser: |resid| vs X
    abs_resid = np.abs(test_model_for_resid.resid)
    glejser_aux_model = sm.OLS(abs_resid, original_exog).fit()
    glejser_p_value = glejser_aux_model.pvalues[1] # p-valor do coeficiente de X

    results = {
        'breusch_pagan': {'lm_p_value': bp_test[1]},
        'white': {'lm_p_value': white_test[1]},
        'park': {'p_value': park_p_value},
        'glejser': {'p_value': glejser_p_value}
    }
    
    return results
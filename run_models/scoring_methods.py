"""
Implements different scoring methods for our custom ML models.
Current supports:
- accuracy
- confusion-matrix
- f1-score
- bayesian detection rate

! All of the scoring methods, need to take `y_pred` and `y_true` as arguments and none other.
If a scoring method is added, is also needs to be added to `get_scoring_methods`'s return value.
"""

import constants

from sklearn.metrics import f1_score, roc_auc_score

def check_inputs(y_pred, y_true):
    """
    Performs checks on the input to any of the scoring methods.
    Both arguments are 1D array-like objects
    """
    if len(y_pred) != len(y_true):
        raise ValueError("The length of y_pred and y_true should be the same")

def accuracy(y_pred, y_true):
    """
    One of the simplest scoring methods that is calculated as $correct / total$.

    @param y_pred is a 1D array-like object that represents the predicted values
    @param y_true is also a 1D array-like object of the same length as `y_pred` and represents the true values
    """
    check_inputs(y_pred, y_true)

    correct = len([x for x, y in zip(y_pred, y_true) if x == y])

    return correct / len(y_pred)

def confusion_matrix(y_pred, y_true):
    """
    Rather than having an entry for every single class (of which there can be a lot), we treat it as a binary classification problem.
    - If you have correctly predicted a monitored website, its a TP.
    - If you have correctly predicted an unmonitored website, its a TN.
    - If you have predicted an unmonitored website as a monitored, it is a FP.
    - If you have predicted a monitored website as unmonitored, it is a FN

    @param y_pred is a 1D array-like object that represents the predicted values
    @param y_true is also a 1D array-like object of the same length as `y_pred` and represents the true values
    """
    check_inputs(y_pred, y_true)
    res = {
        'TP': 0,
        'TN': 0,
        'FP': 0,
        'FN': 0
    }

    for i, val in enumerate(y_pred):
        if val == y_true[i]:
            if val == constants.UNMONITORED_LABEL:
                res['TN'] += 1
            else:
                res['TP'] += 1

        else:
            if y_true[i] == constants.UNMONITORED_LABEL:
                res['FP'] += 1
            else:
                res['FN'] += 1

    return res

def f1_score1(y_pred, y_true):
    """
    Returns the weighted f1 score

    @param y_pred is a 1D array-like object that represents the predicted values
    @param y_true is also a 1D array-like object of the same length as `y_pred` and represents the true values
    """
    check_inputs(y_pred, y_true)
    return f1_score(y_true, y_pred, average='weighted')

def bayesian_detection_rate(y_pred, y_true):
    """
    Returns the bayesian detection rate

    $$\text{BDR} = \frac{\text{TPR} \times \Pr(M)}{\text{TPR} \times \Pr(M) + \text{FPR} \times \Pr(U)}$$
    where
    $$\Pr(M) = \frac{|\text{Monitored}|}{|\text{Total Pages}|}, \quad \Pr(U) = 1 - \Pr(M)$$
    """
    cm = confusion_matrix(y_pred, y_true)
    PrM = len([y for y in y_true if y != constants.UNMONITORED_LABEL]) / float(len(y_true))
    PrU = 1 - PrM

    TPR = cm['TP'] / len(y_true)
    FPR = cm['FP'] / len(y_true)

    nominator =TPR * PrM
    denominator = nominator + (FPR * PrU)

    try:
        return nominator / denominator
    except:
        return 0

def evaluate_model(y_pred, y_true):
    """
    Given a `y_pred` and `y_true`, returns a dictionary with all of the scoring methods
    """
    evaluations = {}

    for scoring_method in SCORING_METHODS:
        evaluations[scoring_method] = SCORING_METHODS[scoring_method](y_pred, y_true)

    return evaluations

def get_scoring_methods():
    return {
        'accuracy': accuracy, 'confusion-matrix': confusion_matrix, 'f1-score': f1_score1, 'bayesian_detection_rate': bayesian_detection_rate
    }

SCORING_METHODS = get_scoring_methods()

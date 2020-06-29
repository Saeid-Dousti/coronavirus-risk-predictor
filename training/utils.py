import yaml


def stripword(word):
    word = word.replace("[", "")
    word = word.replace("]", "")
    word = word.replace("'", "")
    word = word.replace("'", "")
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace("_", "")
    word = word.replace(":", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    word = word.replace("/", "")
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("´", "")
    word = word.replace("`", "")
    word = word.replace(";", "")
    word = word.replace("__END", "")
    word = word.replace("BEG__", "")
    return word


def read_yaml(model_type):
    """read yaml files to get configurations"""
    with open('configs/config.yml', 'r') as f:
        y = yaml.load(f)
        n_estimators = y['n_estimators']
        max_features = y['max_features']
        max_depth = y['max_depth']
        min_samples_split = y['min_samples_split']
        min_samples_leaf = y['min_samples_leaf']
        bootstrap = y['bootstrap']
        booster = y['booster']
        subsample = y['subsample']
        C = y['C']
        activation = y['activation']
        solver = y['solver']
        learning_rate = y['learning_rate']

    if model_type == 'rf':
        max_depth.append(None)
        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}

    elif model_type == 'xgb':
        random_grid = {'booster': booster,
                       'min_child_weight': min_samples_leaf,
                       'max_depth': max_depth,
                       'subsample ': subsample}

    elif model_type == 'lr':
        random_grid = {'C': C}

    else:
        random_grid = {
            'hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100,)],
            'activation': activation,
            'solver': solver,
            'alpha': [0.0001, 0.05],
            'learning_rate': learning_rate,
        }

    return random_grid

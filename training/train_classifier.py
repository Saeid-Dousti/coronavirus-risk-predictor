import argparse
import pickle
from training.utils import read_yaml

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier


def main(args):
    """Trains classifier depending on the type chosen and optimizes for the metric chosen"""
    # load data
    data = pd.read_csv(args['data_csv'], index_col=0)
    y = data['scores']
    X = data.drop(['activities', 'counties', 'dates', 'scores'], axis=1)

    # resample to counteract slight class imbalance
    X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    # create type of classifier chosen
    if args['type'] == 'rf':
        clf = RandomForestClassifier()
    elif args['type'] == 'xgb':
        clf = XGBClassifier()
    elif args['type'] == 'lr':
        clf = LogisticRegression()
    else:
        clf = MLPClassifier(early_stopping=True, max_iter=200)

    # carry out hyperparameter optimization
    if args['optimization_metric']:
        random_grid = read_yaml(args['type'])

        opt_model = RandomizedSearchCV(estimator=clf, param_distributions=random_grid, n_iter=100, cv=3,
                                       scoring=args['optimization_metric'], random_state=42, verbose=0, n_jobs=-1)
        opt_model.fit(X_train, y_train)
        clf = opt_model.best_estimator_

    # train model
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # print results of model validation
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print(cm)
    print(report)

    pickle.dump(clf, open('app/classifiers/retrained_clf.sav', 'wb'))
    print('Saved as app/classifiers/retrained_clf.sav')


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="train classifier"
    )
    parser.add_argument(
        "-t", "--type", help="which model type to train", choices=['rf', 'xgb', 'lr', 'nn'],
        default='rf', required=True, type=str
    )
    parser.add_argument(
        "-d", "--data_csv", help="the csv data file to train the model on",
        default='data/processed/triplet_training_data_with_features.csv', required=False
    )
    parser.add_argument(
        "-o", "--optimization_metric", help="which metric to optimize the model on",
        choices=['recall', 'accuracy', 'f1'], default=None, required=False
    )
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    parser = init_argparse()
    args = parser.parse_args()
    main(vars(args))

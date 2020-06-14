import argparse
from datetime import datetime
import numpy as np
from gensim.models import Word2Vec
import pickle
from app.utils import APICaller


# Main function
def main(args):
    clf_file = 'classifiers/optimized_random_for.sav'
    embd_file = 'word2vec/newsdata_model2'
    features, feature_list, date, county = feature_extraction(args['activity'], args['location'], clf_file)
    risk_level = classification(args['activity'], features, feature_list, date, county, embd_file)


# feature extraction function giving word embedding, demographics, case no., weather and social dist. levels
def feature_extraction(activity, location, word2vec_file):
    # get current date
    date = datetime.now()

    # extract features
    # Word embedding
    currentmodel = Word2Vec.load(word2vec_file)
    sentiment = currentmodel.wv[activity.lower()] - currentmodel.wv['safe']

    # API Features
    caller = APICaller(location, date)
    county = caller.get_county()
    cases = caller.cases()
    demographics = caller.demographics()
    weather = caller.weather()
    social_dist = caller.social_dist()

    # concatenate all features
    features = np.append(sentiment, (float(social_dist), int(cases)))
    features = np.concatenate((features, np.array(weather).reshape(-1)))
    features = np.concatenate((features, np.array(demographics).reshape(-1)))
    features = features.reshape(-1)

    feature_list = ['Social Distancing levels', 'Cases in last 2 weeks', 'Max Temp',
                    'Average Temp', 'Sunlight (hrs)', 'Wind (kmh)', 'Rain (mm)',
                    'Population Density', 'Population size', 'Health-ins1', 'Health-ins2', 'Poverty Levels']

    return features, feature_list, date, county


# function putting features into classifier
def classification(activity, features, feature_list, date, location, classifier_file):
    # classify
    clf = pickle.load(open(classifier_file, 'rb'))
    pred = clf.predict(features.reshape(1, -1))
    if pred == 1:
        risk_level = 'high risk'
    else:
        risk_level = 'low risk'

    # output
    print('Activity: ' + activity)
    print('Location: ' + location)
    print('Date: ' + str(date))
    print('\n')
    for n, f in zip(feature_list, features[100:-1]):
        print(n + ': ' + str(f))
    print('\n')
    print('RISK LEVEL: ' + risk_level.upper())

    return risk_level


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Classify risk level"
    )
    parser.add_argument(
        "-a", "--activity", help="activity",
        default='data/raw/sample.csv'
    )
    parser.add_argument(
        "-c", "--county", help="county"
    )
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    parser = init_argparse()
    args = parser.parse_args()
    main(vars(args))

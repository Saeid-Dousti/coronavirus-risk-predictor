import argparse
import pickle
from datetime import datetime
import streamlit as st
import numpy as np
from gensim.models import Word2Vec

from app.utils import APICaller


# Main function
def main(args):
    clf_file = 'app/classifiers/optimized_random_for.sav'
    embd_file = 'app/word2vec/newsdata_model2'
    county = args['county'].replace(' County', '')
    features, feature_list, date, county = feature_extraction(args['activity'], county, embd_file)
    risk_level = classification(args['activity'], features, feature_list, date, county, clf_file)


def feature_extraction(activity, location, word2vec_file):
    """feature extraction function giving word embedding, demographics, case no.,
    weather and social dist. levels"""
    # initiate placeholder and progress bar
    bar = st.progress(0)
    placeholder = st.empty()

    # get current date
    date = datetime.now()

    # extract features
    # Word embedding
    placeholder.text('Getting activity information...')
    currentmodel = Word2Vec.load(word2vec_file)
    try:
        sentiment = currentmodel.wv[activity.lower()] - currentmodel.wv['safe']
    except KeyError:
        return None, None, None, None
    bar.progress(20)

    # API Features
    caller = APICaller(location, date)
    placeholder.text('Getting COVID-19 information...')
    county = caller.get_county()
    cases = caller.cases()
    bar.progress(40)
    placeholder.text('Getting county demographic information...')
    demographics = caller.demographics()
    bar.progress(60)
    placeholder.text('Getting weather and climate information...')
    weather = caller.weather()
    bar.progress(80)
    placeholder.text('Getting social distancing information...')
    social_dist = round(caller.social_dist())
    bar.progress(100)

    # concatenate all features
    features = np.append(sentiment, (float(social_dist), int(cases)))
    features = np.concatenate((features, np.array(weather).reshape(-1)))
    features = np.concatenate((features, np.array(demographics).reshape(-1)))
    features = features.reshape(-1)

    feature_list = ['Social Distancing levels', 'Cases in last 2 weeks', 'Max Temp',
                    'Average Temp', 'Sunlight (hrs)', 'Wind (kmh)', 'Rain (mm)',
                    'Population Density', 'Population size', 'Health-ins1', 'Health-ins2', 'Poverty Levels']

    placeholder.empty()
    return features, feature_list, date, county


def classification(activity, features, feature_list, date, location, classifier_file):
    """Classification function putting features into classifier and returning risk level"""
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
    print('OVERALL RISK LEVEL: ' + risk_level.upper())

    return risk_level


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Classify risk level",
    )
    parser.add_argument(
        "-a", "--activity", help="activity",
        default='swimming',
        required=True,
        type=str
    )
    parser.add_argument(
        "-c", "--county", help="county",
        default='San Francisco County',
        required=True,
        type=str
    )
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    parser = init_argparse()
    args = parser.parse_args()
    main(vars(args))

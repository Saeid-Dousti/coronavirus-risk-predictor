import os
from zipfile import ZipFile

import pandas as pd
import streamlit as st
from PIL import Image

from app.inference_functions import feature_extraction, classification

classifier_file = 'app/classifiers/classifier_random_for.sav'
word2vec_file = 'app/word2vec/newsdata_model2'


# create US counties dataframe to allow people to choose counties
df = pd.read_csv('data/united-states-counties.csv')


def main():
    """Calls run function only if main"""
    image = Image.open('static/coronavirus.png')
    st.image(image, width=100, format='PNG')
    with open("app/intro.md", 'r') as file:
        st.markdown(file.read())
    run()


def run():
    """Function runs web-app"""
    # ask for input on activity and county location
    act_input = st.text_input("Please indicate the activity you would like to partake in.")
    states = sorted(df['State'].value_counts().index.tolist())
    state = st.selectbox('Choose State', states)
    count_input = None

    if state:
        counties = sorted(df[df['State'] == state]['County'].value_counts().index.tolist())
        count_input = st.selectbox('Choose County', counties)

    if act_input and count_input:
        if st.button('Check Risk'):

            count_input = count_input.replace(' County', '')
            features, feature_list, date, county_full = feature_extraction(act_input, count_input, word2vec_file)

            if features is None:
                st.markdown('No information about inputted activity, please try with another activity.')

            else:
                display_features = pd.DataFrame(features[100:-1].reshape(1, -1), columns=feature_list)

                # display results
                st.table(display_features)
                risk_level = classification(act_input, features, feature_list, date, county_full, classifier_file)
                st.markdown('OVERALL RISK LEVEL: ' + risk_level.upper())


# only run if main
if __name__ == "__main__":
    main()

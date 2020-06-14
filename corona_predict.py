import os
import csv
import pandas as pd
import streamlit as st
from PIL import Image
from zipfile import ZipFile

from app.classification_functions import feature_extraction, classification

classifier_file = 'app/classifiers/classifier_random_for.sav'
word2vec_file = 'app/word2vec/newsdata_model2'

# extract word2vec dependency files if this has not occurred previously
if not os.path.isfile(word2vec_file + '.wv.vectors.npy'):
    with ZipFile('word2vec_file1.zip', 'r') as zipObj:
        # Extract all the contents of zip file in word2vec directory
        zipObj.extractall('app/word2vec')

if not os.path.isfile(word2vec_file + '.trainables.syn1neg.npy'):
    with ZipFile('word2vec_file2.zip', 'r') as zipObj:
        # Extract all the contents of zip file in word2vec directory
        zipObj.extractall('app/word2vec')


# create dictionary with all the US counties
with open('data/united-states-counties.csv') as csvfile:
    county_list = csv.reader(csvfile)
    statedict = dict()
    for county in county_list:
        statedict[county[0]] = county[1]


# main function starting app
def main():
    image = Image.open('static/coronavirus.png')
    st.image(image, width=100, format='PNG')
    with open("app/intro.md", 'r') as file:
        st.markdown(file.read())
    run()


# run web app
def run():
    # ask for input on activity and county location
    act_input = st.text_input("Please indicate the activity you would like to partake in")
    count_input = st.text_input("Which county do you want to go to?")
    if act_input and count_input:
        if count_input not in statedict:

            # check if county exists in US county dictionary
            st.markdown('Inputted county has not been found, please try with another county')

        else:
            # if exists - start feature extraction and classification
            count_input = count_input.replace(' County', '')
            features, feature_list, date, county_full = feature_extraction(act_input, count_input, word2vec_file)
            display_features = pd.DataFrame(features[100:-1].reshape(1, -1), columns=feature_list)

            # display results
            st.table(display_features)
            risk_level = classification(act_input, features, feature_list, date, county_full, classifier_file)
            st.markdown('RISK LEVEL: ' + risk_level.upper())


# only run if main
if __name__ == "__main__":
    main()

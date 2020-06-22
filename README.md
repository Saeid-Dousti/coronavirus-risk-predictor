# Corona Predict 🧍↔️🧍
#### Tool for Coronavirus Infection Risk Prediction of Activities

[![GitHub issues](https://img.shields.io/github/issues/marcelschaack/coronavirus-risk-predictor?style=flat-square)](https://github.com/marcelschaack/coronavirus-risk-predictor/issues)
[![GitHub forks](https://img.shields.io/github/forks/marcelschaack/coronavirus-risk-predictor?style=flat-square)](https://github.com/marcelschaack/coronavirus-risk-predictor/members)
[![GitHub stars](https://img.shields.io/github/stars/marcelschaack/coronavirus-risk-predictor?style=flat-square)](https://github.com/marcelschaack/coronavirus-risk-predictor/stargazers)
[![GitHub license](https://img.shields.io/github/license/marcelschaack/coronavirus-risk-predictor?style=flat-square)](https://github.com/marcelschaack/coronavirus-risk-predictor/blob/master/LICENSE)
[![HitCount](http://hits.dwyl.com/marcelschaack/coronavirus-risk-predictor.svg)](http://hits.dwyl.com/marcelschaack/coronavirus-predictor)

Welcome to the Corona Predict Github.
This tool helps you understand the risks of Coronavirus transmission of independent particular activities.

Here is a demo of the application:

![Failed to load](/static/application_demo.gif?raw=true "Demo")


## Setup
Clone repository
```
git clone https://github.com/marcelschaack/coronavirus-risk-predictor.git
cd ./coronavirus-risk-predictor
```


#### Dependencies

- Python 3.6 or higher
- pip
- conda
- shown in [requirements.txt](https://github.com/marcelschaack/coronavirus-risk-predictor/blob/master/requirements.txt)


#### Installation
To install the package above, pleae run:
```shell
pip install -r requirements
```

## Build Environment
- Include instructions of how to launch scripts in the build subfolder
- Build scripts can include shell scripts or python setup.py files
- The purpose of these scripts is to build a standalone environment, for running the code in this repository
- The environment can be for local use, or for use in a cloud environment
- If using for a cloud environment, commands could include CLI tools from a cloud provider (i.e. gsutil from Google Cloud Platform)
```
# Example

# Step 1
# Step 2
```

## Configs
- As you will require AWS access keys to run the full interference, please contact me to obtain the keys
- If credentials are needed, use environment variables or HashiCorp's [Vault](https://www.vaultproject.io/)


## Test
- Tests will be added here briefly
```
# Example

# Step 1
# Step 2
```

## Run Inference
- WordEmbedding model to create word embeddings of all activities
- final classification of activity + location (+date) into high-risk or low-risk
```
python 
```

## Build Model
- The word2vec model and final classifier model (random forest) are already build and included as pickle files.
- If you would like to train your own classifier or word2vec model, you can do so by running the following commands:

```
python training/train_classifier.py
python training/train_word2vec.py
```

![Failed to load](/static/data_training_pipeline.jpg?raw=true "Data Training Pipeline")

## Running the app
Run
```
streamlit run corona_predict.py
```

## Analysis
|Features used             |Model          |Recall   |
|--------------------------|---------------|---------|
|Word2Vec                  |Random Forest  |75%      |
|Word2Vec + location-based |Random Forest  |84%      |


- Further results about PCA and significance will be included shortly

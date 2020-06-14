# Corona Predict
#### Tool for Coronavirus Infection Risk Prediction of Activities

Welcome to my project GitHub.
This tool helps you understand the risks of Coronavirus transmission of independent particular activities.
Further instructions will be added shortly.


## Setup
Clone repository and update python path
```
git clone https://github.com/marcelschaack/coronavirus-risk-predictor.git
cd ./coronavirus-risk-predictor
```


#### Dependencies

- [Streamlit](https://streamlit.io)
- shown in [requirements.txt](https://github.com/marcelschaack/coronavirus-risk-predictor/blob/master/requirements.txt)


#### Installation
To install the package above, pleae run:
```shell
pip install -r requiremnts
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
- **DO NOT STORE CREDENTIALS IN THE CONFIG DIRECTORY!!**
- If credentials are needed, use environment variables or HashiCorp's [Vault](https://www.vaultproject.io/)


## Test
- Include instructions for how to run all tests after the software is installed
```
# Example

# Step 1
# Step 2
```

## Run Inference
- WordEmbedding model to create word embeddings of all activities
- final classification of activity + location (+date) into high-risk or low-risk
```
# Example

# Step 1
# Step 2
```

## Build Model
- Include instructions of how to build the model
- This can be done either locally or on the cloud

![Failed to load](/static/data_training_pipeline.jpg?raw=true "Data Training Pipeline")
```
# Example

# Step 1
# Step 2
```

## Serve Model
- Include instructions of how to set up a REST or RPC endpoint
- This is for running remote inference via a custom model
```
# Example

# Step 1
# Step 2
```

## Analysis
- Include some form of EDA (exploratory data analysis)
- And/or include benchmarking of the model and results
```
# Example

# Step 1
# Step 2
```

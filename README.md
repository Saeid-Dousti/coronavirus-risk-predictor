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
```bash
git clone https://github.com/marcelschaack/coronavirus-risk-predictor.git
cd ./coronavirus-risk-predictor
```


#### Dependencies

- Python 3.8 or higher
- conda
- shown in [requirements.txt](https://github.com/marcelschaack/coronavirus-risk-predictor/blob/master/requirements.txt)


#### Installation
To install the packages above, please run:
```shell script
pip install -r requirements
```

Alternatively, if you would like to use docker you can also use:
```shell script
docker build -t corona-predict-streamlit:v1 -f Dockerfile.app .
docker run -p 80:80 corona-predict-streamlit:v1
```

## Configs
- As you will require AWS access keys to run the full interference, please contact me to obtain the keys

## Run Inference
- WordEmbedding model to create word embeddings of all activities
- final classification of activity + location (+date) into high-risk or low-risk
```shell script
python app/inference_functions.py
```

## Build Model
- The word2vec model and final classifier model (random forest) are already build and included as pickle files.
- If you would like to train your own classifier or word2vec model, you can do so by running the following commands:

```shell script
python training/train_classifier.py
python training/train_word2vec.py
```

![Failed to load](/static/data_training_pipeline.jpg?raw=true "Data Training Pipeline")

## Running the app
Run
```shell script
streamlit run corona_predict.py
```

Or run the Docker Build:
```shell script
docker build -t corona-predict-streamlit:v1 -f Dockerfile.app .
docker run -p 80:80 corona-predict-streamlit:v1
```

## Deploy to Google Kubernetes Engine (GKE)
Based off the instruction from Google's ['Deploying a containerized web application'](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app).

Prerequisites:
1) A Google Cloud (GC) Project with billing enabled.
2) The GC SDK installed (https://cloud.google.com/sdk/docs/quickstarts)
3) Install kubernetes
```shell script
gcloud components install kubectl
```

Set up gcloud tool
```shell script
export PROJECT_ID=gcp-project-name
export ZONE=gcp-compute-zone (e.g. us-west-1)

gcloud config set project PROJECT_ID
gcloud config set compute/zone ZONE

gcloud auth configure-docker
```

Build and push the container image to GC Container Registry:
```shell script
docker build -t gcr.io/coronavirus-risk-predictor/corona-predict-streamlit:v1 -f Dockerfile.app .
docker push gcr.io/coronavirus-risk-predictor/corona-predict-streamlit:v1
```

Create GKE Cluster
```shell script
gcloud container clusters create corona-predict-cluster --machine-type=n1-highmem-2
gcloud compute instances list
```

Deploy app to GKE
```shell script
kubectl create deployment corona-predict-app --image=gcr.io/coronavirus-risk-predictor/corona-predict-streamlit:v1
kubectl autoscale deployment corona-predict-app --cpu-percent=80 --min=1 --max=5
kubectl get pods
```

Expose app to internet
```shell script
kubectl expose deployment corona-predict-app --name=corona-predict-app-service --type=LoadBalancer --port 80 --target-port 8080
kubectl get service
```
---


## Analysis
|Features used             |Model          |Recall   |
|--------------------------|---------------|---------|
|Word2Vec                  |Random Forest  |75%      |
|Word2Vec + location-based |Random Forest  |84%      |


- The predicted results of the model also highly correlate with the Coronavirus case numbers and findings by the New York Times on individual activities.
![Failed to load](/static/model_validation.jpg?raw=true "Further model validation")


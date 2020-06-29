import csv
import gzip
import json
import os
import urllib.request
from datetime import timedelta, datetime
from statistics import mean
from time import localtime

import boto3
import requests
import yaml

# read yaml files to get configurations
f = open('configs/config.yml', 'r')
y = yaml.load(f)
key1 = y['API_key_census']
key2 = y['API_key_weather']
key3 = y['yaml_key1']
key4 = y['yaml_key2']
f.close()


class APICaller:
    """class calling all APIs to extract features about county"""
    def __init__(self, county, date):
        self.county = county
        self.date = date
        self.date_str = str(date)[:10]
        self.code = self.get_code()
        self.state = self.get_state()

    def get_county(self):
        return self.county

    def get_code(self):
        """get FIPS code for county name"""
        with open('data/county-fips-to-name.csv', 'r') as csvfile:
            csvdata = csv.reader(csvfile)
            for row in csvdata:
                if row[1] in self.county:
                    code = row[0]
                    break

        # county fips code has to be length of 5
        if len(code) == 4:
            code = '0' + code

        return code

    def get_state(self):
        """get state the county is located in"""
        with open('data/united-states-counties.csv', 'r') as csvfile:
            csvdata = csv.reader(csvfile)
            for row in csvdata:
                if self.county in row[0]:
                    state = row[1].rstrip()
                    break

        return state

    def demographics(self):
        """get demographic information about county from US census API, including
        population, density, poverty levels and no. of people with health insurance"""
        code = self.code
        url = 'https://api.census.gov/data/2017/pep/population?get=DENSITY,POP&for=county:{}&in=state:{}&' \
              'key={}'.format(code[2:], code[:2], key1)
        url2 = 'https://api.census.gov/data/timeseries/healthins/sahie?get=NIC_PT,NUI_PT,NAME&for=county:{}&' \
               'in=state:{}&time=2017&key={}'.format(code[2:], code[:2], key1)
        url3 = 'https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVALL_PT,SAEMHI_PT,NAME&for=county:{}&' \
               'in=state:{}&time=2018&key={}'.format(code[2:], code[:2], key1)

        response = requests.get(url).json()
        response2 = requests.get(url2).json()
        response3 = requests.get(url3).json()

        density = response[1][0]
        population = response[1][1]
        healthins1 = response2[1][0]
        healthins2 = response2[1][1]
        pov1 = response3[1][0]
        pov2 = response3[1][1]

        demographics = (density, population, healthins1, healthins2, pov1, pov2)
        return demographics

    def weather(self):
        """Get current weather information at county using weather API"""
        date = self.date

        with open('data/county_to_zip.csv', 'r') as csvfile:
            csvdata = csv.reader(csvfile)
            for row in csvdata:
                if row[1] == self.code:
                    zipcode = row[0]
                    break

        for _ in range(7):
            try:
                url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={}' \
                      '&date={}&tp=24&format=json&key={}'.format(zipcode, date, key2)
                response = requests.get(url).json()

                temp = response['data']['weather'][0]['maxtempC']
                temp2 = response['data']['weather'][0]['avgtempC']
                sun = response['data']['weather'][0]['sunHour']
                wind = response['data']['weather'][0]['hourly'][0]['windspeedKmph']
                rain = response['data']['weather'][0]['hourly'][0]['precipMM']
                break

            except KeyError:
                date = date - timedelta(days=1)

        weather = (temp, temp2, sun, wind, rain)
        return weather

    def social_dist(self):
        """get social distancing levels at county - given by average out of home dwell time"""
        date = str(self.date - timedelta(days=3, hours=16))[:10]
        code = self.code

        filename = date + '-social-distancing.csv.gz'

        # download social distancing information file from S3 bucket
        if not os.path.isfile('data/raw/' + filename):
            session = boto3.Session(
                aws_access_key_id=key3,
                aws_secret_access_key=key4,  # use current access key from SafeGraph group
                region_name='us-east-1'
            )
            s3 = session.client('s3', endpoint_url='https://s3.wasabisys.com')

            filedir = 'social-distancing/v2/{}/{}/{}/'.format(date[:4], date[5:7], date[8:])
            s3.download_file(Bucket='sg-c19-response', Key=filedir + filename, Filename='data/raw/' + filename)

        with gzip.open('data/raw/' + filename, mode="rt") as csvfile:
            dwell_times = list()

            csvdata = csv.reader(csvfile)
            for row in csvdata:
                if row[0][:-7] == code:
                    dwell_times.append(int(row[21]))

        return mean(dwell_times)

    def cases(self):
        """get number of case increase over last 2 weeks in county"""
        date = self.date_str
        date2 = str(self.date - timedelta(days=7))[:10]
        county = self.county + ' County, ' + self.state + ', United States'
        case_file = 'data/raw/timeseries-byLocation.json'

        if datetime.fromtimestamp(os.path.getmtime(case_file)) < self.date - timedelta(days=1):
            url = 'https://coronadatascraper.com/timeseries-byLocation.json'
            urllib.request.urlretrieve(url, case_file)

        with open(case_file, 'r', encoding="utf8") as jfile:
            data = json.load(jfile)

            for _ in range(14):
                try:
                    cases = data[county]['dates'][date]['cases'] - data[county]['dates'][date2]['cases']
                    if cases < 0:
                        cases = 0
                    return cases

                except KeyError:
                    # if information for this date does not exist - go back by one day and try again
                    date = str(datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1))[:10]
                    date2 = str(datetime.strptime(date2, "%Y-%m-%d") - timedelta(days=1))[:10]
                    continue

        # if no data is found - caseload is negligible - assume 0 cases
        return 0

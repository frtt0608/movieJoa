import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize, StandardScaler
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
import requests
import json

API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

# cmap = "tab10"
def user_hcluster():
    # 데이터 전처리
    data = pd.read_csv("./user_clu.csv")
    label = pd.DataFrame(data['user_pk'])
    data = data[['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
    data_scaled = normalize(data)
    df = pd.DataFrame(data_scaled)
    # 데이터 모델링
    for n in range(3, 8):
        model = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='ward').fit(df)
        y_predict = model.fit_predict(df)
        header = 'H' + str(n)
        label[header] = y_predict
    request_data = {'clustering': []}
    for lab in label.values:
        request_data['clustering'].append({
                'user_pk': str(lab[0]+1),
                'H3': str(lab[1]),
                'H4': str(lab[2]),
                'H5': str(lab[3]),
                'H6': str(lab[4]),
                'H7': str(lab[5])
        })
    print(request_data)
    response = requests.post(API_URL + 'cluster/hcluster/user/', data=json.dumps(request_data), headers=headers)
    print(response.text)

def movie_hcluster():
    # 데이터 전처리
    data = pd.read_csv("./movie_clu.csv")
    label = pd.DataFrame(data['title'])
    data = data[['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
    data_scaled = StandardScaler().fit_transform(data)
    df = pd.DataFrame(data_scaled)
    # 데이터 모델링
    for n in range(3, 8):
        model = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='ward').fit(df)
        y_predict = model.fit_predict(df)
        header = 'H' + str(n)
        label[header] = y_predict
    request_data = {'clustering': []}
    for lab in label.values:
        request_data['clustering'].append({
                'title': str(lab[0]),
                'H3': str(lab[1]),
                'H4': str(lab[2]),
                'H5': str(lab[3]),
                'H6': str(lab[4]),
                'H7': str(lab[5])
        })
    # print(request_data)
    response = requests.post(API_URL + 'cluster/hcluster/movie/', data=json.dumps(request_data), headers=headers)
    print(response.text)

if __name__ == '__main__':
    user_hcluster()
    # movie_hcluster()

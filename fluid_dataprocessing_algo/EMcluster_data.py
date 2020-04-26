import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import normalize, StandardScaler
import requests
import json

API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

# cmap = "tab10"
def user_emcluster():
    # 데이터 전처리
    data = pd.read_csv("./user_clu.csv")
    label = pd.DataFrame(data['user_pk'])
    data = data[['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
    data_scaled = normalize(data)
    df = pd.DataFrame(data_scaled)
    # 데이터 모델링
    for n in range(3, 8):
        model = GaussianMixture(n_components=n, max_iter=20, random_state=0, covariance_type='spherical').fit(df)
        y_predict = model.fit_predict(df)
        header = 'EM' + str(n)
        label[header] = y_predict
    request_data = {'clustering': []}
    for lab in label.values:
        request_data['clustering'].append({
                'user_pk': str(lab[0]+1),
                'EM3': str(lab[1]),
                'EM4': str(lab[2]),
                'EM5': str(lab[3]),
                'EM6': str(lab[4]),
                'EM7': str(lab[5])
        })
    # print(request_data)
    response = requests.post(API_URL + 'cluster/emcluster/user/', data=json.dumps(request_data), headers=headers)
    print(response.text)

def movie_emcluster():
    # 데이터 전처리
    data = pd.read_csv("./movie_clu.csv")
    label = pd.DataFrame(data['title'])
    data = data[['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
    data_scaled = StandardScaler().fit_transform(data)
    df = pd.DataFrame(data_scaled)
    # 데이터 모델링
    for n in range(3, 8):
        model = GaussianMixture(n_components=n, max_iter=20, random_state=0, covariance_type='spherical').fit(df)
        y_predict = model.fit_predict(df)
        header = 'EM' + str(n)
        label[header] = y_predict
    request_data = {'clustering': []}
    for lab in label.values:
        request_data['clustering'].append({
                'title': str(lab[0]),
                'EM3': str(lab[1]),
                'EM4': str(lab[2]),
                'EM5': str(lab[3]),
                'EM6': str(lab[4]),
                'EM7': str(lab[5])
        })
    # print(request_data)
    response = requests.post(API_URL + 'cluster/emcluster/movie/', data=json.dumps(request_data), headers=headers)
    print(response.text)

if __name__ == '__main__':
    user_emcluster()
    # movie_emcluster()

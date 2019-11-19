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
def matrix_factorization():
    response = requests.get(API_URL + 'matrix/', headers=headers)
    

if __name__ == '__main__':
    matrix_factorization()

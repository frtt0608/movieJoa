# 임시저장
# 클러스터 저장
def CheckCluster(cluster, Movies, Nearest_movie):
  way = "EM"
  k = cluster.n_component
  if way=="EM":
    Movies_scaled = normalize(Movies)
    df = pd.DataFrame(Movies_scaled)
    model = GaussianMixture(n_components=k, max_iter=20, random_state=0, covariance_type='spherical').fit(df)
    predict = model.fit_predict(df)
  elif way=="H":
    Movies_scaled = StandardScaler().fit_transform(Movies)
    df = pd.DataFrame(Movies_scaled)
    model = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward').fit(df)
    predict = model.fit_predict(df)
  elif way=="K":
    df = pd.DataFrame(Movies)
    model = KMeans(n_clusters=3, algorithm='auto').fit(df)
    predict = model.labels_

  clu_list = [0 for i in range(k+1)]
  for pk in Nearest_movie:
    clu_list[predict[pk-1]] += 1;
  input_movie_cluster = clu_list.index(max(clu_list))
  cluster_list = [];
  for i in range(len(predict)):
    if predict[i]==3: cluster_list.append(i+1)
  tmp = random.sample(list(cluster_list), 10)
  print(tmp)

# csv에 행 추가하기
import csv
scores = [3.96,4.0,4.0,4.0,3.77,0,0,4.0,4.5,0,2.67,4.0,3.0,3.8,3.83,3.8,4.0,4.67]
pk = 6041
scores.append(pk)
f = open('user_clu.csv', 'a', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(scores)
f.close()
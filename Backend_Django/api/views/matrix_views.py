import numpy as np
from rest_framework.decorators import api_view
from api.models import Movie, Rate, Profile, Matrix
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

movies = Movie.objects.all()
none = [x for x in range(1, movies[Movie.objects.count()-1].id+1)]

class MatrixFactorization():
    def __init__(self, R, k, learning_rate, reg_param, epochs, verbose=False):
        """
        :param R: rating matrix
        :param k: latent parameter
        :param learning_rate: alpha on weight update
        :param reg_param: beta on weight update
        :param epochs: training epochs
        :param verbose: print status
        """

        self._R = R
        self._num_users, self._num_items = R.shape
        self._k = k
        self._learning_rate = learning_rate
        self._reg_param = reg_param
        self._epochs = epochs
        self._verbose = verbose


    def fit(self):
        """
        training Matrix Factorization : Update matrix latent weight and bias

        참고: self._b에 대한 설명
        - global bias: input R에서 평가가 매겨진 rating의 평균값을 global bias로 사용
        - 정규화 기능. 최종 rating에 음수가 들어가는 것 대신 latent feature에 음수가 포함되도록 해줌.

        :return: training_process
        """

        # init latent features
        self._P = np.random.normal(size=(self._num_users, self._k))
        self._Q = np.random.normal(size=(self._num_items, self._k))

        # init biases
        self._b_P = np.zeros(self._num_users)
        self._b_Q = np.zeros(self._num_items)
        self._b = np.mean(self._R[np.where(self._R != 0)])

        # train while epochs
        self._training_process = []
        for epoch in range(self._epochs):

            # rating이 존재하는 index를 기준으로 training
            for i in range(self._num_users):
                for j in range(self._num_items):
                    if self._R[i, j] > 0:
                        self.gradient_descent(i, j, self._R[i, j])
            cost = self.cost()
            self._training_process.append((epoch, cost))

            # print status
            if self._verbose == True and ((epoch + 1) % 10 == 0):
                print("Iteration: %d ; cost = %.4f" % (epoch + 1, cost))


    def cost(self):
        """
        compute root mean square error
        :return: rmse cost
        """

        # xi, yi: R[xi, yi]는 nonzero인 value를 의미한다.
        # 참고: http://codepractice.tistory.com/90
        xi, yi = self._R.nonzero()
        predicted = self.get_complete_matrix()
        cost = 0
        for x, y in zip(xi, yi):
            cost += pow(self._R[x, y] - predicted[x, y], 2)
        return np.sqrt(cost) / len(xi)


    def gradient(self, error, i, j):
        """
        gradient of latent feature for GD

        :param error: rating - prediction error
        :param i: user index
        :param j: item index
        :return: gradient of latent feature tuple
        """

        dp = (error * self._Q[j, :]) - (self._reg_param * self._P[i, :])
        dq = (error * self._P[i, :]) - (self._reg_param * self._Q[j, :])
        return dp, dq


    def gradient_descent(self, i, j, rating):
        """
        graident descent function

        :param i: user index of matrix
        :param j: item index of matrix
        :param rating: rating of (i,j)
        """

        # get error
        prediction = self.get_prediction(i, j)
        error = rating - prediction

        # update biases
        self._b_P[i] += self._learning_rate * (error - self._reg_param * self._b_P[i])
        self._b_Q[j] += self._learning_rate * (error - self._reg_param * self._b_Q[j])

        # update latent feature
        dp, dq = self.gradient(error, i, j)
        self._P[i, :] += self._learning_rate * dp
        self._Q[j, :] += self._learning_rate * dq


    def get_prediction(self, i, j):
        """
        get predicted rating: user_i, item_j
        :return: prediction of r_ij
        """
        return self._b + self._b_P[i] + self._b_Q[j] + self._P[i, :].dot(self._Q[j, :].T)


    def get_complete_matrix(self):
        """
        computer complete matrix PXQ + P.bias + Q.bias + global bias

        - PXQ 행렬에 b_P[:, np.newaxis]를 더하는 것은 각 열마다 bias를 더해주는 것
        - b_Q[np.newaxis:, ]를 더하는 것은 각 행마다 bias를 더해주는 것
        - b를 더하는 것은 각 element마다 bias를 더해주는 것

        - newaxis: 차원을 추가해줌. 1차원인 Latent들로 2차원의 R에 행/열 단위 연산을 해주기위해 차원을 추가하는 것.

        :return: complete matrix R^
        """
        # 소수점을 없애기 위해 반올림한 평점으로 구성한다.
        return self._b + self._b_P[:, np.newaxis] + self._b_Q[np.newaxis:, ] + self._P.dot(self._Q.T)


    def print_results(self):
        """
        print fit results
        """
        """
        print("User Latent P:")
        print(self._P)
        print("Item Latent Q:")
        print(self._Q.T)
        print("P x Q:")
        print(self._P.dot(self._Q.T))
        print("bias:")
        print(self._b)
        print("User Latent bias:")
        print(self._b_P)
        print("Item Latent bias:")
        print(self._b_Q)
        print("Final RMSE:")
        print(self._training_process[self._epochs-1][1])
        """
        # 결과 매트릭스를 DB에 저장하기
        # print("Final R matrix:")
        # print(self.get_complete_matrix())
        result = self.get_complete_matrix().tolist()
        tmp = self._R.tolist()
        for i in range(1, len(result[0])):
            user = i
            movie_list = []
            for j in range(1, len(result)):
                if (j in none) or (tmp[j][i] != 0):
                    pass
                else:
                    movie_list.append((result[j][i], j))
            movie_list.sort()
            movie1 = Movie.objects.get(id=movie_list[0][1])
            movie2 = Movie.objects.get(id=movie_list[1][1])
            movie3 = Movie.objects.get(id=movie_list[2][1])
            movie4 = Movie.objects.get(id=movie_list[3][1])
            movie5 = Movie.objects.get(id=movie_list[4][1])
            movie6 = Movie.objects.get(id=movie_list[5][1])
            movie7 = Movie.objects.get(id=movie_list[6][1])
            movie8 = Movie.objects.get(id=movie_list[7][1])
            movie9 = Movie.objects.get(id=movie_list[8][1])
            movie10 = Movie.objects.get(id=movie_list[9][1])
            Matrix(UserID=Profile.objects.get(user=User.objects.get(pk=user)), Movie1=movie1, Movie2=movie2, Movie3=movie3, Movie4=movie4, Movie5=movie5, Movie6=movie6, Movie7=movie7, Movie8=movie8, Movie9=movie9, Movie10=movie10).save()
                
                
                
        


@api_view(['GET'])
def matrix_factorization(request):
    
    ratings = [[0 for _ in range(Profile.objects.count()+1)] for _ in range(movies[Movie.objects.count()-1].id+1)]
    print(none)
    for movie in movies:
        tmp = movie.profile_movie.all()
        idx = movie.id
        none.remove(idx)
        if tmp:
            for t in tmp:
                ratings[idx][t.UserID.pk] = t.rating
       
    factorizer = MatrixFactorization(np.array(ratings), k=3, learning_rate=0.01, reg_param=0.01, epochs=300, verbose=True)
    factorizer.fit()
    factorizer.print_results()
    return Response(status=status.HTTP_200_OK)
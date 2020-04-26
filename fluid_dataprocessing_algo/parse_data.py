import requests
import json

API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

def create_users():
    user_data = open('./users.dat', 'r', encoding='ISO-8859-1')
    request_data = {'profiles': []}
    occupation_map = {
        0: "other", 1: "academic/educator", 2: "artist", 3: "clerical/admin", 4: "college/grad student",
        5: "customer service", 6: "doctor/health care", 7: "executive/managerial", 8: "farmer", 9: "homemaker",
        10: "K-12 student", 11: "lawyer", 12: "programmer", 13: "retired", 14: "sales/marketing",
        15: "scientist", 16:  "self-employed", 17: "technician/engineer", 18: "tradesman/craftsman",
        19: "unemployed", 20: "writer"
    }

    for line in user_data.readlines():
        [userid, gender, age, occupation, zipcode] = line.split('::')

        username = 'user' + userid
        age = int(age)
        occupation = occupation_map[int(occupation)]

        request_data['profiles'].append({
            'username': username,
            'password': username,
            'age': age,
            'gender': gender,
            'occupation': occupation
        })
    # print(request_data['profiles'][0])
    # print(len(request_data['profiles']))

    response = requests.post(API_URL + 'auth/signup-many/', data=json.dumps(request_data), headers=headers)
    print(response.text)


def create_movies():
    movie_data = open('./movies.dat', 'r', encoding='ISO-8859-1')
    request_data = {'movies': []}
    for line in movie_data.readlines():
        [id, title, genres] = line.split('::')
        genres = genres[:-1].split('|')
        request_data['movies'].append({
            'id': id,
            'title': title,
            'genres': genres
        })

    response = requests.post(API_URL + 'movies/', data=json.dumps(request_data), headers=headers)
    print(response.text)


def create_ratings(num_users):
    rating_data = open('./ratings.dat', 'r', encoding='ISO-8859-1')
    request_data = {'ratings':[]}

    # 이건 중간 자르기 버전.
    # for line in rating_data.readlines():
    #     [UserID, MovieID, Rating, Timestamp] = line.split('::')
    #     if int(UserID) > num_users :
    #         # print(request_data)
    #         response = requests.post(API_URL + 'ratings/', data=json.dumps(request_data), headers=headers)
    #         print(response.text)
    #         return
    #
    #     else:
    #         request_data['ratings'].append({
    #             'UserID':UserID,
    #             'MovieID':MovieID,
    #             'Rating':Rating,
    #             'Timestamp':Timestamp
    #         })

    for line in rating_data.readlines():
        [UserID, MovieID, Rating, Timestamp] = line.split('::')

        request_data['ratings'].append({
            'UserID':UserID,
            'MovieID':MovieID,
            'Rating':Rating,
            'Timestamp':Timestamp
        })
    response = requests.post(API_URL + 'ratings/', data=json.dumps(request_data), headers=headers)
    print(response.text)

    '''
    UserID::MovieID::Rating::Timestamp
    1::1193::5::978300760
    1::661::3::978302109
    1::914 ::3::978301968
    1::3408::4::978300275
    1::2355::5::978824291
    1::1197::3::978302268
    1::1287::5::978302039
    1::2804::5::978300719
    1::594::4::978302268
    6040
    '''



if __name__ == '__main__':
    # num_users = 6040
    # create_movies()
    # create_users()
    # create_ratings()
    pass
from math import sqrt
from numpy import average

from Collaborative.Dataset import saveFileToPickle


# calculates cosine similiraty of two given vectors
def cosine_similarity(vector1, vector2, data_dict):
    if not (vector1 in data_dict and vector2 in data_dict):
        return 0

    sum_of_eclidean_distance = []

    for item in data_dict[vector1]:
        if item in data_dict[vector2]:
            sum_of_eclidean_distance.append(data_dict[vector1][item] * data_dict[vector2][item])

    if(len(sum_of_eclidean_distance)==0):
        return 0

    person_1_sum_square = sum([pow (data_dict[vector1][item], 2) for item in data_dict[vector1]])
    person_2_sum_square = sum([pow (data_dict[vector2][item], 2) for item in data_dict[vector2]])

    sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

    return (sum_of_eclidean_distance/(sqrt(person_1_sum_square)*sqrt(person_2_sum_square)))



# calculates cosine similiraty of two given vectors
def pearson_similarity(vector1, vector2, data_dict):

    if not (vector1 in data_dict and vector2 in data_dict):
        return 0
    person1_dataset = data_dict[vector1]
    person2_dataset=data_dict[vector2]

    both_rated = {}
    for item in person1_dataset:
        if item in person2_dataset:
            both_rated[item] = 1

    person1_preferences_sum = average([person1_dataset[item] for item in person1_dataset])
    person2_preferences_sum = average([person2_dataset[item] for item in person2_dataset])

    person1_square_preferences_sum = sum([pow((person1_dataset[item]-person1_preferences_sum), 2) for item in both_rated])
    person2_square_preferences_sum = sum([pow((person2_dataset[item]-person2_preferences_sum), 2) for item in both_rated])

    product_sum_of_both_users = sum([(person1_dataset[item]-person1_preferences_sum) * (person2_dataset[item]-person2_preferences_sum) for item in both_rated])

    if(product_sum_of_both_users==0 or person1_square_preferences_sum==0 or person2_square_preferences_sum==0):
        return 0

    # Calculate the pearson score
    similarity = product_sum_of_both_users / sqrt(person2_square_preferences_sum * person1_square_preferences_sum)

    return similarity



# returns a sorted list of items based on the given similarity function
def most_similar_users(person, sim_type, data_dict):

    scores=[]

    if (sim_type == 'pearson'):
        scores = [(pearson_similarity(person, other_person, data_dict), other_person) for other_person in data_dict if
                  other_person != person]

    elif (sim_type == 'cosine'):
        scores = [(cosine_similarity(person, other_person, data_dict), other_person) for other_person in data_dict if
                  other_person != person]

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()

    return scores



# returns the predicted rating of the given user for the given item
def predict_score(active_user, item, type, user_based_dict, item_based_dict, k_array):
    user_rate = []

    if (active_user in user_based_dict and item in item_based_dict ):
        sim_users = most_similar_users(active_user, type, user_based_dict)

        for k in k_array:
            index = 0
            score = []

            for element in sim_users:
                user = element[1]
                sim_rate = element[0]

                if (sim_rate == 0):
                    if(index<=0):
                        user_score=average([user_based_dict[active_user][elm] for elm in user_based_dict[active_user] ])
                        score.append((1,user_score))
                    break

                if (item in user_based_dict[user]):
                    index += 1
                    score.append((sim_rate, user_based_dict[user][item]))

                if (index == k):
                    break

            user_rate.append(calculate_rate(score))
        return user_rate

    elif not (active_user in user_based_dict):
        if (item in item_based_dict):

            item_score= average([item_based_dict[item][elm] for elm in item_based_dict[item] ])

            for k in k_array:
                user_rate.append(item_score)
            print(user_rate)
            return user_rate

    elif not (item in item_based_dict):

        item_score = average([user_based_dict[active_user][elm] for elm in user_based_dict[active_user]])

        for k in k_array:
            user_rate.append(item_score)
        print(user_rate)
        return user_rate


    for k in k_array:
        user_rate.append(0)
    print(user_rate)

    return user_rate



# calculates score of an item based on similar users or items and their similarities
def calculate_rate(score):

    sum_of_similarities = sum([item[0] for item in score])
    sum_of_scores = sum([item[0] * item[1] for item in score])

    if (sum_of_scores == 0):
        return 0

    return sum_of_scores / (sum_of_similarities)



# evaluates predicted rates with RMSE indicator based on given different Ks and saves the 'results' in given path
def evaluate(k_array, results, totalCount, path):

    length = len(k_array)
    saveFileToPickle(path, results)

    for i in range(0, length):

        sum_square = sum([pow(item[0] - item[1][i], 2) for item in results])

        RMSE = sum_square / totalCount

        print('RMSE for K = ' + str(k_array[i]) + " is: " + str(RMSE))

        print(RMSE)

    return
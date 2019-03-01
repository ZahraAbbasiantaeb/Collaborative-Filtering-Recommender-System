from Collaborative.Dataset import test_DF, item_based_dict, user_based_dict
from Collaborative.algorithms import predict_score, evaluate

length= len(test_DF)
k_array=[10,15,20]
results=[]

# this part calculates rating, and RMSE for each item based on item-based model

for i in range(0, length):

    active_user = test_DF.iloc[i, 0]

    item = test_DF.iloc[i, 1]

    score = test_DF.iloc[i, 2]

    user_scores = predict_score(item, active_user, 'pearson', item_based_dict, user_based_dict, k_array)
    print(i)

    results.append((score,user_scores))

evaluate(k_array, results, length, 'item-pearson-2.pkl')

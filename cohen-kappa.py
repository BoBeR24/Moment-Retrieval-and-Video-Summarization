from sklearn.metrics import cohen_kappa_score

print("Video 25")
rater_a = [2, 1, -2, -1, 2]
rater_b = [1, 2, -2, 2, -2]

kappa = cohen_kappa_score(rater_a, rater_b)
print(kappa)

print("Video 26")
rater_a = [1, 2]
rater_b = [2, 2]

kappa = cohen_kappa_score(rater_a, rater_b)
print(kappa)

print("Video 27")
rater_a = [1, 2, 1, 0, 2, -2, 1]
rater_b = [2, 2, 1, 2, 1, 1, 2]

kappa = cohen_kappa_score(rater_a, rater_b)
print(kappa)

print("Video 28")
rater_a = [-1, 2, 2, 1, -2, -1]
rater_b = [-1, 1, 2, 2, 2, 1]

kappa = cohen_kappa_score(rater_a, rater_b)
print(kappa)
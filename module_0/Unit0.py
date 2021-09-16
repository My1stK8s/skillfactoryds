#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
def number():
    from random import random
    return (1+random()*100)
def game_core_v3(number):
    count = 0
    minpoint = 1
    maxpoint = 100
    predict = np.random.randint(1,101)
    while count<100 and number != predict:
        count+=1
        if number > predict: 
            minpoint = predict
        elif number < predict: 
            maxpoint = predict
        predict = (minpoint+maxpoint)//2
    return (count)

def score_game(game_core):
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)
score_game(game_core_v3)


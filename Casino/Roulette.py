# -*- coding: utf-8 -*-
"""
Created on Fri May 25 17:06:38 2018

@author: jeff.tsai
"""
import pandas as pd
import numpy as np

# one_round
def one_round(n,red,black,big,small,odd,even):
    nums = ['0','r','b','r','b','r','b','r','b','r','b', #  0-10
            'b','r','b','r','b','r','b','r','r','b', # 11-20
            'r','b','r','b','r','b','r','b','b','r', # 21-30
            'b','r','b','r','b','r']# 31-36
    if n == 0:
        return -sum([red,black,big,small,odd,even])
    win = ((red*(nums[n]=='r') + black*(nums[n]=='b')+
          big*(n > 18) + small*(n<19) +
          odd*(n%2==1) + even*(n%2==0))*2-sum([red,black,big,small,odd,even]))
    return win

# Roulette function
def roulette(coin,num_round,threshold_times):
    nums = ['0','r','b','r','b','r','b','r','b','r','b', #  0-10
            'b','r','b','r','b','r','b','r','r','b', # 11-20
            'r','b','r','b','r','b','r','b','b','r', # 21-30
            'b','r','b','r','b','r'] # 31-36
    table = []
    u_red,u_black,u_big,u_small,u_odd,u_even = [1]*6
    c_red,c_black,c_big,c_small,c_odd,c_even = [0]*6
    for i in range(num_round):
        # bet
        n = np.random.randint(0,37)
        flow = one_round(n, u_red * (c_black >= threshold_times),
                            u_black * (c_red >= threshold_times),
                            u_big * (c_small >= threshold_times),
                            u_small * (c_big >= threshold_times),
                            u_odd * (c_even >= threshold_times),
                            u_even * (c_odd >= threshold_times))
        # counter , unit
        if n != 0:
            # count consecutive events
            c_red = (c_red + (nums[n]=='r')) * (nums[n]=='r')
            c_black = (c_black + (nums[n]=='b')) * (nums[n]=='b')
            c_big = (c_big + (n > 18)) * (n > 18)
            c_small = (c_small + (n <= 18)) * (n <= 18)
            c_odd = (c_odd + (n%2==1)) * (n%2==1) 
            c_even = (c_even + (n%2==0)) * (n%2==0)
            # units adjusted
            u_red  =u_red*2   if (nums[n]=='b') * (c_black > threshold_times) else 1
            u_black=u_black*2 if (nums[n]=='r') * (c_red > threshold_times) else 1
            u_big  =u_big*2   if (n <= 18) * (c_small > threshold_times) else 1
            u_small=u_small*2 if (n >= 19) * (c_big > threshold_times) else 1
            u_odd  =u_odd*2   if (n%2==0) * (c_even > threshold_times) else 1
            u_even =u_even*2  if (n%2==1) * (c_odd > threshold_times) else 1
            # state
            s = ('Red'*(nums[n]=='r')+'Black'*(nums[n]=='b')+','+
                 'Big'*(n>18)+'Small'*((n>0)*(n<19))+','+
                 'Odd'*(n%2==1)+'Even'*(n%2==0))
        else:
            u_red,u_black,u_big,u_small,u_odd,u_even = [1]*6
            c_red,c_black,c_big,c_small,c_odd,c_even = [0]*6
            s = '0'
        # table
        coin += flow
        bet = sum([u_red*(c_black >= threshold_times),u_black*(c_red >= threshold_times),
                   u_big*(c_small >= threshold_times),u_small*(c_big >= threshold_times),
                   u_odd*(c_even >= threshold_times),u_even*(c_odd >= threshold_times)])
        table += [[i+1,n,s,coin,bet,flow,
                   u_red*(c_black >= threshold_times),c_black,
                   u_black*(c_red >= threshold_times),c_red,
                   u_big*(c_small >= threshold_times),c_small,
                   u_small*(c_big >= threshold_times),c_big,
                   u_odd*(c_even >= threshold_times),c_even,
                   u_even*(c_odd >= threshold_times),c_odd]]
        if coin < bet:
            break
    # Dataframe
    table = pd.DataFrame(table, columns=['Round','Number','State','Coin','Bet','CashFlow',
                                         'u_Red','c_Black','u_Black','c_Red',
                                         'u_Big','c_Small','u_Small','c_Big',
                                         'u_Odd','c_Even','u_Even','c_Odd'])
    for i in ['u_Red','u_Black','u_Big','u_Small','u_Odd','u_Even']:
        table[i] = table[i].shift(1)
    return table
# Function Ending Line
a = roulette(100,1000,5)
sum(a['CashFlow'])


# experiment
coin = 100
num_round = 1000
threshold_times = 5
result = pd.DataFrame(columns=['i','Round','Coin','Bet'])
for i in range(10000):
    if i%1000==0 : print(i,end=',')
    temp = roulette(coin,num_round,threshold_times)[-1:][['Round','Coin','Bet']]
    temp['i'] = i
    result = pd.concat([result,temp],sort=False,ignore_index=True)
for i in list(result):
    result[i] = pd.to_numeric(result[i])
    # experiment result
print('There are',sum(result['Round'] == num_round),'times safe after',num_round,'rounds,')


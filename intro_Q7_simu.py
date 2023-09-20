"""
#My first app
Here's our first attempt
"""

import streamlit as st
import pandas as pd
# import numpy as np
import random
import time

# functions
def game(door, method = 'not_random'):
    '''
    used to describe director, guest and host choice
    method = 'random' : host random chooses which door to open
    '''
    car_loc = random.choice(door)
    guest_choice = random.choice(door)
    door.remove(guest_choice)  # drop guest_choice
    if method == 'random':
        host_choice = random.choice(door)
    else:
        if car_loc == guest_choice:
            host_choice = random.choice(door)
        else:
            door.remove(car_loc)
            host_choice = door[0]
    return [car_loc, guest_choice, host_choice]


# Simulation 
def result_simu(simu_round, method='not_random'):
    '''
    if method = 'random', then host choose door randomly
    default method = 'not_random'
    '''
    result = []
    for i in range(0,simu_round):
        door = list('ABC')
        result.append(game(door, method = method))
    result_table = pd.DataFrame(result, columns=['car_loc', 'guest_choice', 'host_choice'])
    result_table['no choice change'] = result_table.apply(lambda x: 1 if x['car_loc'] == x['guest_choice'] else 0, axis = 1)
    result_table['drop-times'] = 0
    if method == 'random':
        result_table['drop-times'] = result_table.apply(lambda x: 1 if x['car_loc'] == x['host_choice'] else 0, axis = 1)
    win_rate = sum(result_table['no choice change'])/(result_table.shape[0]-sum(result_table['drop-times']))
    return win_rate, result_table

# run game
st.title("Let's Make a Deal")

st.image("https://tingwen-pic.oss-cn-beijing.aliyuncs.com/img/20230920193210.png")


method = st.selectbox(
    'which assumption do you want to select?',
    ('Host opens door purposefully', 'Host opens doors randomly'),
    index = 0)

st.write("")

simu_round = st.number_input(
    'how many rounds do you want to play?',
    min_value = 1, max_value = 100000000, 
    value = 20)
simu_round = int(simu_round)

def open_method(method):
    if method == 'Host opens door purposefully':
        return 'not_random'
    else:
        return 'random'

if st.button("RUN", type = "primary"):
    win_rate, table = result_simu(simu_round, open_method(method))
    with st.spinner('Processing...'):
        time.sleep(3)
    
    st.write("")
    
    # print winning rate
    if method == 'Host opens door purposefully':
        st.write('**在主持人知道哪个门后面有车的情况下，嘉宾改变选择，获胜的概率为**: {:.2f}'.format(1-win_rate))
    elif method == 'Host opens doors randomly':
        st.write('**在主持人不知道哪个门后面有车的情况下，嘉宾改变选择，获胜的概率为**: {:.2f}'.format(1-win_rate))
    else:
        st.warning('Something is Wrong!!!')
    st.balloons()
    
st.write("")


code = """
import streamlit as st
import pandas as pd
# import numpy as np
import random
import time

# functions
def game(door, method = 'not_random'):
    '''
    used to describe director, guest and host choice
    method = 'random' : host random chooses which door to open
    '''
    car_loc = random.choice(door)
    guest_choice = random.choice(door)
    door.remove(guest_choice)  # drop guest_choice
    if method == 'random':
        host_choice = random.choice(door)
    else:
        if car_loc == guest_choice:
            host_choice = random.choice(door)
        else:
            door.remove(car_loc)
            host_choice = door[0]
    return [car_loc, guest_choice, host_choice]


# Simulation 
def result_simu(simu_round, method='not_random'):
    '''
    if method = 'random', then host choose door randomly
    default method = 'not_random'
    '''
    result = []
    for i in range(0,simu_round):
        door = list('ABC')
        result.append(game(door, method = method))
    result_table = pd.DataFrame(result, columns=['car_loc', 'guest_choice', 'host_choice'])
    result_table['no choice change'] = result_table.apply(lambda x: 1 if x['car_loc'] == x['guest_choice'] else 0, axis = 1)
    result_table['drop-times'] = 0
    if method == 'random':
        result_table['drop-times'] = result_table.apply(lambda x: 1 if x['car_loc'] == x['host_choice'] else 0, axis = 1)
    win_rate = sum(result_table['no choice change'])/(result_table.shape[0]-sum(result_table['drop-times']))
    return win_rate, result_table

# run game
st.title("Let's Make a Deal")

st.image("https://tingwen-pic.oss-cn-beijing.aliyuncs.com/img/20230920193210.png")


method = st.selectbox(
    'which assumption do you want to select?',
    ('Host opens door purposefully', 'Host opens doors randomly'),
    index = 0)

st.write("")

simu_round = st.number_input(
    'how many rounds do you want to play?',
    min_value = 1, max_value = 100000000, 
    value = 20)
simu_round = int(simu_round)

def open_method(method):
    if method == 'Host opens door purposefully':
        return 'not_random'
    else:
        return 'random'

if st.button("RUN", type = "primary"):
    win_rate, table = result_simu(simu_round, open_method(method))
    with st.spinner('Processing...'):
        time.sleep(3)
    
    st.write("")
    
    # print winning rate
    if method == 'Host opens door purposefully':
        st.write('**在主持人知道哪个门后面有车的情况下，嘉宾改变选择，获胜的概率为**: {:.2f}'.format(1-win_rate))
    elif method == 'Host opens doors randomly':
        st.write('**在主持人不知道哪个门后面有车的情况下，嘉宾改变选择，获胜的概率为**: {:.2f}'.format(1-win_rate))
    else:
        st.warning('Something is Wrong!!!')
"""

on = st.toggle("Show Code")

if on:
    st.code(code, language = 'python')
    
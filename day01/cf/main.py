import numpy as np
from load_data import create_user_item_click,create_user_item_score
from base_user import cal_allSim
from user_cf import predict_all_score_baseUser,predict_click_baseUser
import sys
import os
import time
def rec(top_item=30):

    #1.加载用户物品词典（可以放在hdfs中，hbase）
    if os.path.exists("result/user_item.txt"):
        with open("result/user_item.txt", "r+", encoding="utf-8") as f:
            user_item = eval(f.read())
    else:
        raise FileNotFoundError("please confirm your path")
    #2.加载用户相似矩阵（内存，广播）
    if os.path.exists("result/user_sim.txt"):
       with open("result/user_sim.txt","r+",encoding="utf-8") as f:
            sim_dict=eval(f.read())
    else:

        sim_dict = cal_allSim(user_item, method="jaccard")
        with open("result/user_sim.txt", "w+", encoding="utf-8") as f:
            f.write(str(sim_dict))

    return user_item,sim_dict
if __name__ == '__main__':

    top_item = 20
    user_item, sim_dict = rec(top_item)
    start = time.time()
    while True:
        uid = "1"
        item = predict_click_baseUser(uid, user_item, sim_dict, top_item)
    end=time.time()
    print((end-start))







from load_data import create_user_item_click,create_user_item_score
from base_user import cal_allSim
import time
import numpy as np
############################3.1预测评分




def predict_score_baseUser(uid,iid,user_item,sim_dict):
    """

    :param uid: 用户id
    :param iid: 未曝光的物品id
    :param user_item: 用户-物品评分表
    :param sim_dict: 用户相似矩阵
    :return:
    """
    ##1.基于用户uid,最相似的100个用户[i1,i4,...,i10,i11]
    user_sim=dict(sorted(sim_dict[uid].items(),key=lambda x:x[1],reverse=True)[:100])
    #temp1 用来存储 用户相似系数*score
    #temp2用来存储 用户相似系数做归一化
    temp1=0
    temp2=0
    #1.遍历与用uid相似的用户other_user_id和score
    for other_user_id,sim in user_sim.items():
        #如果其他用户没有iid这个物品，那么继续，我只需要
        if user_item[other_user_id].get(iid,-1)==-1:
            continue
        else:
            #拿到用户a的分数
            score=user_item[other_user_id][iid]
            #计算用户a的分数和相似度乘积
            temp1+=score*user_sim[other_user_id]
            #累加相似度，作为权重分布
            #（3*0.9+4*0.8+3*0.2）/（0.9+0.8+0.2）
            temp2+=user_sim[other_user_id]

    if temp2==0:
        return 0
    sims=np.around(temp1/temp2,2)
    # print("用户-%s对物品-%s的预测评分为%f" % (uid,iid,sims ))
    return sims
############################3.2隐式预测
def predict_click_baseUser(uid,user_item,sim_dict,top_item=200):
    #1.用户浏览过的物品
    uid_item=user_item[uid]
    #2.对相似用户进行排序
    uid_sim_otherid=sorted(sim_dict[uid].items(),key=lambda x:x[1],reverse=True)
    #2.找出用户的相似物品
    rec_item=set()

    for uid,value in uid_sim_otherid:
        item_set=set(user_item[uid])-uid_item
        rec_item=rec_item | item_set
        if len(rec_item)>top_item:
            return rec_item

def predict_all_score_baseUser(uid,user_item,item_set,sim_dict,top_item=100):
    """
    :param uid: 用户id
    :param user_item: 用户_物品词典
    :param item_set: 物品列表
    :param sim_dict: 用户相似词典
    :param top_item: 最相似的topk个物品推荐
    :return:
    """
    #过滤，找到用户没有评分的电影
    un_score_item=item_set-set(user_item[uid].keys())
    #推荐列表
    rec_item_dict={}
    #遍历用户没有看过的电影列表
    for iid in un_score_item:
        #计算该用户对iid 的评分预测为s
        s=predict_score_baseUser(uid, iid, user_item, sim_dict)
        #补齐s
        rec_item_dict[iid]=s
        print("用户:%s 对物品:%s 的预测评分为%f" % (uid, iid, rec_item_dict[iid]))
    #补全之后 做排序后推荐
    res=dict(sorted(rec_item_dict.items(),key=lambda x:x[1],reverse=True)[:top_item])
    return res

if __name__ == '__main__':
    path="data/ua.base"
    #读取数据，获取用户-商品评分矩阵（字典的形式存储），以及所有商品列表
    user_item, item_set=create_user_item_score(path)
    #获取用户相似性矩阵
    sim_dict=cal_allSim(user_item)
    #给用户推荐物品
    s=predict_all_score_baseUser("1",user_item,item_set,sim_dict,top_item=100)
    print(s)

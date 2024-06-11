
import numpy as np
from  load_data import  create_user_item_click
#1.计算两个用户的相似性
def sim_cos(u1_id,u2_id,user_item):
    """
    :param u1: uid
    :param u2: uid
    :return:相似度
    """
    # u1：{i1:3,i2:4,....}
    # u2:
    u1=user_item[u1_id]
    u2=user_item[u2_id]
    # 获取两个用户共同评分过的商品
    cor_index=u1.keys()&u2.keys()
    cross=0
    u1_score=0
    u2_score=0

    # u1:3,4,5  u2 2 3 5
    for iid in cor_index:
        cross+=u1[iid]*u2[iid]

        u1_score+=u1[iid]*u1[iid]
        u2_score+= u2[iid] * u2[iid]
    m=cross
    s=(np.sqrt(u1_score)*np.sqrt(u2_score))

    if s==0:
        return 0
    sim=m/s
    return sim
def sim_jaccard(u1_id,u2_id,user_item):
    #拿出u1 u2的集合，做交集，做并集，用交集的长度除以并集的长度得到jaccard距离
    #注意分母为0.
    u1_item=user_item[u1_id]
    u2_item=user_item[u2_id]
    m=len(u1_item & u2_item)
    n=len(u1_item | u2_item)
    if n==0:
        return 0
    else:
        return np.around(m/n,2)
#2.计算用户两两相似字典
def cal_allSim(user_item,method="cosin"):
    #初始一个用户相似词典
    sim_dict={}
    # {u1:{u2:0.91,u3:0.81}}
    #遍历用户去计算用户的两两相似
    for u1 in user_item.keys():
        for u2 in user_item.keys():
            #如果用户id一样，意味着用户是同一个，因此，不用计算，直接跳过。
            if u1==u2:
                continue
            # 如果两个用户id不一样，那么计算用户相似
            else:
                #如果sim_dict字典中没有u1的key，那么基于get进行初始化，然后计算u1 和u2 的相似度
                if sim_dict.get(u1,-1)==-1:
                    #用cos 夹角余玄方法
                    if method=="cosin":
                        #此处自己实现了一个sim_cos的方法
                        sim_dict[u1]={u2:sim_cos(u1,u2,user_item)}
                    #用jaccard方法
                    elif method=="jaccard":
                        # 此处自己实现了一个sim_jaccard的方法
                        sim_dict[u1] = {u2: sim_jaccard(u1, u2, user_item)}
                    else:
                        raise ("请输入正确相似度计算方法")
                # 如果sim_dict字典中有u1的key，那么直接计算相似度
                else:
                    if method == "cosin":
                        sim_dict[u1].update({u2:sim_cos(u1,u2,user_item)})
                    elif method=="jaccard":
                        sim_dict[u1].update({u2: sim_jaccard(u1, u2, user_item)})
                    else:
                        raise ("请输入正确相似度计算方法")
    #最终返回用户相似词典 {"u1":{"u2":0.5，"u3":0.04}}
    return sim_dict










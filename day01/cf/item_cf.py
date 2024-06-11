
import  numpy as np
"""
base item-cf
1.计算物品的相似性，此时需要倒排列表sim_dict
   2.1对于显示评分：（目的补全分数）
        1.找出用户(u1)打过分的物品[i1:4,i2:5]，和未打分的物品[i3,i4,i5]
        2.遍历每一个未打分的物品（i3,i4,i5）：以i3为例子
            2.1 对于这个物品找到 与 打过分物品的相似度 sim_dict[i3][i1]=0.3  sim_dict[i3][i2]=0.8
            2.2  基于每个相似度*对应的打分，最终得到部分
                score(i3)=sim_dict[i3][i1]*user_item[u1][i1]+sim_dict[i3][i2]*user_item[u1][i2]/(sim_dict[i3][i1]+sim_dict[i3][i2] )
                         =(4*0.3+5*0.8)/(0.3+0.8)=4.72
    2.2对于隐式评分：（推荐topk个）
        1.找出点击过的物品
        2.由于点击的物品，没有度量，此时可以看场景，
        遍历每一个用户未点击的物品，(此时为了用户不遍历所有的，可以引入比如曝光为未点击去除，时间阈值
        阶段等手段)[i3,i4] 跟用户点击物品[i1,i2]计算相似性。
        2.1 i3     sim[i3][i1]=0.3  sim[i3][i2]=0.7
        2.2  i3 rec_score=1 (0.21)
"""



def dis_jaccard(i1,i2):
    """
    think：物品如果是热门物品怎么办？是否可以做热门打压

    :param i1: set(用户)
    :param i2: set(用户)
    :return:

    """
    m = len(i1 & i2)
    n = len(i1 | i2)
    if n == 0:
        return 0
    else:
        return np.around(m / n, 2)


def get_item_sim_dict(item_user):

    sim_dict={}
    for iid1 ,uid1_set in item_user.items():
        for iid2, uid2_set in item_user.items():
            if iid1==iid2:
                continue
            else:
                if sim_dict.get(iid1,-1)==-1:
                    sim_dict[iid1]={iid2:dis_jaccard(uid1_set,uid2_set)}
                else:
                    sim_dict[iid1].update({iid2: dis_jaccard(uid1_set, uid2_set)})
    return sim_dict


def predict_iid_score(uid,iid,user_item,sim_dict):

    #1.用户已经点击的序列
    uid_click=user_item[uid]

    #2.遍历用户点击的序列并计算得分综合
    iid_score=0

    for uiid in uid_click:
        iid_score+=sim_dict[iid].get(uiid,0)
    return iid_score/len(uid_click)


def recommand(uid,user_item,sim_dict,all_item_set,top_item=20):

    uid_dict={}
    #拿出用户评价过的物品
    uid_click=user_item[uid]
    uid_unclick=all_item_set-uid_click
    for un_click_id in uid_unclick:
        uid_dict[un_click_id]=predict_iid_score(uid,un_click_id,user_item,sim_dict)

    re=dict(sorted(uid_dict.items(), key=lambda x: x[1], reverse=True)[:top_item])
    return re


def create_item_user_click(path):
    """
       主要是构建点击数据，输入是数据路径
       输出是用户-物品字典
       :param path:
       :return:
       """
    #初始化用户物品字典为空
    item_user = dict()
    user_item=dict()
    all_item_set=set()
    #相当于打开文件操作，做一个buffer
    with open(path, "r", encoding="utf-8") as f:
        #死循环，一行一行读取数据，知道读取完毕
        while True:
            #一行一行读数据 1	1	5	874965758
            line = f.readline()
            # 如果line不为空，则对line基于\t进行切分，得到[1,1,5,874965758]
            if line:
                lines = line.strip().split("\t")
                uid = lines[0]
                iid = lines[1]
                all_item_set.add(iid)
                # 初始化字典,get到uid就更新 如果uid不在字典中，那么初始化uid为
                #key，value为set(iid)
                if item_user.get(iid, -1) == -1:
                    item_user[iid] ={uid}
                else:
                    item_user[iid].add(uid)

                if user_item.get(uid, -1) == -1:
                    user_item[uid] = {iid}
                else:
                    user_item[uid].add(iid)

            #如果line为空，表示读取完毕，那么调出死循环。
            else:
                print("读完")
                break
    return item_user,user_item,all_item_set


if __name__ == '__main__':

    item_user,user_item,all_item_set=create_item_user_click("data/ua.base")

    #相似矩阵

    sim_dict=get_item_sim_dict(item_user)

    s=predict_iid_score("1","2",user_item,sim_dict)

    re=recommand("2", user_item, sim_dict, all_item_set, top_item=20)
    print(len(re))
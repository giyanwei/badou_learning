def create_user_item_click(path):
    """
       主要是构建点击数据，输入是数据路径
       输出是用户-物品字典
       :param path:
       :return:
       """
    #初始化用户物品字典为空
    user_item = dict()
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

                # 初始化字典,get到uid就更新 如果uid不在字典中，那么初始化uid为
                #key，value为set(iid)
                if user_item.get(uid, -1) == -1:
                    user_item[uid] ={iid}
                else:
                    user_item[uid].add(iid)
            #如果line为空，表示读取完毕，那么调出死循环。
            else:
                print("读完")
                break
    #         {u1:(i1,i3,i4,i8,i11),u2:(i9,i11,i12,i19)}
    return user_item
def create_user_item_score(path):

    #初始化用户物品字典为空
    user_item = dict()
    #为了保证物品测唯一，所以构建了set集合
    item_set=set()

    with open(path, "r", encoding="utf-8") as f:

        while True:
            line = f.readline()
            # print(line)
            if line:
                lines = line.strip().split("\t")
                uid = lines[0]
                iid = lines[1]
                score = int(lines[2])
                item_set.add(iid)
                # 初始化字典
                if user_item.get(uid, -1) == -1:
                    user_item[uid] = {iid: score}
                else:
                    user_item[uid].update({iid: score})

            else:
                print("读完")
                break
    # {u1: {i1:4, i3:2, i4:2, i8:1, i11:2}, }
    return user_item,item_set
































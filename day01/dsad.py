
user_click_list = [[1,3,4,5],
                   [2,3,4,5],
                   [4,5,89,231,41],
                   [123,2,3,4,5]]
dicts={}
for i in range(len(user_click_list)):
    tmp = user_click_list[i]
    # [1, 3, 4, 5]   [1,3] ,[3,4],[4,5]
    for j in range(1,len(tmp)):
        src_index = tmp[j-1]
        dsc_index =tmp[j]
        key=str(src_index)+"_"+str(dsc_index)
        if dicts.get(key,-1)==-1:
            dicts[key]=1
        else:
            dicts[key]+=1
print(dicts)


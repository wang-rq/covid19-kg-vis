import plotly.graph_objects as go
import urllib, json
import urllib.request
import pandas as pd
from collections import Counter
from pandas.core.frame import DataFrame
import re


data = pd.read_csv("/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/conditions.csv")
data2 = pd.read_csv("/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/patients1.csv")

data.sort_values(by=["PATIENT", "STOP"], inplace=True, ascending=[True,True])

data_new = data.groupby(['ENCOUNTER'])['DESCRIPTION'].apply(list).to_frame()
for index, row in data_new.iterrows():
    if row['DESCRIPTION'][0] != 'Suspected COVID-19':
        data_new = data_new.drop(index=index)
data_new.to_csv('/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/enc_samples.csv')
data_new.to_csv('/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/samples.csv')
data_new = pd.read_csv("/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/samples.csv")
print(data_new)
print(data2)
# data_new['PATIENT']=data_new['PATIENT'].astype(str)
# data2['PATIENT']=data2['PATIENT'].astype(str)
# print(data_new['PATIENT'].dtype)
# print(data2['PATIENT'].dtype)
# data_new = data_new.merge(data2, on = 'PATIENT')
# print(data_new)





res = []
for index, row in data_new.iterrows():
    des_list = row['DESCRIPTION'][1:-1].split(', ')
    # birth = int(row['BIRTHDATE'][0:4])
    # agebound = 60
    # if 2020 - birth > agebound:
    #     group = 'old'
    # else:
    #     group = 'young'
    # print(group)
    # print(des_list)
    if len(des_list) == 1:
        des = des_list[0][1:-1] + "_" + str(0)# + "_" + str(group)
        res.append((des, 'OK'))# + "_" + str(group)))
    for i in range(len(des_list)-1):
        # res.append((des_list[i], des_list[i+1]))
        des = des_list[i][1:-1] + "_" + str(i)# + "_" + str(group)
        des1 = des_list[i+1][1:-1] + "_" + str(i+1)# + "_" + str(group)
        res.append((des, des1))
        # print(des, des1)


count = Counter(res)
# print(count)

source_label = []
target_label = []
value = []

for item in count.items():
    source_label.append(item[0][0])
    target_label.append(item[0][1])
    value.append(item[1])

labels = list(set(source_label + target_label))
number = list(range(0,len(labels)))
index = dict(list(zip(labels, number)))

data_sankey = DataFrame({"source_label": source_label,
                        "target_label": target_label,
                        "value": value})
data_sankey["source"] = data_sankey["source_label"].map(index)
data_sankey["target"] = data_sankey["target_label"].map(index)

source = data_sankey["source"].tolist()
target = data_sankey["target"].tolist()

# print(labels)

# color_link = [
# '#D7BDE2', '#FAD7A0', '#AED6F1', '#CBB4D5', '#EBBAB5', 
# '#EBBAB5', '#FEF3C7', '#FEF3C7', '#A6E3D7', '#A6E3D7', 
# '#A6E3D7', '#A6E3D7', '#A6E3D7', '#A6E3D7', '#CBB4D5', 
# '#CBB4D5', '#CBB4D5', '#A6E3D7', '#D6E3D7', '#A6E3D7',
# '#CBB4D5', '#CBB4D5', '#CBB4D5', '#EBBAB5', '#FEF3C7',
# '#EBBAB5', '#FEF3C7', '#A6E3D7', '#CBB4D5', '#EBBAB5', 
# '#EBBAB5', '#FEF3C7', '#FEF3C7', '#A6E3D7', '#A6E3D7', 
# '#A6E3D7', '#A6E3D7', '#A6E3D7', '#A6E3D7', '#CBB4D5', 
# '#CBB4D5', '#CBB4D5', '#A6E3D7', '#D6E3D7', '#A6E3D7',
# '#CBB4D5', '#CBB4D5', '#CBB4D5', '#EBBAB5', '#FEF3C7',
# '#EBBAB5', '#FEF3C7', '#A6E3D7', '#CBB4D5', '#EBBAB5', 
# '#EBBAB5', '#FEF3C7', '#FEF3C7', '#A6E3D7', '#A6E3D7', 
# '#A6E3D7', '#A6E3D7', '#A6E3D7', '#A6E3D7', '#CBB4D5', 
# '#CBB4D5', '#CBB4D5', '#A6E3D7', '#D6E3D7']


color_link = [
'#EDBB99', '#ABEBC6', '#D6EAF8', '#CBB4D5', '#EBBAB5', 
'#EBBAB5', '#73C6B6', '#FEF3C7', '#A6E3D7', '#F5B7B1', 
'#F8C471', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9',
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9', 
'#ABB2B9', '#ABB2B9', '#ABB2B9', '#ABB2B9']



# data to dict, dict to sankey
link = dict(source = source, target = target, value = value)#, color=color_link)
node = dict(label = labels, pad=5, thickness=10)
data = go.Sankey(link = link, node=node)
# plot
fig = go.Figure(data)
fig.show()
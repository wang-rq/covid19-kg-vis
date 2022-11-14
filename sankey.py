import plotly.graph_objects as go
import urllib, json
import urllib.request
import pandas as pd
from collections import Counter
from pandas.core.frame import DataFrame


data = pd.read_csv("/Users/wangruoqi/Desktop/cov/conditions.csv")

data.sort_values(by=["PATIENT", "STOP"], inplace=True, ascending=[True,True])

data_new = data.groupby(['PATIENT'])['DESCRIPTION'].apply(list).to_frame()
for index, row in data_new.iterrows():
    if row['DESCRIPTION'][0] != 'Suspected COVID-19':
        data_new = data_new.drop(index=index)


res = []
for index, row in data_new.iterrows():
    for i in range(len(row['DESCRIPTION'])-1):
        # res.append((row['DESCRIPTION'][i], row['DESCRIPTION'][i+1]))
        des = row['DESCRIPTION'][i] + "_" +str(i)
        des1 = row['DESCRIPTION'][i+1] + "_" +str(i+1)
        res.append((des, des1))


count = Counter(res)
print(count)

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

print(labels)

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
link = dict(source = source, target = target, value = value, color=color_link)
node = dict(label = labels, pad=50, thickness=5)
data = go.Sankey(link = link, node=node)
# plot
fig = go.Figure(data)
fig.show()
import pandas as pd
import json
from pandas import json_normalize
df = pd.read_json('data/world_bank_projects.json')
print(df.groupby('countryname').size().sort_values(ascending=False).head(10))
projectCount = {}
for x in range(len(df)):
    row = df['mjtheme_namecode'][x]
    for y in range(len(row)):
        nRow=json_normalize(row)
        code = nRow.code[y]
        name = nRow.name[y]
        current = None
        if code in projectCount:
            current = projectCount[code]
            
            if len(current['name'].strip()) == 0 and len(name.strip())>0:
                current['name'] = name
        else:
            current = {
                'code':code,
                'name':name,
                'count':0,
            }
            projectCount[code] = current
        current['count']+=1
projectList = []
for key in projectCount:
    item = projectCount[key]
    projectList.append(item)
print(pd.DataFrame(projectList).sort_values('count', ascending=False).head(10))
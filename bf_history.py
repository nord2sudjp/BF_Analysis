#!/usr/bin/env python
# coding: utf-8


import pandas as pd
df = pd.read_excel('./template/Template_1_3_2019.xlsx', sheet_name='Sheet1')

def get_location(name):
    try: 
        if name is None:
            return ""
#        if np.isnan(name):
#            return ""
        if "-" in name:
            return name.split('-')[0].strip().upper()
        else: 
            return name
    except:
        print(name)

def get_os(name):
    return name.split(' ')[2].strip()


def dfw_create(df):
    df_w = pd.DataFrame(index=[])
    df_w['location_1']=df['Location'].apply(get_location)
    df_w['os_version'] = df['Full Operating System Name and Service Pack Level - Windows'].apply(get_os)
    df_w['computer'] = df['Computer Name']
    df_x = df_w.groupby(["location_1", "os_version"], as_index=False).count()
    return df_x[df_x["os_version"]=="10"]

def rtv_date(name):
    return name.replace("PC_Info_", "").replace(".xlsx", "").replace("_", "/")    


df_final = dfw_create(df)
df_final.rename(columns={'computer': '1/3/2019'}, inplace=True)


import os
import re
path = './'
regex = re.compile(r'(.xlsx)$')
files = []
for filename in os.listdir(path):
    if os.path.isfile(os.path.join(path, filename)): #ファイルのみ取得
        if regex.search(filename):
            files.append(filename)



for xlsx_file in files:
    print("main:Loading-" + xlsx_file)
    try:
        df = pd.read_excel(xlsx_file, sheet_name='Sheet1')
    except:
        df = pd.read_excel(xlsx_file, sheet_name='FullList')
    df_w = dfw_create(df)
    df_w.rename(columns={'computer': rtv_date(xlsx_file)}, inplace=True)
    df_final = pd.merge(df_final, df_w, how="outer")


df_final.to_csv("bigfix_agg.csv")

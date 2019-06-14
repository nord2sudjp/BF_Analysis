#!/usr/bin/env python
# coding: utf-8

# In[194]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

# Data Loading
df = pd.read_csv('bigfix_report.txt',  header=None,sep='\t',engine='python')


# In[195]:


# Data Cleansing
## Select only upgraded laptop, criterial third column = "-".
df_w = df[df[0].str[2:3]=='-']


# In[196]:


## Add "Country" from laptop name, first two character specify country code.
df_w['country'] = df[0].str[0:2]


# In[197]:


## get_relay("Relay-Name.xxx.com:52311	") returns "Relay-Name".
def get_relay(name):
    if ':' in name:
        return name.split(':')[0].split('.')[0].strip()
    else:
        return name


# In[198]:


## Add "relay"
df_w["relay"] = df[6].apply(get_relay)


# In[199]:


## Drop non-necessary fields, only required country and relain.
df_w = df_w.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis=1)


# In[200]:


# EDA
## profiling
import pandas_profiling
pandas_profiling.ProfileReport(df_w)


# In[201]:


## count record
print("***** Record Count *****")
print(df_w.shape)

## data summary
print("***** Data Summary *****")
print(df_w.head())
print(df_w.describe())
print(df_w.dtypes)


# In[202]:


# Null Value Analysis
print(df_w.info())
df_w.isnull().sum()

sns.heatmap(df_w.isnull(), cbar=False)


# In[203]:


# Data Visualization - categoral

cat = ['country', 'relay']
fig = plt.figure(figsize=(40, 40))
for i in range(0, len(cat)):
  fig.add_subplot(2,1,i+1)
  b = sns.countplot(y=cat[i], data=df_w, order=df_w[cat[i]].value_counts().index)
  b.tick_params(labelsize=20)


# In[208]:


def view_breakdown(target_unit, target_y):
    fig = plt.figure(figsize=(70, 100))
    figure_x_count = 3
    figure_y_count=len(df_w_index)/figure_x_count+1
    # sns.set(rc=None)
    sns.set(rc={'figure.facecolor':'cornflowerblue'})
    for i in range(0, len(df_w_index)):
       fig.add_subplot(figure_y_count,figure_x_count,i+1)
       target_data=df_w[df_w[target_unit]==df_w_index[i]]
       b = sns.countplot(y=target_y, data=target_data, order=target_data[target_y].value_counts().index)
       b.tick_params(labelsize=12)
       b.set_xlabel('count')
       b.set_ylabel(target_y)
       b.set_title(df_w_index[i], fontsize=18)


# In[209]:


target_unit='country'
target_y='relay'
df_w_index = df_w[target_unit].value_counts().index
view_breakdown(target_unit, target_y)


# In[212]:


target_unit='relay'
target_y='country'
df_w_index = df_w[target_unit].value_counts().index
view_breakdown(target_unit, target_y)


# In[213]:


3+5


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime


# In[2]:


covid_df = pd.read_csv(r'C:\Users\talk2\Downloads\covid_19_india.csv')
covid_df.head(10)


# In[3]:


covid_df.info()


# In[4]:


covid_df.describe()


# In[5]:


vaccine_df = pd.read_csv(r'C:\Users\talk2\Downloads\covid_vaccine_statewise.csv')


# In[6]:


vaccine_df.head(10)


# In[7]:


covid_df.drop(["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"], inplace = True, stateaxis = 1)


# In[ ]:


covid_df.head()


# In[8]:


covid_df['Date']= pd.to_datetime(covid_df['Date'], format = '%Y-%m-%d')
covid_df.head()


# In[9]:


#Active_cases

covid_df['Active_Cases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])
covid_df.tail(200)


# In[10]:


statewise = pd.pivot_table(covid_df, values = ['Confirmed', 'Deaths', 'Cured'], index = 'State/UnionTerritory', aggfunc = max)


# In[11]:


statewise['Recovery Rate'] = statewise['Cured']* 100/statewise['Confirmed']


# In[12]:


statewise['Mortality Rate'] = statewise['Deaths']* 100/statewise['Confirmed']


# In[13]:


statewise = statewise.sort_values(by = 'Confirmed', ascending = False)


# In[14]:


statewise.style.background_gradient(cmap = "cubehelix")


# In[15]:


# Top 10 Active Cases States

top_10_active_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Active_Cases', 'Date',]].sort_values(by = ['Active_Cases'], ascending = False).reset_index()


# In[16]:


fig = plt.figure(figsize= (16,9))


# In[17]:


plt.title('Top 10 states with most active cases in India', size = 25)


# In[18]:


ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = 'Active_Cases', x = 'State/UnionTerritory', linewidth = 2, edgecolor= 'red')


# In[19]:



top_10_active_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Active_Cases', 'Date',]].sort_values(by = ['Active_Cases'], ascending = False).reset_index()
fig = plt.figure(figsize= (16,9))
plt.title('Top 10 states with most active cases in India', size = 25)
ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = 'Active_Cases', x = 'State/UnionTerritory', linewidth = 2, edgecolor= 'red')
plt.xlabel("Sates")
plt.ylabel("Total Active Cases")
plt.show()


# In[20]:


#Top States with highest deaths

top_10_deaths = covid_df.groupby(by = 'State/UnionTerritory').max()[['Deaths', 'Date']].sort_values(by = ['Deaths'], ascending = False).reset_index()

fig = plt.figure(figsize= (18,5))

plt.title("Top 10 states with most Deaths", size = 25)

ax = sns.barplot(data = top_10_deaths.iloc[:12], y = 'Deaths', x = 'State/UnionTerritory', linewidth = 2, edgecolor = 'black')

plt.xlabel("States")
plt.ylabel("Total Death Cases")
plt.show()


# In[21]:


# Growth Trend

fig = plt.figure(figsize = (12, 6))

ax = sns.lineplot(data = covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Uttar Pradesh'])],x='Date', y  = 'Active_Cases' , hue = 'State/UnionTerritory')

ax.set_title('Top 5 Affected States in India', size = 16)


# In[22]:


vaccine_df.head()


# In[23]:


vaccine_df.rename(columns = {'Updated On' : 'Vaccine_Date'}, inplace = True)


# In[24]:


vaccine_df.head(10)


# In[25]:


vaccine_df.info()


# In[26]:


vaccine_df.isnull().sum()


# In[28]:


vaccination = vaccine_df.drop(columns=['Sputnik V (Doses Administered)', 'AEFI', '18-44 Years (Doses Administered)', '45-60 Years (Doses Administered)', '60+ Years(Individuals Vaccinated)'])


# In[30]:


vaccination.head()


# In[33]:


#Male vs Female vaccination

male = vaccination["Male(Individuals Vaccinated)"].sum()
female = vaccination["Female(Individuals Vaccinated)"].sum()
px.pie(names=["Male", "Female"], values=[male, female], title="Male and Female Vaccination")


# In[36]:


#Remove rows where state = India
vaccine = vaccine_df[vaccine_df.State!= 'India']


# In[39]:


vaccine.rename(columns = {"Total Individuals Vaccinated" : "Total"}, inplace = True)
vaccine.head()


# In[40]:


# Most vaccinated State
max_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vac = max_vac.sort_values('Total', ascending = False)[:5]
max_vac


# In[41]:


fig = plt.figure(figsize = (10,5))
plt.title("Top 5 Vaccinated States in India", size = 20)
x = sns.barplot(data = max_vac.iloc[:10], y = max_vac.Total, x = max_vac.index, linewidth=2, edgecolor= 'black')
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()


# In[ ]:





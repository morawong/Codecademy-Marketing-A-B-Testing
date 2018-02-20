
# coding: utf-8

# In[62]:


#Importing all required libraries for assignment

import sqlite3 as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
get_ipython().magic(u'matplotlib inline')
import scipy as sp


# In[63]:


#Accessing database for Codecademy with information on the current ad and Ad option C
database = "codecademy_sqlite_adc.db"

connection = sql.connect(database)

query = "SELECT * FROM CurrentAd UNION SELECT * FROM GroupC"

#Setting up dataframe as df
df = pd.read_sql_query(query, connection)

df.head()


# In[64]:


#taking a look at the data types in df
df.info()


# In[65]:


#Re-assigning the data types of the index, uuid, Group, Button and Banner as category
df["index"] = df["index"].astype("category")
df["uuid"] = df["uuid"].astype("category")
df["Group"] = df["Group"].astype("category")
df["Button"] = df["Button"].astype("category")
df["Banner"] = df["Banner"].astype("category")


# In[66]:


#Checking for missing and weird values
df.isnull().sum()


# In[67]:


#Subsetting data frame
df.Group.unique()


# In[68]:


curr_ad = df[df["Group"] == "CurrentAd"]


# In[69]:


ad_C= df[df["Group"] == "C"]


# In[70]:


#Checking count on current ad
curr_ad.describe()


# In[71]:


#Checking count of Ad C
ad_C.describe()


# In[72]:


#Visualization 1
sns.distplot(ad_C["Click"], label = "Ad C", kde = False)
sns.distplot(curr_ad["Click"], label = "Current Ad", kde = False)
plt.legend()


# In[73]:


#Visualization 2
sns.barplot(x = df["Group"], y = df["Click"], estimator = sum)
plt.xlabel("Ad Groups")
plt.ylabel("Click Count")
plt.title("Count of Clicks per Group");


# In[74]:


ad_C["Click"].sum() - curr_ad["Click"].sum()


# In[75]:


curr_click_perc = curr_ad["Click"].sum()/len(curr_ad) * 100
C_click_perc = ad_C["Click"].sum()/len(ad_C) * 100

C_click_perc, curr_click_perc


# In[76]:


#Visualization 3 of percentage of clicks per group
sns.barplot(x = ["C", "Current Ad"], y = [C_click_perc, curr_click_perc])
plt.xlabel("Ad Groups")
plt.ylabel("Percentage (%)")
plt.title("Percentage of clicks per Group");


# In[77]:


#t-test to check for statistical significance
def stat_significant(p,alpha):
    if p <= alpha:
        print("P-Value =" + str(p) + "\n" + "Reject the Null Hypothesis. Results are statistically significant.")
    else:
        print("P-Value =" + str(p) + "\n" + "Accept the Null Hypothesis. Results are not statistically significant.")
                


# In[78]:


alpha = .05
ttest = sp.stats.ttest_ind(curr_ad['Click'], ad_C['Click'])
p = ttest[1]

stat_significant(p, alpha)


# In[102]:


# Pie chart of the percentages of ad clicks
# Data to plot
labels = 'Ad C clicks', 'Current Ad clicks'
sizes = [C_click_perc, curr_click_perc]
colors = ['steelblue', 'lightsteelblue']
explode = (0 , 0.1)  # explode 1st slice
 
# Plot
piechart=plt.pie(sizes, explode=explode, labels=labels, colors=colors, shadow=True, startangle=140, autopct='%1.1f%%')
 
plt.axis('equal')
plt.show()




# In[81]:


#Results were statistcally significant meaning Ad C had a significantly higher amount of clicks


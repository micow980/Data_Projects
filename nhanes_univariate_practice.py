
# coding: utf-8

# # Univariate analysis using NHANES data
# 
# This notebook will give you the opportunity to perform some univariate analyses on your own using the NHANES.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

da = pd.read_csv("nhanes_2015_2016.csv")


# ## Question 1
# 
# Relabel the marital status variable [DMDMARTL](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.htm#DMDMARTL) to have brief but informative character labels.  Then construct a frequency table of these values for all people, then for women only, and for men only.  Then construct these three frequency tables using only people whose age is between 30 and 40.

# In[33]:


#Create an alternate dataframe so main data is unaltered
da_clean = da

#This is in order to relabel the numeric data to characters
da_clean['DMDMarrital'] = da.DMDMARTL.replace({1: 'Married', 2: 'Single', 3: 'In a Relationship', 4: 'Divorced', 
                                         5: 'Complicated', 6: 'Not Interested', 77: 'Prefer not to say'})

#This code was in order to see the count in each strata
da_clean.DMDMarrital.value_counts()


# In[54]:


#This was to be able to relabel the numeric data according to sex
da_clean['gender'] = da.RIAGENDR.replace({1: 'Male', 2: 'Female'})

#This was to see the count in each strata by gender
da_clean.groupby('gender')['DMDMarrital'].value_counts(normalize = True)


# In[39]:


# this is to get the agegroup 30 to 40
da_clean["agegrp"] = pd.cut(da.RIDAGEYR, [30, 40])

#This was to see the stratified age group's 30-40 and see reported marrital status
da_clean.groupby("agegrp")["DMDMarrital"].value_counts()


# In[38]:


# Combining the two variables we created as filters to report marrital status
da_clean.groupby(['gender', 'agegrp'])['DMDMarrital'].value_counts().unstack()


# In[40]:


#Replaced NaN variables in Table to 0 
x = da_clean.groupby(['gender', 'agegrp'])['DMDMarrital'].value_counts().unstack()
x = x.fillna(0)
x


# __Q1a.__ Briefly comment on some of the differences that you observe between the distribution of marital status between women and men, for people of all ages.

# In[43]:


#Created a new age strata covering ages with 10 years minimum difference
da_clean['agestrata'] = pd.cut(da.RIDAGEYR, [10,20, 30, 40, 50, 60, 70, 80])

#Replaced NaN variables in Table to 0 
y = da_clean.groupby(['gender', 'agestrata'])['DMDMarrital'].value_counts().unstack()
y = y.fillna(0)
y


# In[62]:


x = da_clean[da.gender == "Female"]
x["agegrp2"] = pd.cut(da_clean.RIDAGEYR, [10,20, 30, 40, 50, 60, 70, 80])
dx = x.groupby(["agegrp2"])["DMDMarrital"].value_counts(normalize = True).unstack()
dx = dx.fillna(0)
print(dx)


# ## Question 3
# 
# Construct a histogram of the distribution of heights using the BMXHT variable in the NHANES sample.

# In[64]:


# insert your code here

sns.distplot(da.BMXHT.dropna())
plt.show()


# __Q3a.__ Use the `bins` argument to [distplot](https://seaborn.pydata.org/generated/seaborn.distplot.html) to produce histograms with different numbers of bins.  Assess whether the default value for this argument gives a meaningful result, and comment on what happens as the number of bins grows excessively large or excessively small. 

# In[66]:


sns.distplot(da.BMXHT.dropna(), bins = 10)
plt.show()


# __Q3b.__ Make separate histograms for the heights of women and men, then make a side-by-side boxplot showing the heights of women and men.

# In[68]:


sns.boxplot(x = da_clean.BMXHT, y = da_clean.gender)
hist = sns.FacetGrid(da_clean, row = 'gender')
hist = hist.map(plt.hist, 'BMXHT')

plt.show()


# __Q3c.__ Comment on what features, if any are not represented clearly in the boxplots, and what features, if any, are easier to see in the boxplots than in the histograms.

# ## Question 4
# 
# Make a boxplot showing the distribution of within-subject differences between the first and second systolic blood pressure measurents ([BPXSY1](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXSY1) and [BPXSY2](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXSY2)).

# In[70]:


x = da[['BPXSY1', 'BPXSY2']]
x.boxplot()


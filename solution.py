
# coding: utf-8

# In[1]:

#Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib notebook')

#Reading the data files
rdata = pd.read_csv('Sub_Division_IMD_2017.csv')
cdata = pd.read_csv('apy.csv')

#Filter on Haryana state only
cdata = cdata[cdata['State_Name']=='Haryana']  

#Removing the comments from season labels for futher use
cdata.loc[cdata["Season"] == "Kharif     ", cdata.columns[3]] = 'Kharif'     
cdata.loc[cdata["Season"] == "Rabi       ", cdata.columns[3]] = 'Rabi'       
cdata.loc[cdata["Season"] == "Whole Year ", cdata.columns[3]] = 'Whole Year' 

cdata.rename(columns={'Crop_Year':'Year'}, inplace=True) #Renaming coloumn name so to merge it with other file later on
cdata.dropna(inplace=True)

#Creating new column to estimate a comparison statistic
cdata['Production per unit area'] = cdata['Production']/cdata['Area']
#Pivoting the data table and calulating the total unique count for years and seasons
cdata = cdata.pivot_table(index=['Year','Season'], values=['Production per unit area'], aggfunc=[np.sum]).sort_index()
years = cdata.index.get_level_values(0).unique()
seasons = cdata.index.get_level_values(1).unique()
cdata = cdata.unstack()

#Slicing the multiindexed columns
idx = pd.IndexSlice
cdata = cdata.loc[:,idx['sum','Production per unit area']]

#Filter on Haryana state only
rdata = rdata[rdata['SUBDIVISION'] == 'Haryana Delhi & Chandigarh']
rdata.set_index('YEAR', inplace=True)
# Selecting the data only for those years which were there in the first file
rdata = rdata.loc[1997:2012]
#Removing any unused columns
rdata.drop(['JF','MAM','JJAS','OND'], axis=1, inplace=True)

#Calculating yearly sum for rainfall as per seasons and their respective months
rdata.rename(columns={'ANNUAL':'Whole Year Rainfall'}, inplace=True)
rdata['Rabi Rainfall'] = rdata[['JAN','FEB','OCT','NOV','DEC']].sum(axis=1)
rdata['Kharif Rainfall'] = rdata[['JUL','AUG','OCT','SEP']].sum(axis=1)
#Renaming the subdivision name for easy merging
rdata['SUBDIVISION'] = 'Haryana'

#Choosing seaborn data style for matplotlib
plt.style.use('seaborn')

#Creating figure, subplots, and intializing subplots to share x-axis 
#so that rainfall and production can be compared for each season
fig = plt.figure(figsize=(9,9))
ax1 = plt.subplot(311)
ax11 = ax1.twinx()
ax2 = plt.subplot(312)
ax22 = ax2.twinx()
ax3 = plt.subplot(313)
ax33 = ax3.twinx()

#Plotting data for Whole year on the first axis
rdata.plot(x=rdata.index, y=['Whole Year Rainfall'], ax=ax1, color='b', linewidth=2, alpha=0.6);
cdata.plot(x=cdata.index, y=['Whole Year'], ax=ax11, color='r', alpha=0.6, linewidth=2);
ax1.set_xticks(rdata.index.values);
ax1.grid(b=None, which='both', axis='y');
ax11.grid(b=None, which='both', axis='y');
ax1.legend(['Whole Year average rainfall'], loc=9, bbox_to_anchor=(0.5, 0.90));
ax11.legend(['Production per unit area for whole year crops'], loc=9);

#Plotting data for Rabi's season on the second axis
rdata.plot(x=rdata.index, y=['Rabi Rainfall'], ax=ax2, color='b', linewidth=2, alpha=0.6);
cdata.plot(x=cdata.index, y=['Rabi'], ax=ax22, color='g', alpha=0.6, linewidth=2);
ax2.set_xticks(rdata.index.values);
ax2.grid(b=None, which='both', axis='y');
ax22.grid(b=None, which='both', axis='y');
ax22.set_ylabel('Production per unit area', fontsize=17);
ax2.set_ylabel('Total rainfall in mm', fontsize=17, animated=True);
ax2.legend(['Rabi season average rainfall'], loc=9, bbox_to_anchor=(0.5, 0.90));
ax22.legend(['Production per unit area for Rabi season crops'], loc=9);

#Plotting data for Kharif season on the third axis
rdata.plot(x=rdata.index, y=['Kharif Rainfall'], ax=ax3, color='b', linewidth=2, alpha=0.6);
cdata.plot(x=cdata.index, y=['Kharif'], ax=ax33, color='m', alpha=0.6, linewidth=2);
ax3.set_xticks(rdata.index.values);
ax3.grid(b=None, which='both', axis='y');
ax33.grid(b=None, which='both', axis='y');
ax3.legend(['Kharif Season average rainfall'], loc=9, bbox_to_anchor=(0.5, 0.90));
ax33.legend(['Production per unit area for Kharif season crops'], loc=9);

#Rotating the x-axis labels to 45` so that they do not overlap
h = ax3.xaxis
for item in h.get_ticklabels():
    item.set_rotation(45)

#Saving the infographic
fig.savefig('solution4.png', bbox_inches='tight')


# In[ ]:




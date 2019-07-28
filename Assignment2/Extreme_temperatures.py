import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')

%matplotlib notebook
import pandas as pd
import datetime
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def ans_one():
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df = df.sort(['ID', 'Date'])

    # Pre-process the data
    df['Year'] = df['Date'].apply(lambda x: x[:4])
    df['Month-Day'] = df['Date'].apply(lambda x: x[5:])
    df = df[df['Month-Day'] != '02-29']

    # df['Month'] = df['Date'].apply(lambda x: x[5:7])

    df_min = df[(df['Element'] == 'TMIN')]
    df_max = df[(df['Element'] == 'TMAX')]

    df_temp_min = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')]
    df_temp_max = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')]

    temp_min = df_temp_min.groupby('Month-Day')['Data_Value'].agg({'temp_min_mean': np.mean})
    temp_max = df_temp_max.groupby('Month-Day')['Data_Value'].agg({'temp_max_mean': np.mean})

    temp_min_15_tmp = df_min[df_min['Year'] == '2015']
    temp_max_15_tmp = df_max[df_max['Year'] == '2015']

    temp_min_15 = temp_min_15_tmp.groupby('Month-Day')['Data_Value'].agg({'temp_min_15_mean': np.mean})
    temp_max_15 = temp_max_15_tmp.groupby('Month-Day')['Data_Value'].agg({'temp_max_15_mean': np.mean})


    # Reset Index
    temp_min = temp_min.reset_index()
    temp_max = temp_max.reset_index()

    temp_min_15 = temp_min_15.reset_index()
    temp_max_15 = temp_max_15.reset_index()

    # Find index
    broken_min = (temp_min_15[temp_min_15['temp_min_15_mean'] < temp_min['temp_min_mean']]).index.tolist()
    broken_max = (temp_max_15[temp_max_15['temp_max_15_mean'] > temp_max['temp_max_mean']]).index.tolist()
    #print (broken_min)
    
    plt.figure()
    plt.plot(temp_min['temp_min_mean'],'y',alpha=0.75 ,label='Record Low')
    plt.plot(temp_max['temp_max_mean'],'r',alpha=0.5,label='Record High')
    
    plt.scatter(broken_min,temp_min_15['temp_min_15_mean'].iloc[broken_min],s=1,c='k',label='Broken Min')
    plt.scatter(broken_max,temp_max_15['temp_max_15_mean'].iloc[broken_max],s=1,c='b',label='Broken Max')
    
    plt.xlabel('Month')
    
    plt.ylabel('Temperature (Tenths of Degrees C)')
    plt.title('Extreme Temperatures of 2015 against 2005-2014')
    plt.gca().fill_between(range(len(temp_min)), 
                       temp_min['temp_min_mean'], temp_max['temp_max_mean'], 
                       facecolor='grey', 
                       alpha=0.2)

    plt.gca().axis([-5, 370, -400, 400])
    plt.legend(frameon = False)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    a = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    b = [i+15 for i in a]

    Month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.xticks(b, Month_name)
    
    
    #print (temp_max.head())
    
    #print (df.head())        
ans_one()
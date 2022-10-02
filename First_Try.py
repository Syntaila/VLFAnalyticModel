# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:24:27 2022

@author: Nadine
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import datetime
import math
import calculateNoon as noon
import time
import Plots as plots

# determination of runtime
summe = 0
start = time.time()
start_proc = time.process_time()

#%% define time range to plot (should start with 21.12.)
numdays = 366
base = datetime.datetime(year = 2009, month = 12, day = 21)

# numdays = 15
# base = datetime.datetime(year = 2009, month = 1, day = 17)
date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
date_list.sort()
print('this range lasts from ', date_list[0],' to ', date_list[-1])

# define variables
receiver = 'NAA'
counter = 0
dates = []
data_per_day = 24*60*60*10 # every 0.1 seconds one value

# calculate sunrise and sunset for midpoint 
sunrise_uct, sunset_uct = noon.only_daytime()
# first row of data_colourplot = time
data_colourplot = [np.arange(0,data_per_day,3000)]

#%% read out the data
for date in range(len(date_list)):
    # read out todays day, month, year and read in file
    day = date_list[date].day
    month = date_list[date].month
    year = date_list[date].year

    date  = str(year)+'{:0>2}'.format(month)+'{:0>2}'.format(day)
    filename = receiver+date+'.txt'
    print(filename,' is read out')
    header = []
    data = []
    # try to open file, if file not exist, len(data) = 0
    try:
        for line in open('data/'+filename):
            # seperare data in file and header
            fld = line.split()
            if fld[0].startswith('%'):
                header.append(fld)
            else:
                data.append(fld)
    except FileNotFoundError:
        pass
    # if data is empty (no file or empty file), fill with nan
    if len(data) == 0:
        data_np = np.full((data_per_day,3),np.nan)
    else:
        data_np = np.array(data)
        data_np = data_np.astype(float)
    
    # if file don't start with 0 seconds, pad with nan (transmitter error)
    if data_np[0,0] != 0:
        try:
            data_nan = np.empty((int(data_np[0,0]*10),3))
            data_nan[:] = np.nan
            data_np = np.append(data_nan, data_np, axis = 0)
        except ValueError:
            pass
        
    # seperate data per day in 5-10 minute intervalls
    data_average_time_list = []
    data_average_time_amplitude = []
    intervall_time_min = 5 # min
    for i in range(int(data_per_day/(intervall_time_min*60*10))): # value is 3000
        start = int(data_per_day/int(data_per_day/(intervall_time_min*60*10))*i)
        end = int(data_per_day/int(data_per_day/(intervall_time_min*60*10))*(i+1))

        data_average_time = np.nanmean(data_np[start:end+1,0])
        data_average_amplitude = np.nanmean(data_np[start:end+1,1])
        data_average_time_list.append(data_average_time)
        data_average_time_amplitude.append(data_average_amplitude)
    
    time = [] # list of time strings 0:00:00
    time_label = [] # list of time strings without second 0:00
    for j in range(len(data_average_time_list)):
        try:
            time.append(str(datetime.timedelta(seconds=data_average_time_list[j])))
            time_label.append((str(datetime.timedelta(seconds=data_average_time_list[j]))).split(".")[0].split(':')[0]+':'+(str(datetime.timedelta(seconds=data_average_time_list[j]))).split(".")[0].split(':')[1])
        except ValueError: 
            continue
    
    # truncate the night values
    for k in range(len(data_average_time_list)):
        # counter is like the day - starting with 21.12. and ending with 20.12. -> bei letztem tag einmal zurücksetzen
        if data_average_time_list[k]/60/60 <= sunrise_uct[counter] or data_average_time_list[k]/60/60 >= sunset_uct[counter]:
            data_average_time_amplitude[k] = np.nan

    data_colourplot.append(data_average_time_amplitude)
    dates.append(str(datetime.datetime(year = year, month = month, day = day)).split(' ')[0])
    counter +=1
    # reset the counter after 1 year, that sunrise/ sunset are read out correctly
    if counter >= 364:
        counter-=364

data_colourplot_np = np.array(data_colourplot)

#%% Plot the data as colourplot with x-axis = time, y-axis = date, data = amplitude
plots.colourplot(data_colourplot_np, dates, time_label)


#%% calculation of runtime 
ende = time.time()
ende_proc = time.process_time()
print('Total time: {:5.3f}s'.format(ende - start))
print('System time: {:5.3f}s'.format(ende_proc - start_proc))
print('Finished')


# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:24:27 2022

@author: Nadine
"""
# import sys
# import os
# sys.path.append(os.path.abspath('C:\Users\Nadine\Documents\Universitaet\Master\ISWC\0_Praxis'))

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import datetime
import math
import calculateNoon as calcnoon
import time
import Plots as plots
import scipy
import VLF_functions as functions

# determination of runtime
summe = 0
start_time = time.time()
start_proc = time.process_time()

#%% define time range to plot (should start with 21.12.)
numdays = 366
base = datetime.datetime(year = 2009, month = 12, day = 21)

# numdays = 20
# base = datetime.datetime(year = 2009, month = 12, day = 21)
# outlier detection: 21.Juni
date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
date_list.sort()
print('this range lasts from ', date_list[0],' to ', date_list[-1])

# define variables
receiver = 'NAA'
counter = 0

data_per_day = 24*60*60*10 # every 0.1 seconds one value
intervall_time_min = 5

# calculate sunrise and sunset for midpoint 
noon = 12
# midpoint
sunrise_local, sunset_local, noon_shift = calcnoon.only_daytime(noon, [65.397622,-53.107806])
# transmitter
# sunrise_local, sunset_local_transmitter, noon_shift_transmitter = calcnoon.only_daytime(noon, [44.64503, -67.28315])
# receiver
# sunrise_local_receiver, sunset_local, noon_shift_receiver = calcnoon.only_daytime(noon, [78.929479, 11.897683])


# data_colourplot = np.full((int(data_per_day/(intervall_time_min*60*10)),len(date_list)),np.nan)
# first row of data_colourplot = time
# data_colourplot[:,0] = np.arange(0,data_per_day,3000)
data_colourplot = [np.arange(0,data_per_day,3000)]
data_colourplot_total = np.full((len(date_list)+1,int(data_per_day/(intervall_time_min*60*10))),np.nan)
data_colourplot_total[0,:] = np.arange(0,data_per_day,3000)
data_colourplot_without_night_np = np.full((len(date_list)+1,int(data_per_day/(intervall_time_min*60*10))),np.nan)
data_colourplot_without_night_np[0,:] = np.arange(0,data_per_day,3000)
data_colourplot_model = np.full((len(date_list),int(data_per_day/(intervall_time_min*60*10))),np.nan)



#%% read out the data
dates = []
for date_int in range(len(date_list)):
    # read out todays day, month, year and read in file
    day = date_list[date_int].day
    month = date_list[date_int].month
    year = date_list[date_int].year

    date  = str(year)+'{:0>2}'.format(month)+'{:0>2}'.format(day)
    filename = receiver+date+'.txt'
    print(filename,'is read out')
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
    
    # average the data 
    data_average_time_np, data_average_amplitude_np = functions.average_data_2(data_np, data_per_day, intervall_time_min)
        
    data_colourplot_total[date_int+1,:] = data_average_amplitude_np 
    dates.append(str(datetime.datetime(year = year, month = month, day = day)).split(' ')[0])

    # read out the times for label
    time_hours_min_sec = [] # list of time strings 0:00:00
    time_label = [] # list of time strings without second 0:00
    for j in range(len(data_average_time_np)):
        try:
            time_hours_min_sec.append(str(datetime.timedelta(seconds=data_average_time_np[j])))
            time_label.append((str(datetime.timedelta(seconds=data_average_time_np[j]))).split(".")[0].split(':')[0]+':'+(str(datetime.timedelta(seconds=data_average_time_np[j]))).split(".")[0].split(':')[1])
        except ValueError: 
            continue
    

#%% start with averaged data
time_label = np.array(time_label)
counter = 0
data_average_time_list = data_average_time_np
regression_year = np.full((len(date_list),2),np.nan)
for date_int in range(len(date_list)): 
    # truncate the night
    data_colourplot_without_night_np[date_int+1,:] = np.where(np.logical_or((data_colourplot_total[0,:]/3600/10-noon_shift)%24>sunset_local[counter],(data_colourplot_total[0,:]/3600/10-noon_shift)%24<sunrise_local[counter]) ,np.nan,data_colourplot_total[date_int+1,:])
    # counter +=1
    time_label_truncated = np.where(np.logical_or((data_colourplot_total[0,:]/3600/10-noon_shift)%24>sunset_local[counter],(data_colourplot_total[0,:]/3600/10-noon_shift)%24<sunrise_local[counter]) ,np.nan,time_label)
    
#   Create the Model for the day: y = a+cx^2
    if not np.isnan(data_colourplot_without_night_np[date_int+1,:]).all():
        # # PLOT
        # plots.regression_plot_one(data_average_time_list/3600, data_colourplot_total[date_int+1], 'Time [h]', 'Amplitude', ' NAA-NyAlesund 06.04.2009', time_label)
        # plots.regression_plot_one(data_average_time_list/3600, data_colourplot_without_night_np[date_int+1], 'Time [h]', 'Amplitude', ' NAA-NyAlesund 06.04.2009 only day', time_label)
        
        local_time = (data_colourplot_without_night_np[0,:]-noon_shift*3600*10)%864000 # in seconds
        # find out the indices where the data is not nan
        index_amplitude = np.where(~np.isnan(data_colourplot_without_night_np[date_int+1,:]))
        amplitude = data_colourplot_without_night_np[date_int+1,:][index_amplitude]
        
        noon_in_local_time = noon
        # einmal noon abziehen, damit um 0 herum data set, damit parabel mitte bei 0 beim noon
        local_time = local_time[index_amplitude]-noon_in_local_time*60*60*10
        time_label_truncated = time_label_truncated[index_amplitude]
        # print(local_time/36000)
        # print('date_int',date_int, date_list[date_int])
        model, regression, amplitude, times_for_matrix = functions.calculate_regression_for_day(amplitude, local_time-noon, noon_in_local_time = noon)
        
        # #PLOT
        # plots.regression_plot(times_for_matrix/3600/10, model, amplitude, 'time', 'amplitude', 'Regression over the daytime sin', time_label_truncated)
         
        # model, regression, amplitude, times_for_matrix = functions.calculate_regression_for_polynomial(amplitude, local_time-noon, noon_in_local_time = noon)
        
        # # #PLOT
        # plots.regression_plot(times_for_matrix/3600/10, model, amplitude, 'time', 'amplitude', 'Regression over the daytime poly', time_label_truncated)
         
        # if date_int == 5:
        #     break
        
        
        # detect the outliers and delete them
        amplitude_corrected, times_for_matrix_corrected = functions.outlier_detection(model, amplitude, times_for_matrix)
        # not again noonshift
        index_amplitude = np.where(~np.isnan(amplitude_corrected))
        amplitude_corrected = amplitude_corrected[index_amplitude]
        noon_in_local_time = 0
        times_for_matrix_corrected = times_for_matrix_corrected[index_amplitude]-noon_in_local_time*60*60
        time_label_truncated = time_label_truncated[index_amplitude]
        # calclate new model without outliers
        model, regression, amplitude, times_for_matrix = functions.calculate_regression_for_day(amplitude_corrected, times_for_matrix_corrected, noon_in_local_time = 0)
        # times_for_matrix_utc = times_for_matrix + noon+noon_shift
        
        # #PLOT
        # plots.regression_plot(times_for_matrix/3600/10, model, amplitude, 'time', 'amplitude', 'Regression over daytime after outlier-correction',time_label_truncated)
        
        regression_year[date_int] = regression
        
    #% daten in matrix
        # model_average_amplitude = np.full((len(data_average_time_amplitude)),np.nan)
        # for i in range(len(data_colourplot_model[0]):
        #     data_colourplot_model[i] = regression[0]+regression[1]*np.square(data_average_time_list)
        
        
        # bring the data into matrix form (for colourplot later)
        time_for_regression = data_colourplot_without_night_np[0,:]#np.arange(0,data_per_day,3000)
        # regression_result = (regression[0]+regression[1]*np.square(data_average_time_list-(noon+noon_shift)*60*60))
        t = 2*np.pi/(24*3600)
        regression_result = regression[0]+regression[1]*(np.cos((data_average_time_list-(noon+noon_shift)*60*60)*t)+1)
        
        # # PLOT
        # plots.regression_plot_one(time_for_regression/36000, regression_result, 'Time [h]', 'Amplitude', 'Total Model over all hours', time_label)
        
        # print(len(regression_result))
        
        data_colourplot_model[date_int,:] = np.where(np.logical_or((data_colourplot_total[0,:]/3600/10-noon_shift)%24>sunset_local[counter],(data_colourplot_total[0,:]/3600/10-noon_shift)%24<sunrise_local[counter]) ,np.nan,regression_result)
        
        print(data_colourplot_model[date_int,:][0], data_colourplot_model[date_int,:][-1])
        # for k in range(len(regression_result)):
        # # sunrise_local, sunset_local, noon_shift
        # # counter is like the day - starting with 21.12. and ending with 20.12. -> bei letztem tag einmal zurücksetzen
        # # calculate in local time
        #     if (time_for_regression[k]/60/60-noon_shift)%24 <= sunrise_local[counter] or (time_for_regression[k]/60/60-noon_shift)%24 >= sunset_local[counter]:
        #         regression_result[k] = np.nan
        # data_colourplot_model[date_int,:] = regression_result
    else:
        # print('in except')
        data_colourplot_model[date_int,:] = np.full(len(data_average_time_list),np.nan)
        pass
    counter +=1
    # reset the counter after 1 year, that sunrise/ sunset are read out correctly
    if counter >= 364:
        counter-=364

#%%
data_colourplot_model_np = np.append([time_for_regression],data_colourplot_model,axis = 0)
    

data_colourplot_np =data_colourplot_total
# data_colourplot_model_np = np.array(data_colourplot_model)

#% Plot the data as colourplot with x-axis = time, y-axis = date, data = amplitude
plots.colourplot(data_colourplot_np, dates, time_label,  x_axis_number = 10, y_axis_number = 12) # time_label
plots.colourplot(data_colourplot_without_night_np, dates, time_label,  x_axis_number = 10, y_axis_number = 12) # time_label
plots.colourplot(data_colourplot_model_np, dates, time_label,  x_axis_number = 10, y_axis_number = 12) # time_label

# Todo: 1 Monat in der Mitte fehlt
# Zeit optimieren (array befüllen, nicht appenden)

#%%
# plot regression curves
plots.regression_year_plot(regression_year, date = np.arange(-len(dates)/2,len(dates)/2)+1, title = 'Regression curve for a+c*cos(x*t)', dates = dates, x_axis_number = 20)
# plots.plot_one_curve(np.arange(-len(dates)/2,len(dates)/2), regression_year[:,0], 'a', 'title',  'date', 'Value a', 'r')
# plots.plot_one_curve(np.arange(len(dates))+1, regression_year[:,1], 'c', 'title',  'date', 'Value c', 'b')

#% Kurve für a -> Grundlevel wird zuerst festgelegt deshalb a fitten und festhalten
# (a+c*x^2)*cos(x)+d
# c_corrected, times_for_matrix_corrected = functions.outlier_detection(regression_year[:,0], amplitude, times_for_matrix)
a = regression_year[:,0]
# print(a)
time_for_regression = np.arange(-len(dates)/2,len(dates)/2)+1
model_a_1, regression = functions.calculate_regression_withcos(a, time_for_regression,time_for_regression)

plots.regression_plot(time_for_regression, model_a_1, a, 'days', 'a', 'first regression', dates)
a_corrected, times_for_regression_corrected = functions.outlier_detection(model_a_1, a, time_for_regression, percent_distance_accepted = 3)#2.5)
# print(c_corrected)
# ###################!
model_a_corrected, regression_corrected= functions.calculate_regression_withcos(a_corrected, times_for_regression_corrected,timeformodel = time_for_regression)
plots.regression_plot(time_for_regression, model_a_corrected, a_corrected, 'Days', 'Parameter a', 'Regression of parameter a over the year', dates)

#%%
# counter = 0
# sunrise_local, sunset_local, noon_shift = calcnoon.only_daytime(noon)
# plots.plot_one_curve(np.arange(365), sunrise_local, 'label', 'title', 'x_label', 'y_label', 'b')
# plots.plot_one_curve(np.arange(365), sunset_local, 'label', 'title', 'x_label', 'y_label', 'b')

a = model_a_corrected

data_colourplot_4 = np.full((len(date_list)+1,int(data_per_day/(intervall_time_min*60*10))),np.nan)
data_colourplot_4[0,:] = np.arange(0,data_per_day,3000)
c = np.full(len(date_list),np.nan)
for date_int in range(len(date_list)): 
    #data_colourplot_model_np
    # PROBLEM HIER
    amplitude_without_night = np.array(data_colourplot_model_np[date_int+1,:])
    time_without_night = np.array(data_colourplot_model_np[0,:])
    plots.regression_plot(time_without_night, np.full(len(time_without_night), np.nan), amplitude_without_night, 'x_label', 'y_label', 'here', time_label)
    
    model, regression, amplitude, times_for_matrix = functions.calculate_regression_witha(a[date_int], amplitude_without_night, time_without_night, noon_in_local_time = noon+noon_shift)
    plots.regression_plot(times_for_matrix/3600/10+noon_shift, model, amplitude, 'hours', 'y_label', 'here 2', time_label)
    
    
    # model_total = a[date_int]+regression*np.square(data_colourplot_without_night_np[0,:])
    # plots.regression_plot(data_colourplot_without_night_np[0,:]/3600/10+(noon_shift), model_total, data_colourplot_without_night_np[date_int+1,:], 'hours', 'y_label', 'here2')
    # plots.regression_plot(times_for_matrix, model_total, amplitude, 'x_label', 'y_label', 'here')
    # print(date_int, regression)
    c[date_int] = regression
    
plots.regression_plot(time_for_regression, a, a_corrected, 'days', 'a', 'final regression of a', dates)
    

time_for_regression = np.arange(-len(dates)/2,len(dates)/2)+1
t =  1/150 #2*np.pi/366
# model_c_1, regression = functions.calculate_regression_withcos(c, time_for_regression,time_for_regression)
model_c_1, regression = functions.calculate_regression_withtan(c, time_for_regression,time_for_regression,t)
plots.regression_plot(time_for_regression, model_c_1, c, 'Days', 'Parameter c', 'Regression of parameter c over the year', dates)

for date_int in range(len(date_list)): 
    model_total = a[date_int]+model_c_1[date_int]*np.square(data_colourplot_without_night_np[0,:]-(noon+noon_shift)*60*60*10)
    data_colourplot_4[date_int+1,:] = model_total
        
# plots.colourplot(data_colourplot_4, dates, time_label,  x_axis_number = 20, y_axis_number = 12) # time_label

#%% truncate night values from complete model and plot in a colourplot
counter = 0
for date_int in range(len(date_list)): 
    data_colourplot_4[date_int+1,:] = np.where(np.logical_or((data_colourplot_without_night_np[0,:]/3600/10-noon_shift)%24>sunset_local[counter],(data_colourplot_without_night_np[0,:]/3600/10-noon_shift)%24<sunrise_local[counter]), np.nan, data_colourplot_4[date_int+1,:])
    counter +=1
    # reset the counter after 1 year, that sunrise/ sunset are read out correctly
    if counter >= 364:
        counter-=364
    
   
 
plots.colourplot(data_colourplot_4, dates, time_label,  x_axis_number = 20, y_axis_number = 12) 

    
    
#%%
# t =2*np.pi/366
# plots.regression_plot(time_for_regression_without_nan, np.cos(time_for_regression_without_nan*t), c_without_nan)

#%% calculation of runtime 
ende_time = time.time()
ende_proc = time.process_time()
print('Total time: {:5.3f}s'.format(ende_time - start_time))
print('System time: {:5.3f}s'.format(ende_proc - start_proc))
print('Finished')


# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 09:12:57 2022

@author: Nadine
"""
import matplotlib.pyplot as plt
import math

# Plot
def single_day_plot(day, month, year, time, amplitude, time_label):
    # Plot single day!
    plt.title('Amplitude Data '+'{:0>2}'.format(day)+'.'+'{:0>2}'.format(month)+'.'+str(year))
    plt.plot(time_label, amplitude)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.xticks(time_label[0:-1:int(len(time)/8)])
    plt.show()
    
    
def colourplot(data_colourplot_np, dates, time_label, x_axis_number = 20, y_axis_number = 12):
    # Plot the data as colourplot with x-axis = time, y-axis = date, data = amplitude
    plt.pcolor(dates, data_colourplot_np[0],data_colourplot_np[1:].T)
    plt.ylabel('Time')
    plt.xlabel('Date')
    plt.title('Amplitude data of NAA-transmitter over one astronomical year')
    plt.yticks(data_colourplot_np[0][::int(len(time_label)/y_axis_number)] ,time_label[::int(len(time_label)/y_axis_number)])
    plt.xticks(dates[::math.floor(len(dates)/x_axis_number)], dates[::math.floor(len(dates)/x_axis_number)], rotation = 90)
    # plt.xticks(dates[::math.floor(len(dates)/11)], ['Dez 08', 'Jan 09', 'Feb 09', 'Mar 09', ' May 09', 'Jun 09', 'Jul 09','Aug 09', 'Sep 09', 'Oct 09', 'Nov 09', 'Dez 09'], rotation = 90)
    plt.colorbar()
    plt.show()
    
def regression_plot(times_for_matrix, model, amplitude, x_label, y_label, title, dates):
    # Plot the regression curve
    # plt.fig(figsize=(8, 6), dpi=80)
    plt.plot(times_for_matrix, model, 'r', label="model curve")
    plt.plot(times_for_matrix, amplitude, label="datapoints")
    plt.legend(loc="lower center")
    plt.xlabel(x_label)
    # print(math.floor(len(times_for_matrix)/10), math.floor(len(dates)/10))
    plt.xticks(times_for_matrix[::math.floor(len(times_for_matrix)/10)], dates[::math.floor(len(dates)/10)], rotation = 45)
    # plt.xticks(times_for_matrix[::math.floor(len(times_for_matrix)/10)], times_for_matrix[::math.floor(len(times_for_matrix)/10)]/3600, rotation = 45)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    
    
def regression_plot_one(times_for_matrix, amplitude, x_label, y_label, title, label):
    # Plot the regression curve
    # plt.figure(figsize=(8,6))
    # plt.plot(times_for_matrix, model, 'r', label="model curve")
    plt.plot(times_for_matrix, amplitude, label="datapoints")
    plt.legend(loc="lower center")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(times_for_matrix[::math.floor(len(times_for_matrix)/20)], label[::math.floor(len(label)/20)], rotation = 90)
    plt.show()
    
def regression_year_plot(regression_year, date, title, dates, x_axis_number):
    fig, ax1 = plt.subplots()
    fig.suptitle("%s"%title)#, fontsize=16)
    # Plot the regression curve
    ax1.plot(date, regression_year[:,0], 'r')
    ax1.tick_params(axis ='y', labelcolor = 'r')  
    ax1.set_ylabel('a', color = 'r')
    ax1.set_xticks(date[::math.floor(len(dates)/x_axis_number)])
    ax1.set_xticklabels(dates[::math.floor(len(dates)/x_axis_number)], rotation = 90)
    ax1.set_xlabel('date')
    
    ax2 = ax1.twinx() 
    ax2.plot(date, regression_year[:,1], 'b')
    ax2.tick_params(axis ='y', labelcolor = 'b') 
    ax2.set_ylabel('c', color = 'b')
    
    
    
    # plt.legend(loc="center left")
    # ax1.set_xticks(regression_year)
    # print(len(dates), (dates[::math.floor(len(dates)/x_axis_number)]))
    
    plt.show()
    
def plot_one_curve(x, y, label, title, x_label, y_label, color):
    # Plot the regression curve
    plt.plot(x, y, '%s'%color, label="%s"%label)
    plt.title('%s'%title)
    plt.ylabel('%s'%y_label)
    plt.xlabel('%s'%x_label)
    plt.legend(loc="upper left")
    plt.show()
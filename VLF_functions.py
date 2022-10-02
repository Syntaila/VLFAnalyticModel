# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 09:27:51 2022

@author: Nadine
"""
import numpy as np
import matplotlib as plt
import math

def calculate_regression_for_polynomial(amplitude, times_for_matrix, noon_in_local_time = 16):
    """
    Function: a+cx2
    
    Solve a linear least square problem: Ax = b (Regression)
    -> A.T@A@x = A.T@b
    -> x = (A.T@A)^-1@A.T@b
    A = np.array([[1,1,1,...],[t1,t2,t3,t4]]) (here quadratic approach/ansatz -> t1^2,...)
    b = np.array([amplitude1, amplitude2,...])
    x = [a,b,c] -> a+b*x+c*x^2 (here b = 0 because we define highlight at the noon)
    -> can also be solved with scipy.optimize
    Input:
        ----------------------------------------------------------------------
        amplitude_np: np array of amplitude values
        time_np: np array of time values
        noon_in_local_time: time of noon in local time in hours
    
    Output:
        ----------------------------------------------------------------------
        model, regression, amplitude, times_for_matrix
    """    
    
    # create matrix A -> np.array([[1,1,1,...],[t1,t2,t3,t4]])
    matrix = np.append([np.ones(len(times_for_matrix))],[np.square(times_for_matrix)], axis = 0).T
    # solve the linear least squares system
    regression = np.linalg.solve(np.matmul(matrix.T,matrix),matrix.T@amplitude)
    # print(matrix)
    # regression = np.matmul(np.matmul(np.linalg.inv(np.matmul(matrix.T,matrix)),matrix.T),amplitude)
    
    # model = a+c*x^2 
    model = regression[0]+regression[1]*np.square(times_for_matrix)
    # additional: timesynchronisation can be added (noon = 0, sunset = -1, sundown = 1)
    # print(regression)
    # print(model)
    return model, regression, amplitude, times_for_matrix

def calculate_regression_for_day(amplitude, times_for_matrix, noon_in_local_time = 16):
    """
    Function: a+cx2
    
    Solve a linear least square problem: Ax = b (Regression)
    -> A.T@A@x = A.T@b
    -> x = (A.T@A)^-1@A.T@b
    A = np.array([[1,1,1,...],[t1,t2,t3,t4]]) (here quadratic approach/ansatz -> t1^2,...)
    b = np.array([amplitude1, amplitude2,...])
    x = [a,b,c] -> a+b*x+c*x^2 (here b = 0 because we define highlight at the noon)
    -> can also be solved with scipy.optimize
    Input:
        ----------------------------------------------------------------------
        amplitude_np: np array of amplitude values
        time_np: np array of time values
        noon_in_local_time: time of noon in local time in hours
    
    Output:
        ----------------------------------------------------------------------
        model, regression, amplitude, times_for_matrix
    """    
    
    # create matrix A -> np.array([[1,1,1,...],[t1,t2,t3,t4]])
    t = 2*np.pi/(24*3600)
    
    # function: a + c*cos(tx)+1
    matrix = np.append([np.ones(len(times_for_matrix))],[np.ones(len(times_for_matrix))*(np.cos(times_for_matrix*t)+1)], axis = 0).T
    # print(matrix)
    # solve the linear least squares system
    regression = np.linalg.solve(np.matmul(matrix.T,matrix),matrix.T@amplitude)
    # regression = np.matmul(np.matmul(np.linalg.inv(np.matmul(matrix.T,matrix)),matrix.T),amplitude)
    # print(regression)
    
    # model = a+c*x^2 
    model = regression[0]+regression[1]*(np.cos(times_for_matrix*t)+1)
    # print(model)
    # additional: timesynchronisation can be added (noon = 0, sunset = -1, sundown = 1)
    return model, regression, amplitude, times_for_matrix



def calculate_regression_sin(amplitude_np, time_np, noon_in_local_time = 16):
    """
    Solve a linear least square problem: Ax = b (Regression)
    -> A.T@A@x = A.T@b
    -> x = (A.T@A)^-1@A.T@b
    A = np.array([[1,1,1,...],[t1,t2,t3,t4]]) (here quadratic approach/ansatz -> t1^2,...)
    b = np.array([amplitude1, amplitude2,...])
    x = [a,b,c] -> a+b*x+c*x^2 (here b = 0 because we define highlight at the noon)
    -> can also be solved with scipy.optimize
    Input:
        ----------------------------------------------------------------------
        amplitude_np: np array of amplitude values
        time_np: np array of time values
        noon_in_local_time: time of noon in local time in hours
    
    Output:
        ----------------------------------------------------------------------
        model, regression, amplitude, times_for_matrix
    """    
    # find out the indices where the data is not nan
    index_amplitude = np.where(~np.isnan(amplitude_np))
    amplitude = amplitude_np[index_amplitude]
    times_for_matrix = time_np[index_amplitude]-noon_in_local_time*60*60
    t = 2*np.pi/24
    # create matrix A -> np.array([[1,1,1,...],[t1,t2,t3,t4]])
    matrix = np.append([np.ones(len(times_for_matrix))],[(np.cos(np.square(times_for_matrix*t))+1)], axis = 0).T
    # solve the linear least squares system
    regression = np.linalg.solve(np.matmul(matrix.T,matrix),matrix.T@amplitude)
    # regression = np.matmul(np.matmul(np.linalg.inv(np.matmul(matrix.T,matrix)),matrix.T),amplitude)
    
    # model = a+c*x^2 
    model = regression[0]+regression[1]*(np.cos(np.square(times_for_matrix*t))+1)
    # additional: timesynchronisation can be added (noon = 0, sunset = -1, sundown = 1)
    return model, regression, amplitude, times_for_matrix


def calculate_regression_witha(a, amplitude_np, time_np, noon_in_local_time = 16):
    """
    Solve a linear least square problem: Ax = b (Regression)
    -> A.T@A@x = A.T@b
    -> x = (A.T@A)^-1@A.T@b
    A = np.array([[1,1,1,...],[t1,t2,t3,t4]]) (here quadratic approach/ansatz -> t1^2,...)
    b = np.array([amplitude1, amplitude2,...])
    x = [a,b,c] -> a+b*x+c*x^2 (here b = 0 because we define highlight at the noon)
    -> can also be solved with scipy.optimize
    Input:
        ----------------------------------------------------------------------
        amplitude_np: np array of amplitude values
        time_np: np array of time values
        noon_in_local_time: time of noon in local time in hours
    
    Output:
        ----------------------------------------------------------------------
        model, regression, amplitude, times_for_matrix
    """    
    # find out the indices where the data is not nan
    index_amplitude = np.where(~np.isnan(amplitude_np))
    amplitude = amplitude_np[index_amplitude]
    times_for_matrix = time_np[index_amplitude]-noon_in_local_time*60*60*10
    # print(noon_in_local_time*60*60, times_for_matrix[-8], times_for_matrix[-8]-noon_in_local_time*60*60)
    # print('times for matrix',times_for_matrix,'ursprüngliche zeit', time_np)
    # create matrix A -> np.array([[1,1,1,...],[t1,t2,t3,t4]])
    matrix = np.square(times_for_matrix)
    # solve the linear least squares system
    # print('amplitude',len(amplitude), amplitude,'matrix', len(matrix), matrix)
    regression = np.matmul(matrix.T,amplitude-a)/np.matmul(matrix.T,matrix)
    # print('regression',regression)
    # model = a+c*x^2 
    model = a+regression*np.square(times_for_matrix)
    # print('a+c',a, regression)
    # additional: timesynchronisation can be added (noon = 0, sunset = -1, sundown = 1)
    return model, regression, amplitude, times_for_matrix



def calculate_regression_withcos(c, time_for_regression, timeformodel):
    """
    """
    c_index = np.where(~np.isnan(c))
    c_without_nan = c[c_index]
    time_for_regression_without_nan = time_for_regression[c_index]
    
    t = 2*np.pi/366
    
    matrix_0 = np.append([np.ones(len(time_for_regression_without_nan))],[np.ones(len(time_for_regression_without_nan))*(np.cos(time_for_regression_without_nan*t)+1)], axis = 0)
    matrix = np.append(matrix_0,[np.square(time_for_regression_without_nan)*(np.cos(time_for_regression_without_nan*t)+1)], axis = 0).T

    # regression = np.linalg.solve(np.matmul(matrix.T,matrix),matrix.T@c_without_nan)
    regression =  np.matmul(np.matmul(np.linalg.inv(np.matmul(matrix.T,matrix)),matrix.T),c_without_nan)
    
    model = regression[0]+regression[1]*(np.cos(timeformodel*t)+1)+regression[2]*np.square(timeformodel)*(np.cos(timeformodel*t)+1)
    
    return model, regression

def calculate_regression_withtan(c, time_for_regression,timeformodel,t=1):
    """
    """
    c_index = np.where(~np.isnan(c))
    c_without_nan = c[c_index]
    time_for_regression_without_nan = time_for_regression[c_index]
    
    # t = 2*np.pi/366
    # t = 1
    #a + b tan(1.9*x)^2
    
    matrix = np.append([np.ones(len(time_for_regression_without_nan))],[(np.square(np.tan(t*time_for_regression_without_nan)))], axis = 0).T
    # matrix = np.append(matrix_0,[np.square(time_for_regression_without_nan)*(np.cos(time_for_regression_without_nan*t)+1)], axis = 0).T

    # regression = np.linalg.solve(np.matmul(matrix.T,matrix),matrix.T@c_without_nan)
    regression =  np.matmul(np.matmul(np.linalg.inv(np.matmul(matrix.T,matrix)),matrix.T),c_without_nan)
    
    model = regression[0]+regression[1]*np.square(np.tan(timeformodel*t))
    
    return model, regression


def outlier_detection(model, amplitude, times_for_matrix, percent_distance_accepted = 10):
    """
    outlier detection: values in amplitude will be deleted if they are too far away from the mean
    
    """
    # outlier detection -> Alle werte die zu weit von der kurve weg sind raus und neu regression machen
    residual = model-amplitude
    mean_residual = np.nanmean(abs(residual))
    std_residual = np.std(residual)
    # print('mean',mean_residual)
    amplitude_corrected = np.full(len(amplitude), np.nan)
    times_for_matrix_corrected = np.full(len(times_for_matrix), np.nan)
    for l in range(len(amplitude)):
        if amplitude[l] > model[l]+mean_residual*percent_distance_accepted or amplitude[l] < model[l]-mean_residual*percent_distance_accepted:
            # print('value', amplitude[l],' is removed because of %s abweichung (%s percent)'%(residual[l], residual[l]/mean_residual))
            pass
        else:
            amplitude_corrected[l] = amplitude[l]
            times_for_matrix_corrected[l] = times_for_matrix[l]
    return amplitude_corrected, times_for_matrix_corrected
     
def average_data(data_np, data_per_day, intervall_time_min = 5):
    # seperate data per day in 5-10 minute intervalls
    data_average_time_list = []
    data_average_time_amplitude = []
    for i in range(int(data_per_day/(intervall_time_min*60*10))): # value is 3000
        start = int(data_per_day/int(data_per_day/(intervall_time_min*60*10))*i)
        end = int(data_per_day/int(data_per_day/(intervall_time_min*60*10))*(i+1))

        data_average_time = np.nanmean(data_np[start:end+1,0])
        data_average_amplitude = np.nanmean(data_np[start:end+1,1])
        data_average_time_list.append(data_average_time)
        data_average_time_amplitude.append(data_average_amplitude)
    return data_average_time_list, data_average_time_amplitude
    
def average_data_2(data_np, data_per_day, intervall_time_min = 5):
    # seperate data per day in 5-10 minute intervalls
    data_average_time_list = []
    data_average_time_amplitude = []
    data_average_time_np = np.full(int(data_per_day/(intervall_time_min*60*10)), np.nan)
    data_average_amplitude_np = np.full(int(data_per_day/(intervall_time_min*60*10)), np.nan)
    for i in range(int(data_per_day/(intervall_time_min*60*10))): # value is 3000
        index_average = np.where(np.logical_and(data_np[:,0] >int(data_per_day/int(data_per_day/(intervall_time_min*60))*i), data_np[:,0] <int(data_per_day/int(data_per_day/(intervall_time_min*60))*(i+1))))
        data_average_time = np.nanmean(data_np[index_average,0])
        data_average_amplitude = np.nanmean(data_np[index_average,1])
        data_average_time_np[i] = data_average_time
        data_average_amplitude_np[i] = data_average_amplitude
        
    return data_average_time_np, data_average_amplitude_np
  


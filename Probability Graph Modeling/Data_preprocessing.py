import math
import numpy as np
from numpy import genfromtxt


# ek dumm se chle gye :((



file1 = open("Complete_Data.xlsx - Dumped_Data.csv",'r')
file2 = open("Normal_Data.csv",'w')
file3 = open("final1.txt",'w')
file4 = open("final2.txt",'w')
read_file = file1.readlines()
flag = 0
count = 0
for line in read_file:
    if flag == 0:
        flag = 1
        file2.write(line)
        file3.write(line)
        file4.write(line)
        count = count + 1
    else:
        count = count+1
        line_split = line.rstrip().split(',')
        for i in range(len(line_split)):
            line_split[i] = math.log1p(float(line_split[i]))
            if i != (len(line_split)-1):
                file2.write(str(line_split[i]) + ',')
            else:
                file2.write(str(line_split[i]))
        file2.write('\n')
file2.close()

normal_data_numpy_array = genfromtxt('Normal_Data.csv', delimiter=',', skip_header=1)
protien_wise_mean = np.mean(normal_data_numpy_array, axis=0)
protien_wise_std = np.std(normal_data_numpy_array, axis=0)
number_of_cols = protien_wise_mean.shape[0]

for i in range(number_of_cols):
    arity_2_right = protien_wise_mean[i] + protien_wise_std[i]
    arity_2_left = protien_wise_mean[i] - protien_wise_std[i]

    protien_column = normal_data_numpy_array[:, i]
    for j in range(protien_column.shape[0]):

        if protien_column[j] > arity_2_left and protien_column[j] < arity_2_right:
            protien_column[j] = 1.0
        else:
            protien_column[j] = 2.0
    normal_data_numpy_array[:, i] = protien_column
np.savetxt(file3,normal_data_numpy_array, delimiter=',')

normal_data_numpy_array1 = genfromtxt('Normal_Data.csv', delimiter=',', skip_header=1)
for i in range(number_of_cols):
    arity_2_right = protien_wise_mean[i] + protien_wise_std[i]
    arity_2_left = protien_wise_mean[i] - protien_wise_std[i]
    arity_3_right = protien_wise_mean[i] + (2*protien_wise_std[i])
    arity_3_left = protien_wise_mean[i] - (2*protien_wise_std[i])

    protien_column =  normal_data_numpy_array1[:, i]
    for j in range(protien_column.shape[0]):

        if protien_column[j] > arity_2_left and protien_column[j] < arity_2_right:
            protien_column[j] = 1
        elif protien_column[j] <= arity_2_left and protien_column[j] > arity_3_left or protien_column[j] >= arity_2_right and protien_column[j] < arity_3_right :
            protien_column[j] = 2
        else:
            protien_column[j] = 3

    normal_data_numpy_array1[:, i] = protien_column
np.savetxt(file4, normal_data_numpy_array1, delimiter=',')
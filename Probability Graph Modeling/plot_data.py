import matplotlib.pyplot as plt
import numpy as np

x = np.zeros((11672,1))
for i in range(11672):
    x[i] = i+1

numpy_array1 = np.loadtxt('Complete_Data.xlsx - Dumped_Data.csv', delimiter=',', skiprows=1)
nc = numpy_array1.shape[1]
for i in range(numpy_array1.shape[1]):
    y = numpy_array1[:, i]
    y = np.sort(-y)
    plt.hist(y)
    # plt.plot(x,y, label='Loaded from file!')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph')
    plt.legend()
    plt.show()

numpy_array1 = np.loadtxt('Normal_Data.csv', delimiter=',', skiprows=1)
nc = numpy_array1.shape[1]
for i in range(numpy_array1.shape[1]):
    y = numpy_array1[:, i]
    y = np.sort(-y)
    plt.hist(y)
    # plt.plot(x,y, label='Loaded from file!')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph')
    plt.legend()
    plt.show()


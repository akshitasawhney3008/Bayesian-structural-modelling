file1 = open("final2.txt",'r')
file2 = open("CompleteData(arity3).csv",'r')
file1_read = file1.readlines()
file2_read = file2.readlines()
count = 0
accuracy = 0
flag = 0
for i in range(len(file1_read)):
    if flag == 0:
        flag = 1
    else:
        line1_split = file1_read[i].rstrip().split(',')
        line2_split = file2_read[i-1].rstrip().split(',')
        for j in range(len(line1_split)):
            if float(line1_split[j]) == float(line2_split[j]):
                count = count+1

accuracy = (count/(len(file1_read)*len(line1_split)))*100
print(accuracy)

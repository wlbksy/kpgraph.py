from student_route import *

s = student(5, [2, 6] )
goal_list = s.demo_nodes

onLink = []
for each in goal_list:
    each_len = len(each)
    for i in range(each_len-1):
        onLink.append((each[i], each[i+1]))

print(onLink)
row_num, col_num = demo_arr.shape

with open('data.js','w') as f:
    f.write("var links = [\n")

    for i in range(row_num):
        for j in range(col_num):
            val = demo_arr[i,j]
            if (i,j) in onLink:
                if val:
                    f.write("""\t{source: %s, target: %s, value: %s, type: "ColorOn"},\n""" % (i,j, val))
                else:
                    f.write("""\t{source: %s, target: %s, value: %s, type: "ColorOn"},\n""" % (j,j, demo_arr[j,j]))
                    demo_arr[j,j]=0
            else:
                if val:
                    f.write("""\t{source: %s, target: %s, value: %s, type: "ColorOff"},\n""" % (i,j, val))

    f.write("];")

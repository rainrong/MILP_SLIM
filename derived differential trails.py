

f1 = open(r"E:\作业\作业\20211228\SLIM\差分路径推导\derived differential trails.txt","a+")
#从文件中按行读取有效数据，第二行起始，并整数型
def read_data_from_txt_file(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        # 跳过第一行
        next(file)
        for line in file:
            # 去掉每行首尾的空格和换行符，并去掉方括号
            line = line.strip().strip('[').strip(']')
            # 将逗号分隔的字符串转换为int类型的数组
            line_data = list(map(int, line.split(', ')))
            # line_data = [int(x) if x else 0 for x in line.split(', ')]  #两行代码均可实现。注意TXT文档最后不要有空行
            # 将每行数据转换为元组，并添加到列表中
            data_list.append(tuple(line_data))
    return data_list


#从文件中按行读取有效数据，第二行起始，并整数型,前x后y个单独成元组元素append返回
def read_data_from_txt_file_SBOX(file_path, x, y):
    data_x = []
    data_y = []
    with open(file_path, 'r') as file:
        # 跳过第一行
        next(file)
        for line in file:
            # 去掉每行首尾的空格和换行符，并去掉方括号
            line = line.strip().strip('[').strip(']')
            # 将逗号分隔的字符串转换为int类型的数组
            line_data = list(map(int, line.split(', ')))
            # 将每行的前 x 个数值存储到 data_x 中,list类型
            data_x.append(list(line_data[:x]))
            # 将每行的后 y 个数值存储到 data_y 中
            data_y.append(list(line_data[-y:]))
    return data_x, data_y


#把一个长度16的列表四等分
def partition_list(lst):
    n = len(lst)
    if n % 4 != 0:
        raise ValueError('List length must be divisible by 4')
    return [lst[i:i+n//4] for i in range(0, n, n//4)]


#P置换
def LinearLaryer(variable):       #线性层||p置换，
        """
        Linear layer of SLIM.
        """
        array = ["" for i in range(0, 16)]

        array[0] = variable[11]
        array[1] = variable[2]
        array[2] = variable[6]
        array[3] = variable[12]
        array[4] = variable[8]
        array[5] = variable[7]
        array[6] = variable[13]
        array[7] = variable[0]
        array[8] = variable[3]
        array[9] = variable[14]
        array[10] = variable[9]
        array[11] = variable[4]
        array[12] = variable[15]
        array[13] = variable[1]
        array[14] = variable[5]
        array[15] = variable[10]

        return array

#异或
def XOR_lists(list1, list2):
    """
    将 list1 和 list2 中的每个元素进行异或操作，返回一个新列表。
    """
    result = []
    for i in range(len(list1)):
        result.append(list1[i] ^ list2[i])
    return result

Sbox_differential_trails = read_data_from_txt_file_SBOX('/作业/作业/20211228/SLIM/差分路径推导/PFP_DifferentialTrails.txt',4,4)
SBOX_size = len(Sbox_differential_trails[0])

#输入差分
s = "00000000000000001001000000000000"  # 输入差分-“二进制字符串”
num = int(s, 2)  # 将“二进制字符串”转换为整数
Initial_difference_IN = [(num >> i) & 0x01 for i in range(31, -1, -1)]  # 将整数拆分为32位，并存储到Initial_difference_IN
# 将列表分成前后两个部分 
'''
# my_list[:16] 获取 my_list 中的前16个元素，将其赋值给变量 first_half，这样就得到了列表的前半部分。
# 然后，我们使用 my_list[16:] 获取 my_list 中的后16个元素，将其赋值给变量 second_half，这样就得到了列表的后半部分。
# 需要注意的是，切片操作返回的是原列表的一个新副本，因此在对切片进行操作时，不会影响原列表。
'''
Initial_difference_IN_LEFT = Initial_difference_IN[:16]
Initial_difference_IN_RIGHT = Initial_difference_IN[16:]

temp_LEFT = []
temp_RIGHT = []
Number_derive = int(input("Input the target round number: "))
while not (Number_derive > 0):
    print("Input a round number greater than 0.")
    Number_derive = int(input("Input the target round number again: "))
COUNTBOX = [[] for _ in range(Number_derive + 1)]
for i in range(Number_derive):#推1轮;程序仍存在一定问题，还没有解决最后异或时，左支哪些输入需要做异或，不能全做的，现在程序是全做
    LEFT_IN_16_list_i = []
    RIGHT_IN_16_list_i = []
    LEFT_OUT_16_list_i = []
    RIGHT_OUT_16_list_i = []
    Sbox_OUT_16_list_i = []

    #赋值左右支输入
    if i == 0:
        #复制列表。使用copy（）函数
        LEFT_IN_16_list_i.append(Initial_difference_IN_LEFT)
        RIGHT_IN_16_list_i.append(Initial_difference_IN_RIGHT)
    else:
        #复制列表。使用切片操作,结果同copy
        LEFT_IN_16_list_i = temp_LEFT.copy()
        RIGHT_IN_16_list_i = temp_RIGHT[:]

    RIGHT_IN_16_list_i_divide = []
    for j in range(len(RIGHT_IN_16_list_i)):
        RIGHT_IN_16_list_i_divide.append(partition_list(RIGHT_IN_16_list_i[j]))#四等分右支
        #过S盒
        SBOX_OUT = [[] for _ in range(4)]#创建长度为 4 的列表，其中每个元素都是一个空列表。装载四个S盒输出的多种情况
        for k in range(SBOX_size):#进S盒
            if Sbox_differential_trails[0][k] == RIGHT_IN_16_list_i_divide[j][0]:
                SBOX_OUT[0].append(Sbox_differential_trails[1][k])
            if Sbox_differential_trails[0][k] == RIGHT_IN_16_list_i_divide[j][1]:
                SBOX_OUT[1].append(Sbox_differential_trails[1][k])
            if Sbox_differential_trails[0][k] == RIGHT_IN_16_list_i_divide[j][2]:
                SBOX_OUT[2].append(Sbox_differential_trails[1][k])
            if Sbox_differential_trails[0][k] == RIGHT_IN_16_list_i_divide[j][3]:
                SBOX_OUT[3].append(Sbox_differential_trails[1][k])
    
        len_SBOX_OUT0 = len(SBOX_OUT[0])
        len_SBOX_OUT1 = len(SBOX_OUT[1])
        len_SBOX_OUT2 = len(SBOX_OUT[2])
        len_SBOX_OUT3 = len(SBOX_OUT[3])
        if len(COUNTBOX[i+1]) > 0:
            COUNTBOX[i+1].append(len_SBOX_OUT0*len_SBOX_OUT1*len_SBOX_OUT2*len_SBOX_OUT3+COUNTBOX[i+1][-1])   
        else:
            COUNTBOX[i+1].append(len_SBOX_OUT0*len_SBOX_OUT1*len_SBOX_OUT2*len_SBOX_OUT3)     
        # SBOX_OUT_for_Permutation = [[] for _ in range(len_SBOX_OUT0*len_SBOX_OUT1*len_SBOX_OUT2*len_SBOX_OUT3)]#创建长度为S盒输出所有情况组合的列表，其中每个元素都是一个空列表
        SBOX_OUT_for_Permutation = []#16长度元组情况,亦即Permutation_IN[]
        for j0 in range(len_SBOX_OUT0):
            for j1 in range(len_SBOX_OUT1):
                for j2 in range(len_SBOX_OUT2):
                    for j3 in range(len_SBOX_OUT3):
                        SBOX_OUT_for_Permutation.append(SBOX_OUT[0][j0] + SBOX_OUT[1][j1] + SBOX_OUT[2][j2] + SBOX_OUT[3][j3])

        #过P置换
        Permutation_OUT = [LinearLaryer(x) for x in SBOX_OUT_for_Permutation]

        #异或
        XOR_LEFT_IN_Number = 0
        for k in range(len(COUNTBOX[i])):
            if COUNTBOX[i][k] > j:
                XOR_LEFT_IN_Number = k
                break 

        XOR_OUT = []
        for k in range(len(Permutation_OUT)):
             XOR_OUT.append(XOR_lists(LEFT_IN_16_list_i[XOR_LEFT_IN_Number], Permutation_OUT[k]))

        #添加到右支输出
        RIGHT_OUT_16_list_i.extend(XOR_OUT)


    # LEFT_OUT_16_list_i = RIGHT_IN_16_list_i.copy
    # temp_LEFT = RIGHT_IN_16_list_i.copy()
    # temp_RIGHT = RIGHT_OUT_16_list_i.copy()

    #去重复，导入
    temp_LEFT = list(set(tuple(x) for x in RIGHT_IN_16_list_i))
    temp_LEFT = [list(x) for x in temp_LEFT]

    #去重复，导入
    temp_RIGHT = list(set(tuple(x) for x in RIGHT_OUT_16_list_i))
    temp_RIGHT = [list(x) for x in temp_RIGHT]



derived_result = "result_" + "_1round_derived differential trails" + ".txt"
with open(derived_result, "w") as f:  
    f.write("OUTPUT_LEFT\n")
    for kk in range(len(temp_LEFT)):        
        for item in temp_LEFT[kk]:
            f.write(str(item))
        f.write("\n")

    f.write("\n")
    f.write("OUTPUT_RIGHT\n")
    for kk in range(len(temp_RIGHT)):        
        for item in temp_RIGHT[kk]:
            f.write(str(item))
        f.write("\n")

print(temp_LEFT)
print(temp_RIGHT)





        




    
    
    



    




        

    
    
    



        
    

















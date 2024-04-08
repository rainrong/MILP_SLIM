# import numpy as np
# #from scipy.linalg import solve
# np.set_printoptions(threshold=np.inf) # np.inf表示正无穷
# f1 = open(r"C:\Users\BIXINJIE\Desktop\DDTM-Shadow-32.txt","a+")

# #循环左移
# def Rotateleft(a,x,l):
#     temp=x%l
#     temp1=(a<<temp)%int(np.exp2(l))
#     temp2=(a<<temp)/int(np.exp2(l))
#     temp3=temp1+temp2
#     return int(temp3)

# #创建S盒
# S_BOX=np.zeros((16), dtype=int)#创建全0 S盒
# temp = np.zeros((4), dtype=int)#创建全0 S盒
# for i in range(16):
#     T = '{:04b}'.format(i)
#     temp[3] = T[3]&T[2]^T[1]
#     temp[1] = T[2]&T[1]^T[0]
#     temp[2] = T[3]&temp[1]^T[2] = T[3]&(T[2]&T[1]^T[0])^T[2]
#     temp[0] = T[0]&temp[3]^T[3] = T[0]&(T[3]&T[2]^T[1])^T[3]


#     #S_BOX[i]=(Rotateleft(i,1,16)&Rotateleft(i,7,16))^Rotateleft(i,2,16)
#     S_BOX[i]=Rotateleft(i,1,8)&Rotateleft(i,7,8)^Rotateleft(i,2,8)

# print('S盒：')
# print('S盒：',file=f1)    #s盒
# for i in range(256):
#     print('{:<3d}'.format(i),'{:<3d}'.format(S_BOX[i]))
#     print('{:<3d}'.format(i),'{:<3d}'.format(S_BOX[i]),file=f1)
    
# #    print('{:<16d}'.format(i),',','{:<16d}'.format(S_BOX[i],end=' '),file=f1)    #s盒
    


# #DDT = [[0] * 256 for _ in range(256)]   #语法水平orz...

# for i in range(0,8):
#     i2 = int(np.exp2(i))
#     print('输入差分:')
#     print('输入差分:',file=f1)
#     print(' {:08b}'.format(i2))
#     print(' {:08b}'.format(i2),file=f1)
#     DDT = np.zeros((256), dtype=int)
#     for j in range(0, 256):
#         c = S_BOX[j] ^ S_BOX[j ^ i2]                             
#         DDT[c]= DDT[c] + 1
#     print('输出差分，概率:')
#     print('输出差分，概率:',file=f1)
#     for j in range(0, 256):
#         if DDT[j]!=0:
#             print(' {:08b}'.format(j),', 2^%d'%np.log2(DDT[j]/256))
#             print(' {:08b}'.format(j),', 2^%d'%np.log2(DDT[j]/256),file=f1)





f1 = open(r"E:\作业\作业\20211228\SLIM\密钥扩展DDT\key_schedule_subkey.txt","a+")

array1 = []
KeyMSB = []
KeyLSB = []
for i in range(0,5):
    for j in range(0, 16):               
        array1.append("k" + str(i*16+j))
        n = i*16 + j
        if n < 40:
            KeyLSB.append("k" + str(i*16+j))
        else:
            KeyMSB.append("k" + str(i*16+j))


            


# KeyMSB = []
# KeyLSB = []
# for i in range(0,40):
#     KeyLSB.append(array1[i])
# for i in range(40,80):
#     KeyMSB.append(array1[i])

def shift_left_x(lst,x):
    """
    将列表内的元素循环左移x个位置
    """
    # 切片取出前x个元素
    first_x = lst[:x]
    # 从第三个元素开始取到末尾
    remaining = lst[x:]
    # 将前两个元素添加到列表末尾
    shifted_lst = remaining + first_x
    return shifted_lst


for i in range(0,5):  
    print("")
    print("",file=f1)
    print("")
    print("",file=f1)
    print(f"Key_{i}:", end="")
    print(f"Key_{i}:", end="",file=f1)  
    for j in range(0, 16):               
        print(array1[i*16+j], end="")
        print(array1[i*16+j],file=f1, end="")
print("")
print("",file=f1)


for i in range(5,14):#轮数高了文件会大
    MSB16_list_i = []
    LSB16_list_i = []
    for j in range(4):
        index = (i-5)*4 + j
        # 如果index超出list1的范围，重新从头开始
        if index >= 10:
            index %= 10
        for k in range(4):
             MSB16_list_i.append(KeyMSB[index*4+k])
             LSB16_list_i.append(KeyLSB[index*4+k])
    
    LSB16_list_i = shift_left_x(LSB16_list_i,2)
    for j in range(16):
        LSB16_list_i[j] = LSB16_list_i[j] + "⊕" + MSB16_list_i[j]

    SUB16 = []
    for j in range(4):
        for k in range(4):
            if k == 0:
                SUB16.append(LSB16_list_i[4*j] + "&" +(LSB16_list_i[4*j+3] + "&" +LSB16_list_i[4*j+2] + "⊕" +LSB16_list_i[4*j+1]) + "⊕" +LSB16_list_i[4*j+3])
            if k == 1:
                SUB16.append(LSB16_list_i[4*j+2] + "&" +LSB16_list_i[4*j+1] + "⊕" +LSB16_list_i[4*j])
            if k == 2:
                SUB16.append(LSB16_list_i[4*j+3] + "&" +(LSB16_list_i[4*j+2] + "&" +LSB16_list_i[4*j+1] + "⊕" +LSB16_list_i[4*j]) + "⊕" +LSB16_list_i[4*j+2])    
            if k == 3:
                SUB16.append(LSB16_list_i[4*j+3] + "&" +LSB16_list_i[4*j+2] + "⊕" +LSB16_list_i[4*j+1])
    
    MSB16_list_i = shift_left_x(MSB16_list_i,3)
    for j in range(16):
        MSB16_list_i[j] = SUB16[j] + "⊕" + MSB16_list_i[j]
    print("")
    print("",file=f1)  
    print(f"Key_{i}:", MSB16_list_i)
    print(f"Key_{i}:", MSB16_list_i,file=f1)

    for j in range(4):
        index = (i-5)*4 + j
        # 如果index超出list1的范围，重新从头开始
        if index >= 10:
            index %= 10
        for k in range(4):
             KeyMSB[index*4+k] = MSB16_list_i[4*j+k]
             KeyLSB[index*4+k] = SUB16[4*j+k]



            

#     temp[3] = LSB16_list_i[3] + "&" +LSB16_list_i[2] + "⊕" +LSB16_list_i[1]
#     temp[1] = LSB16_list_i[2] + "&" +LSB16_list_i[1] + "⊕" +LSB16_list_i[0]
#     temp[2] = LSB16_list_i[3] + "&" +LSB16_list_iemp[1] + "⊕" +LSB16_list_i[2] = LSB16_list_i[3] + "&" +(LSB16_list_i[2] + "&" +LSB16_list_i[1] + "⊕" +LSB16_list_i[0]) + "⊕" +LSB16_list_i[2]
#     temp[0] = LSB16_list_i[0] + "&" +LSB16_list_iemp[3] + "⊕" +LSB16_list_i[3] = LSB16_list_i[0] + "&" +(LSB16_list_i[3] + "&" +LSB16_list_i[2] + "⊕" +LSB16_list_i[1]) + "⊕" +LSB16_list_i[3]
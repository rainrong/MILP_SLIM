def read_data_from_txt_file(filename):
    with open(filename, 'r') as f:
        # 读取文件内容到变量lines中
        lines = f.readlines()
        
        # 跳过前三行,则lines = lines[3:]
        lines = lines[4:]
        
        # 创建一个空列表，用于存储读取的数据
        data_list = []
        
        # 循环处理每行数据
        for line in lines:
            # 删除每行首尾的空格，并将二进制字符串转换为整数
            data = int(line.strip(), 2)
            
            # 将整数添加到data_list列表中
            data_list.append(data)
        
        # 返回data_list列表
        return data_list


def to_binary_list(num):
    # 将整数转换为二进制字符串
    binary_str = bin(num)[2:]
    # 如果字符串长度不足16位，在前面补0
    if len(binary_str) < 16:
        binary_str = '0' * (16 - len(binary_str)) + binary_str
    # 将字符串转换为列表
    binary_list = [int(x) for x in binary_str]
    return binary_list


output = read_data_from_txt_file('/作业/作业/20211228/SLIM/差分路径推导/result__1round_derived differential trails.txt')
print(output)

ADD_list = [0] * 16
for i in range(len(output)):
    B = to_binary_list(output[i])
    for j in range(16):
        ADD_list[j] += B[j]    #加和对应位数的数值，判断0，*，1

print(len(output))
print(ADD_list)

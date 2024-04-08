"""
x_i_63,x_i_62,....x_i_0 denote the input to the (i+1)-th round.
"""
#注释中元组概念本人并没去学习理解就直接顾自用了


from gurobipy import *

import time


class SLIM:
    def __init__(self, Round):
        self.Round = Round
        self.number = 0
        self.my_var = True  # 或者 False
        self.blocksize = 32
        self.filename_model = "SLIM_" + str(self.Round) +"_" + str(self.number) + ".lp"
        self.filename_result = "result_" + str(self.Round) + "_IDC" + ".txt"
        fileobj = open(self.filename_model, "w")
        fileobj.close()
        fileboj = open(self.filename_result, "w")
        fileobj.close()
        self.Globaly = 0   #S盒标识位，表示S盒是否活跃   ？
        self.dnum = 0     #异或标识位，表示S盒是否活跃
        self.variablein0 = []
        self.variableoutN = []

        
        

    # Linear inequalities for the SLIM Sbox
    S_T = [[3, 4, 4, 1, -2, 0, -2, 1, 0],
           [0, -2, -2, 3, 4, 1, 4, 1, 0],
           [-2, 1, 1, 3, 1, -1, 1, 2, 0],
           [1, -3, -2, -2, 3, -4, 1, -3, 10],
           [-1, -2, -2, -1, -1, 2, -1, 0, 6],
           [2, 1, 1, -3, 1, 2, 1, 2, 0],
           [-2, -2, 1, -1, -2, -1, 1, 0, 6],
           [-1, 2, -3, 1, -1, -2, -3, -3, 10],
           [-1, 1, 1, -1, 0, 0, 0, -1, 2],
           [2, -1, 2, 2, 2, 3, -1, -1, 0],
           [2, 3, -2, -4, -4, -4, -1, 1, 11],
           [2, 2, -1, 2, -1, 3, 2, -1, 0],
           [-1, -3, 2, 1, -3, -2, -1, -3, 10],
           [-1, 0, -1, -1, 1, 0, -1, 0, 3],
           [0, -1, -1, 1, -1, 0, -1, 1, 3],
           [0, -1, 1, -1, 0, -1, -1, 1, 3],
           [-2, 0, 0, 1, 2, 1, 2, 1, 0],
           [0, -2, -2, -2, -1, 2, -1, -1, 7],
           [2, 3, 3, 2, 1, -4, 1, 1, 0],
           [1, -2, -3, -2, 1, -4, 3, -3, 10],
           [0, 1, 1, -1, -1, 1, -1, 0, 2],
           [1, 1, 1, 1, 1, 1, -2, 1, 0],
           [2, 1, 1, 0, -2, 1, 1, 2, 0]]
    NUMBER = 9                               #刻画S盒不等式元组大小

    def CreateObjectiveFunction(self):
        """
        创建MILP模型的目标函数
        """
        fileobj = open(self.filename_model, "a")
        # fileobj.write("Minimize\n")
        fileobj.write("MAXIMIZE\n")
        eqn = []
        for i in range(0, self.Round * 4):    ###？？？PFP为16，感觉应该是8，轮函数内有8个S盒；SLIM 4个   
            eqn.append("y" + str(i))          
        temp = " + ".join(eqn)  # 元素中间添加 “+”
        fileobj.write(temp)
        fileobj.write("\n")
        fileobj.close()

    @staticmethod
    def CreateLeftVariables(n):
        """
        生成模型中左支的输入变量
        """
        array = []
        for i in range(0, 16):
            array.append(("x" + "_" + str(n) + "_" + str(i)))
        return array

    @staticmethod
    def CreateRightVariables(n):
        """
        生成模型中右支的输入变量
        """
        array = []
        for i in range(16, 32):
            array.append(("x" + "_" + str(n) + "_" + str(i)))
        return array

    @staticmethod
    def CreateLeftOutVariables(n):
        """
        生成模型中左支的输出变量
        """
        array = []
        for i in range(48, 64):
            array.append(("x" + "_" + str(n) + "_" + str(i)))
        return array

    @staticmethod
    def CreateSboxVariables(n):
        """
        生成模型中S盒的变量 
        """
        array = []
        for i in range(32, 48):       
            array.append(("x" + "_" + str(n) + "_" + str(i)))
        return array

    """
    @staticmethod
    def CreatePVariables(n):
        
        生成模型中P变换后的变量
        
        array = []
        for i in range(96, 128):
            array.append(("x" + "_" + str(n) + "_" + str(i)))
        return array
    """

    @staticmethod
    def CreateIDAInputVariables(nn):
        """
        生成模型中第一轮输入变量字（nibble）
        """
        n = nn//120#整除结果为整数
        t1 = n//15
        t2 = int(n%15)   
        temp3 = '{:04b}'.format(t2+1)

        array = []
        if t1 > 0:
            for i in range(0, 4*t1):
                array.append(0)       
    
        for j in range(0, 4):#4*t1~4*t1+4
                array.append(temp3[j])
                
        if t1 < 7:
            for i in range(4*t1+4, 32):
                array.append(0)  
        
        str_array = [str(x) for x in array]#将一个list中元素全部变成字符串类型,也可以利用map函数：str_list = list(map(str, my_list))
        return str_array
    
    @staticmethod
    def CreateIDAOutputVariables(nn):
        """
        生成模型中末轮输出变量字（nibble）
        """

        n = int(nn%120)
        t1 = n//15
        t2 = int(n%15)
        temp3 = '{:04b}'.format(t2+1)

        array = []
        if t1 > 0:
            for i in range(0, 4*t1):
                array.append(0)       
    
        for j in range(0, 4):#4*t1~4*t1+4
                array.append(temp3[j])
                
        if t1 < 7:
            for i in range(4*t1+4, 32):
                array.append(0)  

        str_array = [str(x) for x in array]#将一个list中元素全部变成字符串类型,也可以利用map函数：str_list = list(map(str, my_list))
        return str_array
    
    #IDA左支差分约束，内容同交叉约束
    def IDAConstraintsByCopyLeft(self, variable1, variable2):
        """
        Generate the constraints by copy operation.
        """
        
        fileobj = open(self.filename_model, "a")
        for i in range(0, 16):     #分支长度 即1/2分组长度
            temp = []
            temp.append(variable2[i])
            temp.append(variable1[i])            
            s = " = ".join(temp)
            # s = " - ".join(temp)
            # s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()

    #IDA右支差分约束，内容同交叉约束
    def IDAConstraintsByCopyRight(self, variable1, variable2):
        """
        Generate the constraints by copy operation.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(16, 32):     #分支长度 即1/2分组长度
            temp = []            
            temp.append(variable2[i-16])
            temp.append(variable1[i])
            s = " = ".join(temp)
            # s = " - ".join(temp)
            # s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()



    def ConstraintsBySbox(self, variable1, variable2):
        """
        Generate the constraints by sbox layer.
        """
        fileobj = open(self.filename_model, "a")
        for k in range(0, 4):          #轮函数4个S盒
            for coff in SLIM.S_T:      #SLIM.S_T - 刻画S盒的不等式元组
                temp = []
                for u in range(0, 4):   #遍历不等式中S盒输入系数
                    temp.append(str(coff[u]) + " " + variable1[(k * 4) + u])  #variable1  S盒右支输入变量；4-S盒为4bit输入； k- 分组长度64，右支32,32/4=8 需遍历k=8次
                for v in range(0, 4):   #遍历不等式中S盒输出系数
                    temp.append(str(coff[v + 4]) + " " + variable2[(k * 4) + v])  #v+4 - 不等式中S盒输出系数位置
                temp1 = " + ".join(temp)            #在各项间添加“+”成式
                temp1 = temp1.replace("+ -", "- ")   # 对于负数 省略“+”号衔接
                s = str(-coff[SLIM.NUMBER - 1])    #定位取出该不等式的最后一个元素，并在前面添加“-”号，为了移到不等式右边
                s = s.replace("--", "")    #接前，本来就是负数的，消“-”号
                temp1 += " >= " + s    #添加" >= "，和最后一个元素·
                fileobj.write(temp1)
                fileobj.write("\n")
            eqn = []
            eqn.append(' + '.join(variable1[(k * 4) + u] for u in range(0, 4)) + ' - y' + str(self.Globaly) + ' >= 0')   
            #y0 S盒标志位，表示S盒是否活跃  
            #当 Ａ＝１时，Δｘ０，Δｘ１，Δｘ２，Δｘ３ 必定有一个非零
            #例:x_0_35 + x_0_34 + x_0_33 + x_0_32 - y0 >= 0             
            for t in range(0, 4):
                eqn.append(variable1[(k * 4) + t] + ' - y' + str(self.Globaly) + ' <= 0')   #为 了 保 证 Δｘ０，Δｘ１，Δｘ２，Δｘ３ 有 任 意 一个是１时，y0＝１，用不等式约束；
            '''
            例:
            x_0_35 - y0 <= 0
            x_0_34 - y0 <= 0
            x_0_33 - y0 <= 0
            x_0_32 - y0 <= 0
            '''
            for var in eqn:
                fileobj.write(var + '\n')
            self.Globaly += 1
        fileobj.close()


     #feistel交叉操作差分约束
    def ConstraintsByCopy(self, variable1, variable2):
        """
        Generate the constraints by copy operation.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 16):     #分支长度 即1/2分组长度
            temp = []
            temp.append(variable1[i])
            temp.append(variable2[i])
            s = " - ".join(temp)
            s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()


    # 异或约束
    def ConstraintsByXor(self, variable1, variable2, variable3):
        """
        Generate the constraints by Xor operation.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 16):       #异或差分约束； 2.2有差分MILP的原理文章中，有介绍２０１７ 年 欧 洲 密 码 年 会 上，Ｓａｓａｋｉ等 人 针 对ＸＯＲ操作，改进
            temp = []               #temp重置
            temp.append(variable1[i] + ' + ' + variable2[i] + ' + ' + variable3[i] + ' - 2 d_' + str(self.dnum) + ' >= 0')
            temp.append(variable1[i] + ' - d_' + str(self.dnum) + ' <= 0')
            temp.append(variable2[i] + ' - d_' + str(self.dnum) + ' <= 0')
            temp.append(variable3[i] + ' - d_' + str(self.dnum) + ' <= 0')
            temp.append(variable1[i] + ' + ' + variable2[i] + ' + ' + variable3[i] + ' <= 2')
            for var in temp:          #每次temp会重置
                fileobj.write(var + '\n')
            self.dnum += 1
        fileobj.close()

    @staticmethod
    def LinearLaryer(variable):       #线性层||p置换，
        """
        Linear layer of Present.
        """
        array = ["" for i in range(0, 16)]
        '''
        for i in range(0, 31):
            array[(8 * i) % 31] = variable[i]
        array[31] = variable[31]
        '''
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

    '''
    #迭代差分约束，内容同交叉约束
    def iterationConstraintsByCopy(self, variable1, variable2):
        """
        Generate the constraints by copy operation.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 16):     #分支长度 即1/2分组长度
            temp = []
            temp.append(variable1[i])
            temp.append(variable2[i])
            s = " - ".join(temp)
            s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()
    '''

    def Constraint(self):
        """
        Generate the constraints used in the MILP model.
        """
        assert (self.Round >= 1)
        fileobj = open(self.filename_model, "a")
        fileobj.write("Subject To\n")
        fileobj.close()
        variableleftin = SLIM.CreateLeftVariables(0)
        variablerightin = SLIM.CreateRightVariables(0)
        variablesboxout = SLIM.CreateSboxVariables(0)
        # variablepout = SLIM.CreatePVariables(0)
        variableleftout = SLIM.CreateLeftOutVariables(0)
        if self.Round == 1:
            self.ConstraintsBySbox(variablerightin, variablesboxout)
        # omit the last linear layer
        else:
            self.ConstraintsBySbox(variablerightin, variablesboxout)
            for i in range(1, self.Round):
                variablesboxout = self.LinearLaryer(variablesboxout)   ###
                self.ConstraintsByXor(variableleftin, variablesboxout, variableleftout)###通过###这两句完成了p置换，无需写入.lp文件，或者说，他们在刻画异或的不等式中已经体现好了
                variableleftin = SLIM.CreateLeftVariables(i)
                self.ConstraintsByCopy(variablerightin, variableleftin)   #feistel交叉操作差分约束
                variablerightin = SLIM.CreateRightVariables(i)
                variablesboxout = SLIM.CreateSboxVariables(i)
                # variablepout = SLIM.CreatePVariables(i)
                self.ConstraintsByCopy(variableleftout, variablerightin)
                variableleftout = SLIM.CreateLeftOutVariables(i)
                self.ConstraintsBySbox(variablerightin, variablesboxout)
            # omit the last linear layer
        '''
        #迭代差分约束
        variablesboxout = self.LinearLaryer(variablesboxout)
        self.ConstraintsByXor(variableleftin, variablesboxout, variableleftout)
        variableleftin0 = SLIM.CreateLeftVariables(0)
        self.iterationConstraintsByCopy(variablerightin, variableleftin0)
        variablerightin0 = SLIM.CreateRightVariables(0)
        self.iterationConstraintsByCopy(variableleftout, variablerightin0)
        '''

        #IDA差分约束
        variablesboxout = self.LinearLaryer(variablesboxout)
        self.ConstraintsByXor(variableleftin, variablesboxout, variableleftout)

        
        variablein0nn = SLIM.CreateIDAInputVariables(self.number)#生成输入差分值
        variableleftin0 = SLIM.CreateLeftVariables(0)#生成输入差分变量，左支
        variablerightin0 = SLIM.CreateRightVariables(0)#生成输入差分变量，右支
        self.IDAConstraintsByCopyLeft(variablein0nn, variableleftin0)#等式约束，左支
        self.IDAConstraintsByCopyRight(variablein0nn, variablerightin0)

        variableoutNnn = SLIM.CreateIDAOutputVariables(self.number)#生成输出差分值

        self.IDAConstraintsByCopyLeft(variableoutNnn, variablerightin)
        self.IDAConstraintsByCopyRight(variableoutNnn, variableleftout)

        self.variablein0 = variablein0nn#记录，打印输出
        self.variableoutN = variableoutNnn#记录，打印输出
        

    def VariableBinary(self):
        """
        Specify the variable type.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Binary\n")
        for i in range(0, (self.Round + 1)):
            for j in range(0, 64):
                fileobj.write("x_" + str(i) + "_" + str(j))
                fileobj.write("\n")
        for i in range(0, self.Globaly):
            fileobj.write('y' + str(i) + '\n')
        for i in range(0, self.dnum):
            fileobj.write('d_' + str(i) + '\n')
        fileobj.write("END")
        fileobj.close()

    def Init(self):
        """
        Generate the constraints introduced by the initial active sbox.   ###？？？   非0输入？
        """
        fileobj = open(self.filename_model, "a")
        Init_str = ' + '.join('x_0_' + str(i) for i in range(0, 32)) + ' >= 1' #x_0_0 + x_0_1 + ... + x_0_30 + x_0_31 >= 1   语法留意学习
        fileobj.write(Init_str + '\n')
        fileobj.close()

    def MakeModel(self):
        """
        Generate the MILP model of Present given the round number and activebits.
        """
        self.CreateObjectiveFunction()
        self.Constraint()
        self.Init()
        self.VariableBinary()

    def WriteObjective(self, obj):
        """
        Write the objective value into filename_result.
        """
        fileobj = open(self.filename_result, "a")
        fileobj.write("The objective value = %d\n" % obj.getValue())
        eqn1 = []
        eqn2 = []
        for i in range(0, self.blocksize):
            u = obj.getVar(i)
            if u.getAttr("x") != 0:
                eqn1.append(u.getAttr('VarName'))
                eqn2.append(u.getAttr('x'))
        length = len(eqn1)
        for i in range(0, length):
            s = eqn1[i] + "=" + str(eqn2[i])
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()

    def SolveModel(self):
        """
        Solve the MILP model to search the diffenertial distinguisher of SLIM.
        """
        time_start = time.time()
        m = read(self.filename_model)
        m.optimize()
        self.number += 1
        self.filename_model = "SLIM_" + str(self.Round) +"_" + str(self.number) + ".lp"
        
        self.Globaly = 0   #S盒标识位，表示S盒是否活跃   ？
        self.dnum = 0     #异或标识位，表示S盒是否活跃


        # 输出求解结果
        if m.status == gurobipy.GRB.INFEASIBLE:   # print("The problem has no feasible solution.*************************")
          
            '''
            #检测当前round是否存在不可能差分特征
            print(self.variablein0,"-->",self.variableoutN)
                       
            self.my_var = False
            '''
            
            #输出当前round下所有不可能差分特征
            # fileobj = open(self.filename_result, "a")
            # for i in range(0, 32):
            #     fileobj.write(self.variablein0(i))
            # fileobj.write( "-->")
            # for i in range(0, 32):
            #     fileobj.write(self.variableoutN(i))
            # fileobj.write("\n")
            # # print(self.variablein0,"-->",self.variableoutN)
            # fileobj.close()

            # fileobj = open(self.filename_result, "a")
            # print(self.variablein0,"-->",self.variableoutN,file=self.filename_result)
            # fileobj.close()
            with open(self.filename_result, "a") as f:                
                for item in self.variablein0:
                    f.write(item)
                f.write("-->")
                for item in self.variableoutN:
                    f.write(item)
                f.write("\n")
                


       
        
        '''
        else:            
            print("The optimal solution is ...")
        
            fileobj = open(self.filename_result, "a")
            if m.Status == 2:
                print("feasible")
                for i in range(0, self.Round + 1):
                    for j in range(0, 64):
                        a = m.getVarByName('x_' + str(i) + "_" + str(j))
                        fileobj.write('x_' + str(i) + "_" + str(j) + ": " + str(a.getAttr("x")))
                        fileobj.write("\n")
                for i in range(0, self.Globaly):
                    a = m.getVarByName('y' + str(i))
                    fileobj.write('y' + str(i) + ": " + str(a.getAttr("x")))
                    fileobj.write("\n")
            print(m.getObjective().getValue())
            time_end = time.time()
            print(("Time used = " + str(time_end - time_start)))
            fileobj.close()
        '''





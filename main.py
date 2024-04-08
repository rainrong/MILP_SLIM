# Algorithm 3 presented in paper "Applyint MILP Method to Searching Integral 
# Distinguishers based on Division Property for 6 Lightweight Block Ciphers"
# Regarding to the paper, please refer to https://eprint.iacr.org/2016/857
# For more information, feedback or questions, pleast contact at xiangzejun@iie.ac.cn

# Implemented by Xiang Zejun, State Key Laboratory of Information Security, 
# Institute Of Information Engineering, CAS

from SLIM import SLIM

if __name__ == "__main__":

	ROUND = int(input("Input the target round number: "))
	while not (ROUND > 0):
		print("Input a round number greater than 0.")
		ROUND = int(input("Input the target round number again: "))

	
	SLIM = SLIM(ROUND)

	# SLIM.MakeModel()

	# SLIM.SolveModel()

	'''
	#检测当前round是否存在不可能差分特征
	my_var = True  # 或者 False
	
	while SLIM.my_var == True|SLIM.number != 14400:

		SLIM.MakeModel()

		SLIM.SolveModel()
		# SLIM.number += 1

		# if SLIM.my_var == False | SLIM.number == 14400:
		# 	break
	print(SLIM.number)	
	'''

	#输出当前round下所有不可能差分特征
	# f1 = open(r"E:\作业\作业\20211228\SLIM\SLIM差分\SLIM - 副本\result_8_IDC","a+")
	
	while SLIM.number != 14400:

		SLIM.MakeModel()

		SLIM.SolveModel()

	

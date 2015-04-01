# -*- coding: gb2312 -*-
import _csv
import sys
import codecs
reload(sys)                      
sys.setdefaultencoding('utf-8')   
from  fp_growth import find_frequent_itemsets #导入fp_growth这个算法包里的函数发现频繁项

def state_change(bill_one,bill_two):
	negative_chinese = '\xe5\x90\xa6' #中文'否'的另外一种编码描述
	postive_chinese = '\xe6\x98\xaf'  #中文‘是’的另外一种编码描述
	state_change_value = -1 
	if bill_one == negative_chinese and bill_two == negative_chinese: #如果一月是否出账三无 为'否'，二月是否出账三无为’否‘
		state_change_value = 0			#则数值为0
	elif bill_one == negative_chinese and bill_two == postive_chinese: #如果一月是否出账三无 为'否'，二月是否出账三无为’是‘
		state_change_value = 1			#则数值为1
	elif bill_one == postive_chinese and bill_two == negative_chinese:
		state_change_value = 2
	elif bill_one == postive_chinese and bill_two == postive_chinese:
		state_change_value = 3
	return state_change_value
def billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six): #根据状态变化函数state_change 来对六个月的状态变化形成一个数据 譬如'00003'
	billvalue = str(state_change(bill_one,bill_two))+str(state_change(bill_two,bill_three))+str(state_change(bill_three,bill_four))+str(state_change(bill_four,bill_five))+str(state_change(bill_five,bill_six))
	# print  'billvalue'
	# print billvalue
	return billvalue   
def billvalue_make1(bill_one,bill_two,bill_three,bill_four): #只看三个月变化的情况
   billvalue = str(state_change(bill_one,bill_two))+str(state_change(bill_two,bill_three))+str(state_change(bill_three,bill_four))
   return billvalue

def target_change(target_one,target_two): #目标状态变化函数,生成数据譬如'01233'
	if target_one == '0' and target_two == '0':  #如果一月目标0，二月目标0，
		targetvalue = 0				#则这两个月之间目标变化的数值为0
	elif  target_one == '0' and target_two == '1':
		targetvalue = 1
	elif  target_one == '0' and target_two == '2':
		targetvalue = 2
	elif  target_one == '1' and target_two == '0':
		targetvalue = 3
	elif  target_one == '1' and target_two == '1':
		targetvalue = 4
 	elif  target_one == '1' and target_two == '2':
		targetvalue = 5
	elif  target_one == '2' and target_two == '0':
		targetvalue = 6
	elif  target_one == '2' and target_two == '1':
		targetvalue = 7
	elif  target_one == '2' and target_two == '2':
		targetvalue = 8
	return targetvalue
	# pass 
def targetvalue_make(target_one,target_two,target_three,target_four,target_five,target_six): 
	targetvalue = str(target_change(target_one,target_two)) + str(target_change(target_two,target_three))+ str(target_change(target_three,target_four))+ str(target_change(target_four,target_five))+str(target_change(target_five,target_six)) 
	# print 'targetvalue'
	# print targetvalue
	return targetvalue
def targetvalue_make1(target_one,target_two,target_three,target_four):
    targetvalue = str(target_change(target_one,target_two)) + str(target_change(target_two,target_three))+ str(target_change(target_three,target_four))
    return targetvalue

def csv_read():  #核心的函数，
	with open('E:/yk/test/my/yk--my.csv', 'rb') as csvfile: #读取csv 文件.
		csvreader = _csv.reader(csvfile, delimiter=' ', quotechar='|')
		negative_chinese = '\xe5\x90\xa6'
		postive_chinese = '\xe6\x98\xaf'
		billvalue = ''
		targetvalue = ''#初始化为空字符.
		index_number = 0 
		yangka_data = [['0' for i in range(0,2)] for j in range(0,90000)]
		fpgrowth_yangka = codecs.open("E:/yk/test/my/yangka.txt","w")  #定义要把发现出来的数据写入的文件. 其中w代表写.

		for row in csvreader:
			element = str(', '.join(row)) 
			_element = str(', '.join(row).decode("gb2312") )  # 每条_element 的例子为   ”否,否,否,否,否,否,1,0,0,1,2,2“
			#bill_one,bill_two,bill_three ...分别表示一月，二月，三月...是否出账三无的数值为'否'还是'是'
			bill_one = _element.split(',')[0] #对_element 以','进行分割 ”否,否,否,否,否,否,1,0,0,1,2,2“分割得到的第一项为'否'
			bill_two =  _element.split(',')[1]
			bill_three =  _element.split(',')[2]
			bill_four =  _element.split(',')[3]
			bill_five =  _element.split(',')[4]
			bill_six =  _element.split(',')[5]	
			#target_one,target_two,target_three... 分别表示一月，二月，三月....养卡是'0'还是'1'还是'2'
			target_one = _element.split(',')[6]
			target_two = _element.split(',')[7]
			target_three =_element.split(',')[8]
			target_four = _element.split(',')[9]
			target_five = _element.split(',')[10]
			target_six = _element.split(',')[11]

			print _element
			#根据上面得到的每个月的状态（是否出账三无），目标生成一个状态变化的数值  和目标变化的数值
			# billvalue =  billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six)
			# targetvalue = targetvalue_make(target_one,target_two,target_three,target_four,target_five,target_six)
			billvalue=billvalue_make1(bill_one,bill_two,bill_three,bill_four)
			targetvalue=targetvalue_make1(target_one,target_two,target_three,target_four)
			# 生成数值之后赋值给yangka_data这个数组，列1为是否出账生成这个的状态变化#的数据，列2为目标变化生成的数据. index_number每次加1 作为一个浮标
			yangka_data[index_number][0] = billvalue
			yangka_data[index_number][1] = targetvalue
			index_jnumber = index_number + 1
		# print yankga_data
		# 这是核心部分，需要在运行这个程序之前安装fp_growth这个频繁项挖掘的算法包，其返回的itemset 就是挖掘处来的每个数组集如‘['00000', '30288'] ’，support 为出现次数‘2782’,它们共同组成生成到文件里的记录‘['00000', '30288'] 2782’，下面的数字500 是挖掘出来的记录出现的最低次数，比如像'‘['00000', '30288'] ’这种状态如果出现次数低于500 就不考虑，超过500 就考虑，在这里它出现了'2782'次，所以就会考虑了.
		for (itemset,support) in find_frequent_itemsets(yangka_data,500,True):
			print>>fpgrowth_yangka,itemset,support #把这些挖掘得到的记录 生成到文件yangka.txt里.
# 
			# break		 	
# read_fpgrowth_yangka 的功能是清理最开始生成的文件，去除'['30028'] 4428' 这类格式的记录.
def read_fpgrowth_yangka():
	file = 'E:/yk/test/my/yangka.txt'
	fpgrowth_yangka = codecs.open("E:/yk/test/my/yangka_new.txt","w")
	fp_data = open(file)
	for data in fp_data:
		if len(str(data.split(']')[0])) > 8:
			print>>fpgrowth_yangka,data.replace('\n', ' ').replace('\r', '')
# csv_read() # 去掉前面的'#'注释符就可以执行这个函数,进行频繁项发现.
read_fpgrowth_yangka() #清理文件yangka.txt


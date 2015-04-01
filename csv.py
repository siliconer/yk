# -*- coding: gb2312 -*-
import _csv
import sys
import codecs
reload(sys)                      
sys.setdefaultencoding('utf-8')   
from  fp_growth import find_frequent_itemsets #����fp_growth����㷨����ĺ�������Ƶ����

def state_change(bill_one,bill_two):
	negative_chinese = '\xe5\x90\xa6' #����'��'������һ�ֱ�������
	postive_chinese = '\xe6\x98\xaf'  #���ġ��ǡ�������һ�ֱ�������
	state_change_value = -1 
	if bill_one == negative_chinese and bill_two == negative_chinese: #���һ���Ƿ�������� Ϊ'��'�������Ƿ��������Ϊ����
		state_change_value = 0			#����ֵΪ0
	elif bill_one == negative_chinese and bill_two == postive_chinese: #���һ���Ƿ�������� Ϊ'��'�������Ƿ��������Ϊ���ǡ�
		state_change_value = 1			#����ֵΪ1
	elif bill_one == postive_chinese and bill_two == negative_chinese:
		state_change_value = 2
	elif bill_one == postive_chinese and bill_two == postive_chinese:
		state_change_value = 3
	return state_change_value
def billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six): #����״̬�仯����state_change ���������µ�״̬�仯�γ�һ������ Ʃ��'00003'
	billvalue = str(state_change(bill_one,bill_two))+str(state_change(bill_two,bill_three))+str(state_change(bill_three,bill_four))+str(state_change(bill_four,bill_five))+str(state_change(bill_five,bill_six))
	# print  'billvalue'
	# print billvalue
	return billvalue   
def billvalue_make1(bill_one,bill_two,bill_three,bill_four): #ֻ�������±仯�����
   billvalue = str(state_change(bill_one,bill_two))+str(state_change(bill_two,bill_three))+str(state_change(bill_three,bill_four))
   return billvalue

def target_change(target_one,target_two): #Ŀ��״̬�仯����,��������Ʃ��'01233'
	if target_one == '0' and target_two == '0':  #���һ��Ŀ��0������Ŀ��0��
		targetvalue = 0				#����������֮��Ŀ��仯����ֵΪ0
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

def csv_read():  #���ĵĺ�����
	with open('E:/yk/test/my/yk--my.csv', 'rb') as csvfile: #��ȡcsv �ļ�.
		csvreader = _csv.reader(csvfile, delimiter=' ', quotechar='|')
		negative_chinese = '\xe5\x90\xa6'
		postive_chinese = '\xe6\x98\xaf'
		billvalue = ''
		targetvalue = ''#��ʼ��Ϊ���ַ�.
		index_number = 0 
		yangka_data = [['0' for i in range(0,2)] for j in range(0,90000)]
		fpgrowth_yangka = codecs.open("E:/yk/test/my/yangka.txt","w")  #����Ҫ�ѷ��ֳ���������д����ļ�. ����w����д.

		for row in csvreader:
			element = str(', '.join(row)) 
			_element = str(', '.join(row).decode("gb2312") )  # ÿ��_element ������Ϊ   ����,��,��,��,��,��,1,0,0,1,2,2��
			#bill_one,bill_two,bill_three ...�ֱ��ʾһ�£����£�����...�Ƿ�������޵���ֵΪ'��'����'��'
			bill_one = _element.split(',')[0] #��_element ��','���зָ� ����,��,��,��,��,��,1,0,0,1,2,2���ָ�õ��ĵ�һ��Ϊ'��'
			bill_two =  _element.split(',')[1]
			bill_three =  _element.split(',')[2]
			bill_four =  _element.split(',')[3]
			bill_five =  _element.split(',')[4]
			bill_six =  _element.split(',')[5]	
			#target_one,target_two,target_three... �ֱ��ʾһ�£����£�����....������'0'����'1'����'2'
			target_one = _element.split(',')[6]
			target_two = _element.split(',')[7]
			target_three =_element.split(',')[8]
			target_four = _element.split(',')[9]
			target_five = _element.split(',')[10]
			target_six = _element.split(',')[11]

			print _element
			#��������õ���ÿ���µ�״̬���Ƿ�������ޣ���Ŀ������һ��״̬�仯����ֵ  ��Ŀ��仯����ֵ
			# billvalue =  billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six)
			# targetvalue = targetvalue_make(target_one,target_two,target_three,target_four,target_five,target_six)
			billvalue=billvalue_make1(bill_one,bill_two,bill_three,bill_four)
			targetvalue=targetvalue_make1(target_one,target_two,target_three,target_four)
			# ������ֵ֮��ֵ��yangka_data������飬��1Ϊ�Ƿ�������������״̬�仯#�����ݣ���2ΪĿ��仯���ɵ�����. index_numberÿ�μ�1 ��Ϊһ������
			yangka_data[index_number][0] = billvalue
			yangka_data[index_number][1] = targetvalue
			index_jnumber = index_number + 1
		# print yankga_data
		# ���Ǻ��Ĳ��֣���Ҫ�������������֮ǰ��װfp_growth���Ƶ�����ھ���㷨�����䷵�ص�itemset �����ھ�����ÿ�����鼯�确['00000', '30288'] ����support Ϊ���ִ�����2782��,���ǹ�ͬ������ɵ��ļ���ļ�¼��['00000', '30288'] 2782�������������500 ���ھ�����ļ�¼���ֵ���ʹ�����������'��['00000', '30288'] ������״̬������ִ�������500 �Ͳ����ǣ�����500 �Ϳ��ǣ���������������'2782'�Σ����Ծͻῼ����.
		for (itemset,support) in find_frequent_itemsets(yangka_data,500,True):
			print>>fpgrowth_yangka,itemset,support #����Щ�ھ�õ��ļ�¼ ���ɵ��ļ�yangka.txt��.
# 
			# break		 	
# read_fpgrowth_yangka �Ĺ����������ʼ���ɵ��ļ���ȥ��'['30028'] 4428' �����ʽ�ļ�¼.
def read_fpgrowth_yangka():
	file = 'E:/yk/test/my/yangka.txt'
	fpgrowth_yangka = codecs.open("E:/yk/test/my/yangka_new.txt","w")
	fp_data = open(file)
	for data in fp_data:
		if len(str(data.split(']')[0])) > 8:
			print>>fpgrowth_yangka,data.replace('\n', ' ').replace('\r', '')
# csv_read() # ȥ��ǰ���'#'ע�ͷ��Ϳ���ִ���������,����Ƶ�����.
read_fpgrowth_yangka() #�����ļ�yangka.txt


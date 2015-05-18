# -*- coding: gb2312 -*-
import _csv
import sys
import codecs
import os 
import operator
reload(sys)                      
sys.setdefaultencoding('utf-8')   
from  fp_growth import find_frequent_itemsets
def convert_state_value(bill):
	negative_chinese = '\xe5\x90\xa6' 
	postive_chinese = '\xe6\x98\xaf'  
	convert_state_value = 'U'
	if bill == negative_chinese:
		convert_state_value = 'Y'
	if bill == postive_chinese:
		convert_state_value = 'N' 
	return convert_state_value 

def state_change(bill_one,bill_two):
	negative_chinese = '\xe5\x90\xa6' 
	postive_chinese = '\xe6\x98\xaf'  
	state_change_value = -1 
	if bill_one == negative_chinese and bill_two == negative_chinese: 
		state_change_value = 0			
	elif bill_one == negative_chinese and bill_two == postive_chinese: 
		state_change_value = 1			
	elif bill_one == postive_chinese and bill_two == negative_chinese:
		state_change_value = 2
	elif bill_one == postive_chinese and bill_two == postive_chinese:
		state_change_value = 3
	return state_change_value
def billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six): 
	billvalue = str(state_change(bill_one,bill_two))+str(state_change(bill_two,bill_three))+str(state_change(bill_three,bill_four))+str(state_change(bill_four,bill_five))+str(state_change(bill_five,bill_six))
	# print  'billvalue'
	# print billvalue
	return billvalue   


def target_change(target_one,target_two): 
	if target_one == '0' and target_two == '0':  
		targetvalue = 0				
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

def billvalue_make1(bill_one,bill_two,bill_three,bill_four): 
   billvalue = 'B'+str(convert_state_value(bill_one))+str(convert_state_value(bill_two))+str(convert_state_value(bill_three))+str(convert_state_value(bill_four))
   return billvalue
def targetvalue_make1(target_one,target_two,target_three,target_four):
    # targetvalue = 'T'+str(target_change(target_one,target_two)) + str(target_change(target_two,target_three))+ str(target_change(target_three,target_four))
    targetvalue = 'T'+str(target_one)+str(target_two)+str(target_three)+str(target_four)
    return targetvalue

def csv_read():  
	current_dir = os.getcwd()
	counter  = 0
	csv_file = current_dir + '/my/yk--my.csv'
	counter = 0
	yangka_txt = current_dir + '/yangka.txt'
	file_yangka = codecs.open(yangka_txt,"w")  

	with open(csv_file, 'rb') as csvfile: 
		csvreader = _csv.reader(csvfile, delimiter=' ', quotechar='|')
		negative_chinese = '\xe5\x90\xa6'
		postive_chinese = '\xe6\x98\xaf'
		billvalue = ''
		targetvalue = ''
		index_number = 0 
		yangka_data = [['0' for i in range(0,2)] for j in range(0,90000)]

		for row in csvreader:
			element = str(', '.join(row)) 
			_element = str(', '.join(row).decode("gb2312") )  
			
			bill_one = _element.split(',')[0] 
			bill_two =  _element.split(',')[1]
			bill_three =  _element.split(',')[2]
			bill_four =  _element.split(',')[3]
			bill_five =  _element.split(',')[4]
			bill_six =  _element.split(',')[5]	
			target_one = _element.split(',')[6]
			target_two = _element.split(',')[7]
			target_three =_element.split(',')[8]
			target_four = _element.split(',')[9]
			target_five = _element.split(',')[10]
			target_six = _element.split(',')[11]

			print _element
			# billvalue =  billvalue_make(bill_one,bill_two,bill_three,bill_four,bill_five,bill_six)
			# targetvalue = targetvalue_make(target_one,target_two,target_three,target_four,target_five,target_six)
			billvalue=billvalue_make1(bill_one,bill_two,bill_three,bill_four)
			targetvalue=targetvalue_make1(target_one,target_two,target_three,target_four)
			yangka_data[index_number][0] = billvalue
			yangka_data[index_number][1] =  targetvalue
			index_number = index_number + 1

		for (itemset,support) in find_frequent_itemsets(yangka_data,100,True):
			print>>file_yangka,itemset,support 

		#temp_arrya :temporary array  && used for reading the initial data generating from fp_growth ,then adjust the data sequence 
		# example :[T1001,'BYYYY'] 528 ->['BYYYY', 'T1001'] 528 
		temp_array = [ '0' for i in range(0,10000)] 
		temp_array_indexer = 0
		file_data = open(yangka_txt)
		for data in file_data:
			print 'data '+ str(data.replace('\n', ' ').replace('\r', ''))
			if len(str(data.split(']')[0])) > 8:
				# adjust_write_sequence : [T1001,'BYYYY'] 528 ->['BYYYY', 'T1001'] 528 
				# .replace('\n', ' ').replace('\r', '')  ->get rid of the '\n' in the end of  each line of yangka.txt	
				temp_array[temp_array_indexer] = adjust_write_sequence(data).replace('\n', ' ').replace('\r', '')
				temp_array_indexer = temp_array_indexer + 1 
				counter = counter +  1 

		#read data from temp_array , sort them and write into yangka_sort.txt
		yanka_sort_file = current_dir + '/yangka_sort.txt'
		yangka_sort  = codecs.open(yanka_sort_file,"w")
		yangka_data_mining= [['0' for i in range(0,2)] for j in range(0,counter)]
		index_counter = 0 
		for m  in range(0,len(temp_array)):
			data = str(temp_array[m])  # read data from temp_array 
			if data!= '0':
				yangka_data_mining[index_counter][0] = data.split(']')[0]+']'  # pattern, such as '[T1001,'BYYYY']' 
 				yangka_data_mining[index_counter][1] = int(data.split(']')[1]) # the occuring time of pattern ,such as '528' 
				index_counter = index_counter + 1 
		yangka_data_mining.sort(key=operator.itemgetter(1), reverse=True)  # sort them.
		for yangka_data in yangka_data_mining:
			yangka_data[1] = str(yangka_data[1])
		for data in yangka_data_mining:
			print>>yangka_sort,data  # write into file  yangka_sort.txt

def adjust_write_sequence(data):
	return_data = data
	B_start_loc = data.find('B')  # find return location, if not return -1 .
	T_start_loc = data.find('T')
	#data example :['BYYYY', 'T0200'] 159
	if B_start_loc!= -1 and T_start_loc !=-1:
		if B_start_loc > T_start_loc: # T frist show, B then shows.
			return_data = data[0:T_start_loc]+ data[B_start_loc:B_start_loc+5] + data[T_start_loc+5:B_start_loc]+ data[T_start_loc:T_start_loc+5]+data[B_start_loc+5:]
	return return_data

csv_read() 


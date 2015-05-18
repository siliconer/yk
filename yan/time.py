# -*- coding: utf-8 -*-
import _csv
import sys
import codecs
import os 
import operator
import csv

from  fp_growth import find_frequent_itemsets
def csv_read():
	current_dir = os.getcwd()
	counter  = 0
	csv_file = current_dir + '/stop201505.csv'
	index = 0 
	with open(csv_file, 'rb') as csvfile: 
		csvreader = _csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in csvreader:
			if row[0] == '"SERIAL_NUMBER","EXEC_TIME","TRADE_TYPE_CODE"' :
				continue
			index = index + 1 
		single_round_number = 500000
		read_start = 0 
		while(index>0):
			single_csv_read(read_start,csv_file,single_round_number)
			print 'next round coming'
			read_start = read_start + single_round_number
			if (index > single_round_number):
				index = index - single_round_number
			else:
				single_csv_read(read_start,csv_file,single_round_number)
				index = -1 


def single_csv_read(read_start,csv_file,single_round_number):  
	print 'begining new round'
	data  = [['0' for i in range(0,4)] for j in range(0,single_round_number)]  
	index = 0 
	temp_index = 0 
	with open(csv_file, 'rb') as csvfile: 
		csvreader = _csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in csvreader:
			if row[0] == '"SERIAL_NUMBER","EXEC_TIME","TRADE_TYPE_CODE"' :
				continue
			temp_index = temp_index + 1
			if temp_index < read_start:
				continue
			if temp_index > read_start  + single_round_number:
				break 
			#data[][0]  user_id,day,hour,type
			type = row[2][3:-1]
			if index < single_round_number:
				data[index][0] = str(row[0].split(',')[0][1:-1])    #UserId
				data[index][1] = str(row[0].split(',')[1][1:])  # 2015-02-26  Day
				data[index][2] = row[1]	# '11:16:03' hour 
				data[index][3] = row[2][3:-1] # 7220 type 
				index = index + 1 
	sum_gap(data,single_round_number)
		

	

#7210,7101  Half stop
# 7110,7220  Stop
# 7303,7302,7301 Start 


def sum_gap(data,single_round_number):
	gap_data = {}
	month_stop = {}
	half_stop = {}
	for index in range(0,single_round_number):
		gap_data[data[index][0]]=[]
		month_stop[data[index][0]]= {}
		month_stop[data[index][0]]['11']= 0
		month_stop[data[index][0]]['12']= 0
		month_stop[data[index][0]]['1']= 0
		month_stop[data[index][0]]['2']= 0
		month_stop[data[index][0]]['3'] = 0
		month_stop[data[index][0]]['4']	= 0

		half_stop[data[index][0]]={}
		half_stop[data[index][0]]['half_stop'] = 0  # havn't met half_stop
		half_stop[data[index][0]]['day'] = '0'  # first half_stop time 
		half_stop[data[index][0]]['hour'] = '0'  # first half_stop time 

	stop_stop = 0 
	stop_start = 0
	stop_half_stop = 0 
	half_stop_start = 0 
	half_stop_stop = 0 
	half_stop_half =  0 
	gap_day = 0 
	index = 0 
	# prev_index = 0  
	while(index<single_round_number-100):				
		if data[index][3] == '7210' or data[index][3] == '7101':  #half_stop
			if half_stop[data[index][0]]['half_stop']  == 0:
				half_stop[data[index][0]]['half_stop'] = 1 
				half_stop[data[index][0]]['day'] = data[index][1]
				half_stop[data[index][0]]['hour'] = data[index][2]

		if data[index][3]== '7303' or data[index][3]== '7302' or data[index][3]== '7301' or data[index][3]=='530': # start 
			if 	half_stop[data[index][0]]['half_stop'] == 1:
				half_stop_day = half_stop[data[index][0]]['day']
				half_stop_hour = half_stop[data[index][0]]['hour']
				gap_day = calc_day(half_stop_day,half_stop_hour,data[index][1],data[index][2])
				gap_data[data[index][0]].append(gap_day)
				month = int(half_stop_day[5:7])
				# print 'month '+str(month)
				month_stop[data[index][0]][str(month)]=month_stop[data[index][0]][str(month)] + 1 
				half_stop[data[index][0]]['half_stop'] = 0
		index = index + 1
	write_to_file(gap_data,month_stop)
	print 'finish this round'

def write_to_file(gap_data,month_stop):
	current_dir = os.getcwd()
	# gap_file= current_dir + '/gap_data.txt'
	# gap_file_data = codecs.open(gap_file,"w")  

	csvfile = current_dir + '/gap_data_4g.csv'
	with open(csvfile,"a") as output:
		writer = csv.writer(output,lineterminator='\n')
		writer.writerow(["SERIAL_NUMBER","6","5","4","3","2","1","AVG_STOP","OFFINTERVAL","MAX_INT","MIN_INT",'AVG_INT','VAR'])

		for x in gap_data.keys():	
			temp = sorted(gap_data[x])
			item_counter = 0
			sum = 0
			sum1 =0
			for item in temp:
				item_counter = item_counter + 1
				sum = item + sum
				sum1 += item**2

			#calc_stop_by_month part 
			month_counter = 0 
			month_sum = 0 
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'11',month_counter,month_sum)
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'12',month_counter,month_sum)
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'1',month_counter,month_sum)
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'2',month_counter,month_sum)
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'3',month_counter,month_sum)
			month_counter,month_sum = calc_stop_by_month(month_stop[x],'4',month_counter,month_sum)

			if gap_data[x] and len(gap_data[x]) <= 50 :
				averate_time = "%.1f" %(float(sum)/item_counter)
				var= "%.1f" %(float(sum1)/item_counter-float(float(sum)/item_counter)**2)
				stop_by_month = "%.1f" %(float(month_sum)/month_counter)
				writer.writerow([str(x),month_stop[x]['11'],month_stop[x]['12'],month_stop[x]['1'],month_stop[x]['2'],month_stop[x]['3'],month_stop[x]['4'],stop_by_month,gap_data[x],temp[0],temp[-1],averate_time,var])


def calc_stop_by_month(each_user_data,key,month_counter,month_sum):	
	if each_user_data[key] !=0 :
		month_counter = month_counter + 1 
		month_sum = month_sum + each_user_data[key]
	return month_counter,month_sum

def calc_day(day,hour,next_day,next_hour):
	# '11:16:03'
	# 2015-02-27
	days_month = 30 
	if int(next_day[0:4]) == int(day[0:4]) :
		gap_day = (int(next_day[5:7]) - int(day[5:7]))*days_month  +  (int(next_day[8:10]) - int(day[8:10]))
		# print 'gap_day '+str(gap_day)

		hour = int(hour[0:2])
		next_hour = int(next_hour[0:2])

		if next_hour - hour > 12:
			gap_day = gap_day + 1
	elif int(next_day[0:4]) - int(day[0:4]) == 1:
		gap_day = (12-int(day[5:7]))*30+(30-int(day[8:10]))+(int(next_day[5:7])-1)*30 + int(next_day[8:10])
	return gap_day

def sum_gap_calc_number(data):
	gap_data = {}
	for index in range(0,6665000):
		gap_data[data[index][0]]=[]
	stop_stop = 0 
	stop_start = 0
	stop_half_stop = 0 
	half_stop_start = 0 
	half_stop_stop = 0 
	half_stop_half =  0 
	gap_day = 0 
	index = 0 
	# prev_index = 0  
	while(index<6664998):
		next_index = index+ 1 
		if data[index][0] == data[next_index][0]:     
			if data[index][3] == '7110' or data[index][3] == '7220':  #stop 
				if data[next_index][3]== '7303' or data[next_index][3]== '7302' or data[next_index][3]== '7301' or data[next_index][3]=='530': # start 
					print 'time '+data[index][0]+' '+data[index][1]+' '+data[index][3]+' '+data[next_index][1]+' '+data[next_index][3]
					gap_day = calc_day(data[index][1],data[index][2],data[next_index][1],data[next_index][2])
					# if data[prev_index][0] == data[index][0]:
					gap_data[data[index][0]].append(gap_day)
					# prev_index = index
					index = index +  2 
					stop_start = stop_start + 1 

				else:
					if data[next_index][3] == '7110' or data[next_index][3] == '7220': # stop 
						# print 'stop stop ' +str(index)
						stop_stop = stop_stop + 1
						index = index + 1 
					if data[next_index][3] == '7210' or data[next_index][3] == '7101': 
						stop_half_stop = stop_half_stop + 1
						index = index + 2 

			else:
				#half_stop start part 
				if data[index][3] == '7210' or data[index][3] == '7101':  #half_stop
					if data[next_index][3]== '7303' or data[next_index][3]== '7302' or data[next_index][3]== '7301' or data[next_index][3]=='530': # start 
						half_stop_start = half_stop_start + 1 
						# print 'half_stop start ' +str(data[index][0])
						index  = index + 2 
					if data[next_index][3] == '7110' or data[next_index][3] == '7220': # stop 
						half_stop_stop = half_stop_stop + 1 
						# print 'half_stop stop ' +str(data[index][0])
						index = index + 1 
					if data[next_index][3] == '7210' or data[next_index][3] == '7101':  #half_stop
						half_stop_half = half_stop_half  + 1 
						index= index + 2 
				else: #start 
					index = index + 1 
		else: # not the same ;the two row id
			index = index + 1 
	write_to_file(gap_data)
	print 'stop_stop '+str(stop_stop)
	print 'stop_start' +str(stop_start)
	print 'stop_half_stop '+str(stop_half_stop)
	print 'half_stop_start '+str(half_stop_start)
	print 'half_stop_stop '+str(half_stop_stop)
	print 'half_stop_half '+str(half_stop_half)
# //2009051209032566

csv_read()

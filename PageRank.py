import csv
import time
import copy

alpha = 0.85 #the const alpha
iter_count = 1 #current iteration times
N = 55594 #sum of total persons
max_count = 100 #iteration times when the iteration ends

person_list = [] #persons list
person_adj_list = [] #adjacency list
rank_person = {} #nodes and their ranks 
reduce_person = {} #reduce process



'''
pre-process

#from calls data to the adjacency list
with open('calls_adj_list.csv','wb') as f1:
	writer = csv.writer(f1)
	with open('calls.csv') as f2:
		reader = csv.reader(f2)
		tmp_row = ['2457'] #the first person
		for row in reader:
			if row[0]==tmp_row[0]:
				tmp_row.append(row[1])
			else:
				writer.writerow(tmp_row)
				tmp_row = [row[0],row[1]]
f1.close()
f2.close()

#get all persons 
with open('person_list.csv','wb') as f1:
	writer = csv.writer(f1)
	with open('calls.csv') as f2:
		reader = csv.reader(f2)
		for row in reader :
			if row[0] not in person_list:
				person_list.append(row[0])
			if row[1] not in person_list:
				person_list.append(row[1])
	for row in person_list:
		writer.writerow([str(row)])


f1.close()
f2.close()
'''

#clear the last operation values 
def clear_rank(reduce_person):
	for key in reduce_person:
		reduce_person[key] = 0

#the mapping process 
def map_process(person_adj_list,rank_person,reduce_person):
	clear_rank(reduce_person)
	for row in person_adj_list:
		tmp_list = row[1:]
		count = len(tmp_list)
		for person in tmp_list:
			reduce_person[person] += rank_person[row[0]]/count #for each line add the contribution to the nodes (p1+p2+…Pm)

#the reducing process
def reduce_process(reduce_person,rank_person):
	for person in rank_person:
		rank_person[person] = alpha*reduce_person[person] + (1-alpha)/N #calculate the next value (pj=a*(p1+p2+…Pm)+(1-a)*1/n)

#calculate the loss
def loss_calcu(pre_rank,cur_rank):
	loss = 0
	for person in cur_rank:
		loss += abs(pre_rank[person]-cur_rank[person]) #add all losses
	return loss

#initialize person_list from the csv file
with open('person_list.csv') as f1:
	reader = csv.reader(f1)
	for person in reader:
		person_list.append(person)
f1.close()

#initialize person_adj_list from the csv file 
with open('calls_adj_list.csv') as f1:
	reader = csv.reader(f1)
	for row in reader:
		person_adj_list.append(row)
f1.close()

#initialize the dictionaries
for person in person_list:
	reduce_person[person[0]] = 0
	rank_person[person[0]] = 1/N 

start_time = time.time() #iteration start time
#algorithm main part
while iter_count < max_count:
    pre_rank = copy.deepcopy(rank_person)
    map_process(person_adj_list,rank_person,reduce_person)
    reduce_process(reduce_person,rank_person)
    loss = loss_calcu(pre_rank,rank_person)
    print('count : %d loss = %e' %(iter_count,loss))
    iter_count += 1
end_time = time.time()#iteration end time

#sort the final list
sorted_list = sorted(rank_person.items(),key = lambda x:x[1],reverse = True)

#output the final list
with open('Rank.csv','wb') as f1:
	writer = csv.writer(f1)
	for row in sorted_list:
		writer.writerow(row)
f1.close()

#print current loss
print("total time-cost : %fs"%(end_time-start_time))
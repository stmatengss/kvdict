#! /bin/env python
# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import json
import csv
import re
import time
import kvdict2 as kd2

argv = sys.argv[1:]

file_name = argv[0]
begin = int(argv[1])
end = int(argv[2])


# filter_word_file = file("filter_word") 
ticker_words = kd2.KVDict()
ticker_words.load('/home/mateng/dict/doudi_entity.dict')

filter_words = ['有限公司','有限责任公司']
fout = file('filter_match_ticker_res'+'_'+str(begin)+'_'+str(end)+'.csv', 'w')
csv_writer = csv.writer(fout)

def pending_num(term):
	return not term.replace('.', '').isdigit()	



for num in range(begin, end):
	print time.time()
	# name = 'small_case'
	name = file_name+str(num)+'.seg_res'
	# file_raw = file(name, 'r').readlines()
	file_raw = file(name, 'r').readlines()

	count = 0
	print num
	for content in file_raw:
		count = count+1

		# monitor
		if count%10000==0: 
			print count
			print time.time()	

		#content = content.split('\t')[1]
		content = content.split('\t')[1]

		# gain the doc's content.
		## TODO using forzenSet insteadof set
		doc_raw = json.loads(content)['add']['doc']
		title_raw = doc_raw['title'].encode('utf8')
		#print title_raw
		for i in xrange(4,21):
			title_slice = title_raw[:i]
			# print 'slice', title_slice
			if ticker_words.has(title_slice):
				#print 'catch', title_slice
				url = doc_raw['pdf_link']
				# there is a ticker_name in title
				csv_writer.writerow([title_slice, title_raw, url])

print 'end',time.time()
print 'ok',num		
fout.close()
		
		

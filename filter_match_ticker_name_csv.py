#! /bin/env python
# encoding=utf-8
# designed by stmatengss

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import json
import csv
import re
import time
import kvdict2 as kd2
import re
import logging
from logging import *
from csv import *

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                                       
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): 
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

argv = sys.argv[1:]

file_name_in = argv[0]
file_name_out = argv[1]


# filter_word_file = file("filter_word") 
ticker_words = kd2.KVDict()
ticker_words.load('/home/mateng/dict/doudi_entity.dict')

filter_words = [u'公司']
pass_words = [u'年公司']


print 'begin_time', time.time()
# name = 'small_case'
# file_raw = file(name, 'r').readlines()
fin = file(file_name_in, 'r')
fout = file(file_name_out, 'w')
csv_writer = csv.writer(fout)
data = csv.reader(fin)

count_terms_r1 = 0
count_terms_r2 = 0

for count_terms_sum, terms in enumerate (data):
	# monitor
	if count_terms_sum % 100000 == 0: 
		print count_terms_sum
		print time.time()	

	ticker_name_raw = terms[0]
	title_raw = strQ2B(unicode(terms[1]))
#	title_raw = strQ2B(terms[1])
	pdf_link_raw = terms[2]
	#print title_raw
	include_flag = True

	# case: title contains ticker_name
	if ticker_name_raw in title_raw:
		continue

	# case: title contains '年公司'
	if pass_words[0] in title_raw:
		continue

	# case : '公司' in the head of the title
	if title_raw[0:2] == filter_words[0]:
		continue 

	for i in xrange(4,21):
		title_slice = title_raw[:i]
		# print 'slice', title_slice
		if ticker_words.has(title_slice):
			#print 'catch', title_slice
			if title_slice != ticker_name_raw:
				# there is a ticker_name in title
				csv_writer.writerow([ticker_name_raw, '0', title_raw, pdf_link_raw])
				count_terms_r1 = count_terms_r1+1
				include_flag = False

	if include_flag :
		for filter_word in filter_words:
			if filter_word in title_raw:
				# there is a ticker_name in title
				csv_writer.writerow([ticker_name_raw, '1' , title_raw, pdf_link_raw])
				count_terms_r2 = count_terms_r2+1
			
print 'end',time.time()
print 'sum_terms_sum:',count_terms_sum		
print 'sum_terms_r1:',count_terms_r1	
print 'sum_terms_r2:',count_terms_r2	
fout.close()
		
		

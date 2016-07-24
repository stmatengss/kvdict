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

class filter_match_tool:
	def __init__(self, file_name_dict, file_name_equal_dict, file_name_instead_dict):
		"""load dict & initialize the constant"""
		
		self.ticker_instead_words = kd2.KVDict()
		self.ticker_instead_words.load(file_name_instead_dict)
		self.ticker_words = kd2.KVDict()
		self.ticker_words.load(file_name_dict)
		self.ticker_equal_words = kd2.KVDict()
		self.ticker_equal_words.load(file_name_equal_dict)
		
		"""'/home/mateng/dict/doudi_entity.dict'"""

		self.filter_words = [u'公司']
		self.pass_words = [u'年公司']
		print 'begin_time', time.time()

	def pending_legal(ticker_name, title):
		if u'事务年度报告' in title:
			return False
		if u'有限责任' in title or u'有限' in title:
			if u'股份有限' in title:
				return True
			return False
		return False

	def filter_error_pair(terms):

		ticker_name_raw = terms[0]
		title_raw = strQ2B(unicode(terms[1])).encode('utf-8')
		pdf_link_raw = terms[2]
		ticker_name_equal = ''
		ticker_name_instead = ''
		#print title_raw
		include_flag = True

		# case: deal with equal tickers
		if self.ticker_equal_words.has(ticker_name_raw):
			ticker_name_equal = self.ticker_equal_words.find(ticker_name_raw).encode('utf-8').strip()
		#	print ticker_name_equal
		
		if self.ticker_instead_words.has(ticker_name_raw):
			ticker_name_instead = self.ticker_instead_words.find(ticker_name_raw).encode('utf-8').strip()
			if ticker_name_instead in title_raw:
				True
		# case: title contains ticker_name
		if ticker_name_raw in title_raw:
			return True

		# case: title contains '年公司'
		if self.pass_words[0] in title_raw:
			return True

		# case : '公司' in the head of the title
		if title_raw[0:2] == self.filter_words[0]:
			return True

		for i in xrange(4,21):
			title_slice = title_raw[:i]
			# print 'slice', title_slice
			if self.ticker_words.has(title_slice):
				#print title_slice
				#print len(title_slice)
				#print ticker_name_equal
				#print len(ticker_name_equal)
				#print title_slice == ticker_name_equal
				#print title_slice == ticker_name_raw
				#print str( unicode(title_slice) ).strip()==str(strQ2B(unicode(ticker_name_equal))).strip()
				if not title_slice == ticker_name_raw and not title_slice == ticker_name_equal:
					# there is a ticker_name in title
					if not pending_legal(ticker_name_raw, ticker_name_raw):
						return False
					include_flag = False					

		if include_flag :
			for filter_word in self.filter_words:
				if filter_word in title_raw:
					# there is a ticker_name in title
					if not pending_legal(ticker_name_raw, ticker_name_raw):
						return False
		return True				

	def run(self, file_name_in, file_name_out):
		"""file must fit with csv format"""

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
			title_raw = strQ2B(unicode(terms[1])).encode('utf-8')
			pdf_link_raw = terms[2]
			ticker_name_equal = ''
			ticker_name_instead = ''
			#print title_raw
			include_flag = True

			# case: deal with equal tickers
			if self.ticker_equal_words.has(ticker_name_raw):
				ticker_name_equal = self.ticker_equal_words.find(ticker_name_raw).encode('utf-8').strip()
			#	print ticker_name_equal
			
			if self.ticker_instead_words.has(ticker_name_raw):
				ticker_name_instead = self.ticker_instead_words.find(ticker_name_raw).encode('utf-8').strip()
				if ticker_name_instead in title_raw:
					continue
			# case: title contains ticker_name
			if ticker_name_raw in title_raw:
				continue

			# case: title contains '年公司'
			if self.pass_words[0] in title_raw:
				continue

			# case : '公司' in the head of the title
			if title_raw[0:2] == self.filter_words[0]:
				continue 

			for i in xrange(4,21):
				title_slice = title_raw[:i]
				# print 'slice', title_slice
				if self.ticker_words.has(title_slice):
					#print title_slice
					#print len(title_slice)
					#print ticker_name_equal
					#print len(ticker_name_equal)
					#print title_slice == ticker_name_equal
					#print title_slice == ticker_name_raw
					#print str( unicode(title_slice) ).strip()==str(strQ2B(unicode(ticker_name_equal))).strip()
					if not title_slice == ticker_name_raw and not title_slice == ticker_name_equal:
						# there is a ticker_name in title
						csv_writer.writerow([ticker_name_raw, '0', title_raw, pdf_link_raw])
						count_terms_r1 = count_terms_r1+1
						include_flag = False
						

			if include_flag :
				for filter_word in self.filter_words:
					if filter_word in title_raw:
						# there is a ticker_name in title
						csv_writer.writerow([ticker_name_raw, '1' , title_raw, pdf_link_raw])
						count_terms_r2 = count_terms_r2+1
					
		print 'end',time.time()
		print 'sum_terms_sum:',count_terms_sum		
		print 'sum_terms_r1:',count_terms_r1	
		print 'sum_terms_r2:',count_terms_r2	
		fout.close()


""" 
example:
python filter_match_ticker_name.py dict_file input_file out_file

"""

if __name__=='__main__':
	argv = sys.argv[1:]
	file_name_dict = argv[0]
	file_name_equal_dict = argv[3]
	file_name_instead_dict = argv[4]
	file_name_in = argv[1]
	file_name_out = argv[2]
	filter_match_tool_instance = filter_match_tool(file_name_dict, file_name_equal_dict, file_name_instead_dict)
	filter_match_tool_instance.run(file_name_in, file_name_out)

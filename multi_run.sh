#!/bin/bash  
  
for(( i = 11; i < 20; i = i + 2 ))  
do  
{
	python filter_match_ticker_name.py /home/mateng/cb_data/doudi_cb/pdf_tables.data_df_part  $i `expr $i + 2` 
        echo $i 
	echo `expr $i + 2` 
}&  
done  
wait  

#!/usr/bin/python
import csv
import os
import numpy as np
import sys

def strip_space(input):
	#no_ret = input.strip(chr(0xd))
	#no_lf = no_ret.strip(ord())
	no_space = input.strip('\d')
	no_space = no_space.strip('\a')
	no_space = no_space.strip()


	return no_space

def linkmap2csv():
	print (sys.argv)
	arg_len = len(sys.argv)
	f_in = sys.argv[1] if arg_len > 1 else "bss.txt"
	csv_out = sys.argv[2] if arg_len > 2 else "null"

	print ("%s,%s"%(f_in, csv_out))
	if csv_out == 'null':
		prefix = f_in[:f_in.find('.')]
		csv_out = "%s.csv"%prefix
		print("output csv_file: %s"%csv_out)

	csv_raw = []
	index = 1
	with open(f_in, 'r') as f:
		for line in f.readlines():
			#print('original: ',line, line.find(' 0x'))
			#print('original: ',line)
			csv_raw_line = []
			#checking for lines of segments.
			if line.find(' 0x') == -1:
				#segment only line

				segment = line
				print(segment)

				segment = strip_space(segment)
				#skip single line
				#csv_raw_line=[index, segment]
				#csv_raw.append(csv_raw_line)
				#continue
			else:
			#find offset address, set first into segment, offset to offset
				segment = line[:line.find(' 0x')]
				#print(segment)

				line_process1 = line[line.find(' 0x')+1:]
				#print(line_process1)
				#print('offset end:', line_process1.find(' '))
				offset = line_process1[:line_process1.find(' ')]
				#print(offset)
				
				#find if size exist
				if line_process1.find(' 0x') == -1:
					#no size info, dierct add to description
					size_hex = ''
					size = ''
					description = line_process1[line_process1.find(' '):]
					print('seg:', segment, 'off:', offset, 'size_hex:', size_hex, 'size:', size, 'desc:',description)
					
				else:
					line_process2 = line_process1[line_process1.find(' 0x')+1:]
					size_hex = line_process2[:line_process2.find(' ')]
					size = int(size_hex, 16)
					description = line_process2[line_process2.find(' '):]
					print('seg:', segment, 'off:', offset, 'size_hex:', size_hex, 'size:', size, 'desc:',description)

				#print('last desp:%x'%(ord(description[-1])))
				segment = strip_space(segment)
				offset = strip_space(offset)
				size_hex = strip_space(size_hex)
				description = strip_space(description)
				csv_raw_line = [index, segment, offset, size_hex, size, description]
				#csv_raw_line = [index, segment, offset, size_hex, size]
				csv_raw.append(csv_raw_line)
			#skip for single line data
			index = index + 1

	#print(csv_raw)

	with open(csv_out, 'w') as csv_file:
		writer = csv.writer(csv_file, lineterminator='\n')
		titles = ['No.','Segment','Offset','Size(Hex)','Size','Description']
		writer.writerow(titles)

		#writer.writerows(csv_raw)
		for csv_item in csv_raw:
			writer.writerow(csv_item)


if __name__ == "__main__":

	linkmap2csv()

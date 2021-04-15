# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:36:02 2021

@author: seoun
"""

import sys
import os
os.chdir(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Drain")
import Drain_model

input_dir  = r'C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data\\'  # The input directory of log file
output_dir = 'Drain_result\\'  # The output directory of parsing results
log_file   = 'sql.log'  # The input log file name
log_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>'  # HDFS log format
# Regular expression list for optional preprocessing (default: [])
regex      = [
    r'blk_(|-)[0-9]+' , # block id
    r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
    r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes

parser = Drain_model.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)
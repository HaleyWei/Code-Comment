# -*- coding: utf-8 -*-
import codecs

Input_Data = "data/Comment.txt"
Output_Data = "data/Nl.txt"

with codecs.open(Output_Data,'w','utf-8') as file_output:
    with codecs.open(Input_Data, 'r', 'utf-8') as f:
        for line in f:
            line = line.replace('.',' . ')
            line = line.replace(',',' , ')
            line = line.replace('?',' ? ')
            line = line.replace(':',' : ')
            line = line.replace(';',' ; ')
            line = line.replace('!',' ! ')
            line = line.replace('(',' ( ')
            line = line.replace(')',' ) ')
            file_output.write(line)
        
    



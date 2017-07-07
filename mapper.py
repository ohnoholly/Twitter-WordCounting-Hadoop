#!/usr/bin/env python

import sys
import json
import fileinput
# input comes from STDIN (standard input)
for line in fileinput.input():
    try:
        #print 'IT IS DOING!!!'
        # remove leading and trailing whitespace
        #line = line.strip()
        #print line
        data = json.loads(line)
        retweet = data["retweeted"]
        if retweet == 'false':
                continue
        text = data["text"]
        # split the line into words
        words = line.split( )
         # increase counters
        for word in words:
                if word == 'han' or  word == 'hon' or  word == 'den' or  word=='det' or  word=='denna' or word =='denne' or word =='hen':
                         # write the results to STDOUT (standard output);
                         # what we output here will be the input for the
                         # Reduce step, i.e. the input for reducer.py
                         # tab-delimited; the trivial word count is 1
                         print '%s\t%s' % (word, 1)
    except:
        #print 'not JSON format'
        continue




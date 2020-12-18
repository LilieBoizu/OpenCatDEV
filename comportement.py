#!/usr/bin/python3
from ardSerial import *


schedule = [['b25 160',3],\
			['whiNybble',10],\
            ['kwk',10],\
            ['ksit',3],\
            ['b60 160',3],
            ['d',10]]

for task in schedule:
    wrapper(task)


# walk = ['kwk', 0]
# rest = ['d',0]
# wrapper(walk)
# for i in range(100000) : 
      # print("talking while walking")
# wrapper(rest)

from time import sleep
import os
x='''
                                                                               |
                                                STATUS:     {}



    {}
'''
c=0
while True:
    os.system('clear')
    if c%2==0:
        status=''
    else:
        status='testing'
    print(x.format(status,c))
    c+=1
    sleep(.1)

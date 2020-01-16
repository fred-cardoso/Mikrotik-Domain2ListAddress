'''
Created on 07/12/2019

@author: Fred
'''

import sys
import time

MIKROTIK_IP_FW_ADDR_LIST_CMD = "/ip firewall address-list"

class Parser():
    def __init__(self, input_file, output_file, list_name, timeout):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__list_name = list_name
        self.__timeout = timeout
        self.__lines = []
		
		#TODO: Timeout format validation
        
    def __read_input_file(self):
        try:
            f = open(self.__input_file, "r")
        except FileNotFoundError:
            print("Input file not found!")
            sys.exit()
            
        for line in f:
            line = line.replace('\n', '').replace('\r', '') #Replaces line breaks and carriges returns
            if (len(line) > 0 and (line[0] == "#" or line[0] == "")) or len(line) < 1: #Ignores empty lines, or lines starting with # (comments)
                continue
            
            self.__lines.append(line)
            
    def __write_output_file(self):
        try:
            f = open(self.__output_file, "w")
        except Exception:
            print("Error writing to output file!")
            sys.exit()
        
        #Enters in address-list context
        f.write(MIKROTIK_IP_FW_ADDR_LIST_CMD + "\n")
        
        #add address=address list=list_name
        for line in self.__lines:
            f.write('add address=' + line + ' timeout="' + timeout + '" list="' + list_name + '"\n')
        
        f.close()
        
    def convert(self):
        self.__read_input_file()
        self.__write_output_file()

if __name__ == '__main__':
    n_args = len(sys.argv) - 1
    
    if n_args != 4:
        print("Invalid parameters!")
        print("Usage: python3 parser.py input_path output_path list_name timeout")
        print("Example: python3 parser.py /path/to/address_list.txt /path/to/output_file.rsc list_name 7d 00:00:00")
        sys.exit()
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    list_name = sys.argv[3]
    timeout = sys.argv[4]
    
    parser = Parser(input_file, output_file, list_name, timeout)
    parser.convert()
    
    print("Done!")
    time.sleep(2)
    
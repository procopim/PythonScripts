#!/usr/bin/python

'''
@procopim, Sept 2023

This script masks character based endpoints by raising each character one position, with end of alphabet characters coming around 
to the beginning of alphabet.  We also handle IPs by raising each octet by 255. 
This helps us with making defunct live endpoints during testing of business logic. 
'''

import argparse

def demask_hostname(host_name):
    masked_hostname = ''
    for character in host_name:
        if character.isalpha() and character != 'a' and character != 'A':
            masked_hostname = masked_hostname + chr(ord(character) - 1)
        elif character == 'a':
            masked_hostname = masked_hostname + 'z'
        elif character == 'A':
            masked_hostname = masked_hostname + 'Z'
        else:
            masked_hostname = masked_hostname + character
    return masked_hostname

def mask_hostname(host_name):
    masked_hostname = ''
    for character in host_name:
        if character.isalpha() and character != 'z' and character != 'Z':
            masked_hostname = masked_hostname + chr(ord(character) + 1)
        elif character == 'z':
            masked_hostname = masked_hostname + 'a'
        elif character == 'Z':
            masked_hostname = masked_hostname + 'A'
        else:
            masked_hostname = masked_hostname + character
    return masked_hostname

def demask_IP(IP):
    demasked=''
    octets = IP.split('.')
    for idx, n in enumerate(octets):
        if (n.isdigit() or n == '0') and not idx == (len(octets)-1):
            demasked = demasked + str(int(n) - 255)
            demasked = demasked + '.'
        elif (n.isdigit() or n == '0') and idx == (len(octets)-1):
            demasked = demasked + str(int(n) - 255)
    return demasked

def mask_IP(IP):
    masked=''
    octets = IP.split('.')
    for idx, n in enumerate(octets):
        if (n.isdigit() or n == '0') and not idx == (len(octets)-1):
            masked = masked + str(int(n) + 255)
            masked = masked + '.'
        elif (n.isdigit() or n == '0') and idx == (len(octets)-1):
            masked = masked + str(int(n) + 255)
    return masked


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--word')
    parser.add_argument('--ip')
    parser.add_argument('--O', help="M or D")
    args = parser.parse_args()
    if args.word:
        if args.O == "M":
            print(args.word, args.O)
            print(mask_hostname(args.word))
        elif args.O == "D":
            print(args.word, args.O)
            print(demask_hostname(args.word))
        else:
            print("invalid options")
    elif args.ip:
        if args.O == "M":
            print(args.ip, args.O)
            print(mask_IP(args.ip))
        elif args.O == "D":
            print(args.ip, args.O)
            print(demask_IP(args.ip))
        else:
            print("invalid options")
            
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

def gettree(number, count=3):
    """
    Сформировать дерево каталогов
    """
    result = []
    newline = str(number)
    while len(newline) % count:
        newline = '0' + newline
    for i in range(0, len(newline)//count):
        result.append(newline[i*count:i*count+count])
    return result

def gethashtree(hash, count=3):
    """
    Сформировать дерево каталогов
    """
    result = []
    for i in range(0, count):
        element = hash[2*i:2*(i+1)]
        result.append(element)
    return '/'.join(result)

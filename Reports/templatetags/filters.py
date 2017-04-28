'''
Created on Apr 28, 2017

@author: Akila
'''
from django import template

register = template.Library()

def getValidEntry(value):
    if (value==-1.0):
        return "AB"
    elif(value==-2.0):
        return "NA"
    else:
        return value
register.filter('getValidEntry', getValidEntry)
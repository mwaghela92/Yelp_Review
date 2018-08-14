#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 12:11:48 2018

@author: mayur
"""


import requests
import urllib.parse

def retried_func(*args, **kwargs):
        MAX_TRIES = 10
        tries = 0
        while True:
            resp = requests.get(*args , **kwargs)
            if resp.status_code > 200 and tries < MAX_TRIES:
                tries += 1
                continue
            break
        if resp.status_code > 200:
            resp = 'none'
        return resp
    

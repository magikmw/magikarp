#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Misc helper functions, mostly temporary"""

from datetime import datetime

def CurrentTimeString():
    """Produces a string of YYYY-MM-DD HH:MM:SS"""
    now = datetime.now()
    string = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)
    return string

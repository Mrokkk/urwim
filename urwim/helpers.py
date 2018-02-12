#!/usr/bin/env python3

import sys
import traceback

def log_exception(logger):
    tb = traceback.format_exc().split('\n')
    for trace in tb:
        logger.warning(trace)

def clamp(value, min_val=-9999, max_val=9999):
    if value > max_val: return max_val
    if value < min_val: return min_val
    return value


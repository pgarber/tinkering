#!/usr/bin/env python
import os
import subprocess

def display_ps(pid=None):
    # Used for some simple debugging to track memory usage
    if not pid:
        pid = os.getpid()
    cmd = "ps u %s" % (pid)
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out_msg, err_msg = handle.communicate(None)
    return out_msg

if __name__ == "__main__":
    print display_ps()

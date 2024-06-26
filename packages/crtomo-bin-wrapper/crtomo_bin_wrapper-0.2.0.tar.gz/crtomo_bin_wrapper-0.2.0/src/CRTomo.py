#!/usr/bin/env python
# Execute a suitable CRTomo binary in the present directory
import os
from importlib.resources import files
import subprocess


def main():
    basedir = files('crtomo_bin_wrapper')
    crtomo_bin = str(basedir) + os.sep + 'binaries' + os.sep + 'CRTomo_stable'
    subprocess.call(crtomo_bin, shell=True)

#!/usr/bin/env python

import subprocess
import os
import getopt
import numpy as np
from numpy import linalg as LA
import math
from shutil import copy

for i in range(0, 105, 5):
  for j in range(0, 105, 5):
    k = 100 - i - j
    if (k >= 0):
      x = [0, 0, 0]
      x[0] = float(i)/100.0
      x[1] = float(j)/100.0
      x[2] = float(k)/100.0

      x1 = "{:.2f}".format(i/100.0)
      x2 = "{:.2f}".format(j/100.0)
      x3 = "{:.2f}".format(k/100.0)
      comp = x1 + "    " + x2 + "    " + x3 + "    "
      dirname = x1 + "_" + x2 + "_" + x3
      
      Tb=0

      with open(dirname+"/peace.out", "r") as peace:
        lines = peace.readlines()
        for l in lines:
          if ("Calculated phase transition" in  l):
            tmp = l.split()
            Tb = int(float(tmp[3])-0.15)
        peace.close()
        
      with open(dirname+"/thermo1.dat", "r") as thermo:
        lines = thermo.readlines()
        Hl = lines[Tb-272].split()
        Hl = float(Hl[2])
        Hg = lines[Tb-271].split()
        Hg = float(Hg[2])

        Hvap = Hg-Hl

        print(Hvap)
        
        thermo.close()











        
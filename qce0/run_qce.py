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

      
      ncomp = int(math.ceil(i/100.0) + math.ceil(j/100.0) + math.ceil(k/100.0))
      
      with open("qce.input", "w") as qce:
        qce.write("[system]\n")
        qce.write("components {}\n\n".format(ncomp))
        qce.write("[qce]\n")
        qce.write("amf 0.0\n")
        qce.write("bxv 1.0\n\n")
        qce.write("[ensemble]\n")
        qce.write("temperature 273.15 399.15 127 # K\n")
        qce.write("pressure 1.01325 # bar\n")
        if (i > 0):
          if (j > 0):
            if (k > 0):
              qce.write("monomer_amounts " + x1 + " " + x2 + " " + x3 + "\n\n")
              cmd="peacemaker qce.input cmw.clusterset > peace.out"
            else:
              qce.write("monomer_amounts " + x1 + " " + x2 + "\n\n")
              cmd="peacemaker qce.input cm.clusterset > peace.out"
          elif (k > 0):
            qce.write("monomer_amounts " + x1 + " " + x3 + "\n\n")
            cmd="peacemaker qce.input cw.clusterset > peace.out"
          else:
            qce.write("monomer_amounts " + x1 + "\n\n")
            cmd="peacemaker qce.input c.clusterset > peace.out"
        elif (j > 0):
          if (k > 0):
            qce.write("monomer_amounts " + x2 + " " + x3 + "\n\n")
            cmd="peacemaker qce.input mw.clusterset > peace.out"
          else:
            qce.write("monomer_amounts " + x2 + "\n\n")
            cmd="peacemaker qce.input m.clusterset > peace.out"
        else:
          qce.write("monomer_amounts " + x3 + "\n\n")
          cmd="peacemaker qce.input w.clusterset > peace.out"
        
        qce.close()
        
      dirname = x1 + "_" + x2 + "_" + x3
      
      print(dirname)
      subprocess.Popen(cmd, shell=True).wait()
      
      try:
        os.makedirs(dirname)
      except OSError:
        pass
      files = os.listdir(".")
      for fname in files:
          if os.path.isfile(fname) and not fname == "run_qce.py":
              copy(fname, dirname)
          













        
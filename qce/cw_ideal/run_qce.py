#!/usr/bin/env python

import subprocess
import os
import getopt
import numpy as np
from numpy import linalg as LA
import math
from shutil import copy

Trk = [0, 0, 0]

Trk[0] = [-3.521420e+01,   2.292960e+00,  -1.655342e+01,   5.939158e+00,  -2.355837e+01,   4.216619e+01,   2.812976e+01,  -6.492807e+01,  -4.702823e+01,   6.642041e+01]
Trk[1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Trk[2] = [-3.776215e+01,  -3.081547e+01,  -2.385351e+01,  -1.616017e+01,  -1.916869e+01,  -2.442081e+01,   7.382781e+00,   2.303300e+01,  -2.072821e+01,  -2.594481e+01]

Vrk = [0, 0, 0]

Vrk[0] = [-0.541, -0.273, -0.056, 0]
Vrk[1] = [0, 0, 0, 0]
Vrk[2] = [-4.08, -0.43, 0.69, 1.2]


Tb = [334.35, 337.65, 373.15]
V = [0.080701030927835, 0.040676782692481, 0.018069508526]
M = [119.3770, 32.0422, 18.0153]


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

      a1 = 1.46061
      a2 = 0.603485
      a3 = 0.294839
           
      b1 = 1.36005
      b2 = 1.12982
      b3 = 1.13003

      eV = 0.0
      for m in range(3):
        for n in range(3):
          if (n > m):
            beV = 0.0
            if (x[m] > 0.0):
              for g in range(len(Vrk[m+n-1])):
                beV = beV + Vrk[m+n-1][g] * (1.0 - 2.0 * (1.0/(x[n]/x[m] + 1.0)))**g
            eV = eV + beV * x[m] * x[n]
      pV = x[0] * V[0] + x[1] * V[1] + x[2] * V[2]
      pV = pV + eV/1000

      dens = (x[0] * M[0] + x[1] * M[1] + x[2] * M[2])/pV/1000.0
      
      eTb = 0.0
      for m in range(3):
        for n in range(3):
          if (n > m):
            beTb = 0.0
            if (x[m] > 0.0):
              for g in range(len(Trk[m+n-1])):
                beTb = beTb + Trk[m+n-1][g] * (1.0 - 2.0 * (1.0/(x[n]/x[m] + 1.0)))**g
            eTb = eTb + beTb * x[m] * x[n]
      pt  = x[0] * Tb[0] + x[1] * Tb[1] + x[2] * Tb[2] + eTb
      
      
      ncomp = int(math.ceil(i/100.0) + math.ceil(j/100.0) + math.ceil(k/100.0))
      
      amf = (i * a1 + j * a2 + k * a3)/100.0
      bxv = (i * b1 + j * b2 + k * b3)/100.0

      with open("qce.input", "w") as qce:
        qce.write("[system]\n")
        qce.write("components {}\n\n".format(ncomp))
        qce.write("[qce]\n")
        qce.write("amf {}\n".format(amf))
        qce.write("bxv {}\n".format(bxv))
        qce.write("grid_iterations 1\n")
        qce.write("optimizer 1\n\n")
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
        qce.write("[reference]\n")
        qce.write("density 298.15 {} # K; g/cm^3\n".format(dens))
        qce.write("phase_transition {} # K\n".format(pt))
#        qce.write("isobar isob.dat # dm^3/mol\n\n")
        
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
          













        
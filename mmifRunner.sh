#!/bin/bash

#--------------------------------------------------------------------------------------
#
# Developed by Leonardo Hoinaski - leonardo.hoinaski@ufsc.br
#
#---------------------------------- Inputs --------------------------------------------

MMIFhome=/home/lcqar/MMIFv4.0
outPath=/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019/METFILES
wrf_dir=/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019
STARTDAY=2019-01-01
ENDDAY=2019-12-31

python3 ${MMIFhome}/shRunnerWRFtoAERMOD.py ${MMIFhome} ${wrf_dir} ${outPath} ${>




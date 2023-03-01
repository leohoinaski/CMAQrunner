#!/bin/bash

#--------------------------------------------------------------------------------------
#
# Developed by Leonardo Hoinaski - leonardo.hoinaski@ufsc.br
#
#---------------------------------- Inputs --------------------------------------------

MMIFhome=/home/lcqar/MMIFv4.0
outPath=/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019
wrf_dir=/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019
STARTDAY=2019-01-01
ENDDAY=2019-01-02

python3 ${MMIFhome}/shRunnerWRFtoAERMOD.py ${MMIFhome} ${outPath} ${wrf_dir} ${STARTDAY} ${ENDDAY} 

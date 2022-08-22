#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:00:25 2022

@author: leohoinaski
"""
import argparse
#import os

def writePrepMeganInput(MEGANHome,wrf_dir,ncols,nrows):  
    scriptPath = MEGANHome +'/prepmegan4cmaq_2014-06-02'       
    file1 = open(scriptPath + "/prepmegan4cmaq.inp","w") 
    file1.write('&control\n')
    file1.write('\ndomains = 1,')
    file1.write('\nstart_lai_mnth = 1,')
    file1.write('\nend_lai_mnth   = 12,')              
    file1.write("\nwrf_dir = '"+wrf_dir+"',")
    file1.write("\nmegan_dir = '"+MEGANHome+"/inputs',")
    file1.write("\nout_dir = '"+MEGANHome+"/outputs',")
    file1.write('\n')
    file1.write('\n/')
    file1.write('\n')
    file1.write('\n&windowdefs')
    file1.write('\n/')
    file1.write('\n x0         =  1,')
    file1.write('\n y0         =  1,')
    file1.write('\n ncolsin    =  '+str(ncols)+',')    
    file1.write('\n nrowsin    =  '+str(nrows)+',')    
    file1.write('\n')
    file1.write('\n/') 
    file1.close()
    return MEGANHome    

def writeRunMet2mgn(MEGANHome,GDNAM,YEAR,STJD,EDJD,mcipPath):  
    file1 = open(MEGANHome+"/MEGANv2.10/work/run.met2mgn.v210.csh","w") 

    str1 ='#!/bin/csh\
\n#\
\n# MET2MGN v2.10 \
\n# --\
\n#\
\n#\
\n# TPAR2IOAPI v2.03a \
\n# --added 26-category landuse capability for mm5camx (number of landuse categories defined by NLU) \
\n# --added capability for LATLON and UTM projections\
\n# --added capability for MCIP v3.3 input (2m temperatures)\
\n# --bug in PAR processing subroutine fixed where first few hours in GMT produced zero PAR\
\n# --added code to fill missing par data (if valid data exists for the hours surrounding it)\
\n#\
\n# TPAR2IOAPI v2.0\
\n# --added capability for MM5 or MCIP input\
\n#\
\n#\
\n#        RGRND/PAR options:\
\n#           setenv MM5RAD  Y   Solar radiation obtained from MM5\
\n#           OR \
\n#           setenv MCIPRAD Y   Solar radiation obtained from MCIP\
\n#                  --MEGAN will internally calculate PAR for each of these options and user needs to  \
\n#                    specify setenv PAR_INPUT N in the MEGAN runfile \
\n#           OR\
\n#           setenv SATPAR Y (satellite-derived PAR from UMD GCIP/SRB files)\
\n#                  --user needs to specify setenv PAR_INPUT Y in the MEGAN runfile\
\n#\
\n#        TEMP options:\
\n#           setenv CAMXTEMP Y         2m temperature, calculated from mm5camx output files\
\n#           OR\
\n#           setenv MM5MET  Y         2m temperature, calculated from MM5 output files\
\n#                                     Note: 2m temperature is calculated since the P-X/ACM PBL\
\n#                                     MM5 configuration (most commonly used LSM/PBL scheme for AQ \
\n#                                     modeling purposes) does not produce 2m temperatures.\
\n#           OR\
\n#           setenv MCIPMET Y         temperature obtained from MCIP\
\n#              -setenv TMCIP  TEMP2   2m temperature, use for MCIP v3.3 or newer\
\n#              -setenv TMCIP  TEMP1P5 1.5m temperature, use for MCIP v3.2 or older\
\n#\
\n#        TZONE   time zone for input mm5CAMx files \
\n#        NLAY    number of layers contained in input mm5CAMx files \
\n#        NLU     number of landuse categories contained in CAMx landuse file \
\n#\
\n\
\n############################################################\
\n\
\n\
\n\
\n############################################################\
\n# Episodes\
\n############################################################'
    file1.write(str1)    
    file1.write('\nset dom = '+GDNAM)
    file1.write('\nset STJD = '+ str(YEAR)+str(STJD).zfill(3)) #2019001
    file1.write('\nset EDJD = '+ str(YEAR)+str(EDJD).zfill(3)) #2019024
    file1.write('\n')
    file1.write('\nsetenv EPISODE_SDATE '+ str(YEAR)+str(STJD).zfill(3)) #2019001
    file1.write('\nsetenv EPISODE_STIME  000000')
    file1.write('\n')
    file1.write('\n############################################################')
    file1.write('\n#set for grid')
    file1.write('\n############################################################')
    file1.write('\nsetenv GRIDDESC GRIDDESC')
    file1.write('\nsetenv GDNAM3D '+GDNAM)
    file1.write('\n')
    file1.write('\n')
    file1.write('\nsource '+MEGANHome+'/MEGANv2.10/setcase.csh')
    file1.write('\nsetenv PROG met2mgn')
    file1.write('\nsetenv EXE $MGNEXE/$PROG') 
    file1.write('\nset logdir = logdir/$PROG')
    file1.write('\nif ( ! -e $logdir) mkdir -p $logdir')
    file1.write('\nset INPPATH     = '+mcipPath)
    file1.write('\nset OUTPATH     = $MGNINP/MGNMET')
    file1.write('\nif (! -e $OUTPATH) mkdir $OUTPATH')
    file1.write('\nsetenv PFILE $OUTPATH/PFILE')
    file1.write('\n############################################################')
    file1.write('\n# Looping')
    file1.write('\n############################################################')
    file1.write('\nset JDATE = $STJD')
    file1.write('\n#set Y4 = 2008')
    file1.write('\n#set Y2 = 08 ')
    file1.write('\n#set MM = 07')
    file1.write('\n# DD = 21 ')
    file1.write('\n# DDm1 = 20')
    file1.write('\n#while ($JDATE <= $EDJD)')
    file1.write('\nif ($JDATE == 2008367) set JDATE = 2009001')
    file1.write('\n@ jdy  = $JDATE - 2000000')
    file1.write('\n@ jdyf  = $EDJD - 2000000')
    file1.write('\n#set Y4 = 2008')
    file1.write('\n#set Y2 = 08 ')
    file1.write('\n#set MM = 07')
    file1.write('\n#@ DD++')
    file1.write('\n#set start/end dates')
    file1.write('\nsetenv STDATE ${jdy}00')
    file1.write('\nsetenv ENDATE ${jdyf}00')
    file1.write('\n#')
    file1.write('\n#set if using MM5 output files')
    file1.write('\nsetenv MM5MET N')
    file1.write('\nsetenv MM5RAD N')
    file1.write('\n#set if using MCIP output files')
    file1.write('\nsetenv MCIPMET Y')
    file1.write('\nsetenv TMCIP  TEMP2')         #MCIP v3.3 or newer
    file1.write('\n#setenv TMCIP  TEMP1P5')    #MCIP v3.2 or older
    file1.write('\nsetenv MCIPRAD Y') 
    file1.write('\nif ($JDATE == $EPISODE_SDATE) then')
    file1.write('\n  setenv METCRO2Dfile1 $INPPATH/METCRO2D_$GDNAM3D.nc') #METCRO2D.$GDNAM>
    file1.write('\nelse')
    file1.write('\n  setenv METCRO2Dfile1 $INPPATH/METCRO2D_$GDNAM3D.nc')   #METCRO2D.$GDN>
    file1.write('\n  setenv METCRO2Dfile2 $INPPATH/METCRO2D_$GDNAM3D.nc')  #METCRO2D.$GDNA>
    file1.write('\nendif')
    file1.write('\nsetenv METCRO3Dfile  $INPPATH/METCRO3D_$GDNAM3D.nc')  #METCRO3D.$GDNAM3D
    file1.write('\nsetenv METDOT3Dfile  $INPPATH/METDOT3D_$GDNAM3D.nc') #METDOT3D.$GDNAM3D
    file1.write('\nsetenv OUTFILE $OUTPATH/MET.MEGAN.$GDNAM3D.ncf')  #MET.MEGAN.$GDNAM3D.$>
    file1.write('\nrm -rf $OUTFILE')
    file1.write('\n$EXE |tee $logdir/log.$PROG.$GDNAM3D.txt') 
    file1.write('\n@ JDATE++')
    file1.write('\nend  # End while JDATE')
    file1.close()
    return MEGANHome 

def writeRunEmproc(MEGANHome,GDNAM,YEAR,STJD):  
    file1 = open(MEGANHome+"/MEGANv2.10/work/run.emproc.v210.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write('\n#')    
    file1.write('\nsource '+MEGANHome+'/MEGANv2.10/setcase.csh')
    file1.write('\n## Directory setups')
    file1.write('\nsetenv PRJ '+ GDNAM) 
    file1.write('\nsetenv PROMPTFLAG N')    
    file1.write('\n# Program directory')
    file1.write('\nsetenv PROG   emproc')
    file1.write('\nsetenv EXEDIR $MGNEXE')
    file1.write('\nsetenv EXE    $EXEDIR/$PROG')  
    file1.write('\n# Input map data directory')
    file1.write('\nsetenv INPDIR $MGNINP')    
    file1.write('\n# MCIP input directory')
    file1.write('\nsetenv METDIR $MGNINP/MGNMET')  
    file1.write('\n# Intermediate file directory')
    file1.write('\nsetenv INTDIR $MGNINT')   
    file1.write('\n# Output directory')
    file1.write('\nsetenv OUTDIR $MGNOUT')   
    file1.write('\n# Log directory')
    file1.write('\nsetenv LOGDIR $MGNLOG/$PROG')
    file1.write('\nif ( ! -e $LOGDIR ) mkdir -p $LOGDIR')
    file1.write('\n#####################################################################>')   
    file1.write('\nset dom = '+GDNAM)
    file1.write('\nset JD = '+ str(YEAR)+str(STJD).zfill(3))
    file1.write('\nsetenv SDATE $JD')        #start date
    file1.write('\nsetenv STIME 0')
    file1.write('\nsetenv RLENG 250000')
    file1.write('\n#####################################################################>')  
    file1.write('\n#####################################################################>')
    file1.write('\n# Set up for MEGAN')
    file1.write('\nsetenv RUN_MEGAN   Y')       # Run megan?
    file1.write('\n# By default MEGAN will use data from MGNMET unless specify below')
    file1.write('\nsetenv ONLN_DT     Y')       # Use online daily average temperature   
    file1.write('\nsetenv ONLN_DS     Y ')      # Use online daily average solar radiation    
    file1.write('\n# Grid definition')
    file1.write('\nsetenv GRIDDESC $MGNRUN/GRIDDESC')
    file1.write('\nsetenv GDNAM3D '+ GDNAM)    
    file1.write('\n# EFMAPS')
    file1.write('\nsetenv EFMAPS $INPDIR/EFMAPS.${dom}.ncf')   
    file1.write('\n# PFTS16')
    file1.write('\nsetenv PFTS16 $INPDIR/PFTS16.${dom}.ncf')  
    file1.write('\n# LAIS46')
    file1.write('\nsetenv LAIS46 $INPDIR/LAIS46.${dom}.ncf')   
    file1.write('\n# MGNMET')
    file1.write('\nsetenv MGNMET $METDIR/MET.MEGAN.$GDNAM3D.ncf')  
    file1.write('\n# Output')
    file1.write('\nsetenv MGNERS $INPDIR/ER.$GDNAM3D.ncf')  
    file1.write('\n#####################################################################>')
    file1.write('\n## Run MEGAN')
    file1.write("\nif ( $RUN_MEGAN == 'Y' ) then")
    file1.write('\n   rm -f $MGNERS')
    file1.write('\n   time $EXE #>&! $LOGDIR/log.run.$PROG.$GDNAM3D.$SDATE.txt')
    file1.write('\nendif') 
    file1.write('\n@ JD++')
    #end  # End while JD
    file1.close()
    return MEGANHome 

def writeRunMgn2mech(MEGANHome,GDNAM,YEAR,STJD):  
    file1 = open(MEGANHome+"/MEGANv2.10/work/run.mgn2mech.v210.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write('\n#') 
    file1.write('\n#####################################################################>')
    file1.write('\nsource '+MEGANHome+'/MEGANv2.10/setcase.csh')
    ## Directory setups
    file1.write('\nsetenv PRJ '+GDNAM)
    file1.write('\nsetenv PROMPTFLAG N')
    # Program directory
    file1.write('\nsetenv PROG   mgn2mech.wmap')
    file1.write('\nsetenv EXEDIR $MGNEXE')
    file1.write('\nsetenv EXE    $EXEDIR/$PROG')
    # Input map data directory
    file1.write('\nsetenv INPDIR $MGNINP')
    # Intermediate file directory
    file1.write('\nsetenv INTDIR $MGNOUT')
    # Output directory
    file1.write('\nsetenv OUTDIR $MGNOUT')
    # MCIP input directory
    file1.write('\nsetenv METDIR $MGNINP/MGNMET')
    # Log directory
    file1.write('\nsetenv LOGDIR $MGNLOG/$PROG')
    file1.write('\nif ( ! -e $LOGDIR ) mkdir -p $LOGDIR')
    #####################################################################>
    file1.write('\nset dom = '+GDNAM)
    file1.write('\nset JD = '+ str(YEAR)+str(STJD).zfill(3))
    #####################################################################>
    # Set up time and date to process
    file1.write('\nsetenv SDATE $JD')        #start date
    file1.write('\nsetenv STIME 0')
    file1.write('\nsetenv RLENG 250000')
    file1.write('\nsetenv TSTEP 10000')
    #####################################################################>
    # Set up for MECHCONV
    file1.write('\nsetenv RUN_SPECIATE   Y')    # run MG2MECH
    file1.write('\nsetenv RUN_CONVERSION Y')    # run conversions?
                               # run conversions MEGAN to model mechanism
                               # units are mole/s
    file1.write('\nsetenv SPCTONHR       N')    # speciation output unit in tonnes per hour
                               # This will convert 138 species to tonne p>
                               # hour or mechasnim species to tonne per h>
    # If RUN_CONVERSION is set to "Y", one of mechanisms has to be select>
    file1.write('\n#setenv MECHANISM    RADM2')
    file1.write('\n#setenv MECHANISM    RACM')
    file1.write('\n#setenv MECHANISM    CBMZ')
    file1.write('\n#setenv MECHANISM    CB05')
    file1.write('\nsetenv MECHANISM    CB6')
    file1.write('\n#setenv MECHANISM    SOAX')
    file1.write('\n#setenv MECHANISM    SAPRC99')
    file1.write('\n#setenv MECHANISM    SAPRC99Q')
    file1.write('\n#setenv MECHANISM    SAPRC99X')
    file1.write('\n# Grid name')
    file1.write('\nsetenv GDNAM3D ${dom}')
    # EFMAPS NetCDF input file
    file1.write('\nsetenv EFMAPS  $INPDIR/EFMAPS.${dom}.ncf')
    # PFTS16 NetCDF input file
    file1.write('\nsetenv PFTS16  $INPDIR/PFTS16.${dom}.ncf')
    # MEGAN ER filename
    file1.write('\nsetenv MGNERS $INPDIR/ER.$GDNAM3D.ncf')
    # Output filename
    file1.write('\nsetenv MGNOUT $OUTDIR/MEGANv2.10.$GDNAM3D.$MECHANISM.$SDATE.ncf')
    
    
    ## Run speciation and mechanism conversion
    file1.write("\nif ( $RUN_SPECIATE == 'Y' ) then")
    file1.write('\n   rm -f $MGNOUT')
    file1.write('\n   $EXE | tee $LOGDIR/log.run.$PROG.$GDNAM3D.$MECHANISM.$SDATE.txt')
    file1.write('\nendif')
    file1.write('\n@ JD++')
    #end  # End while JD
    file1.close()
    return MEGANHome      
        
def writeRunTxt2ioapi(MEGANHome,GDNAM):
    #os.remove(MEGANHome+"/MEGANv2.10/work/run.txt2ioapi.v210.csh")
    file1 = open(MEGANHome+"/MEGANv2.10/work/run.txt2ioapi.v210.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write("\n##########################################################")
    file1.write('\n## Common setups')
    file1.write('\nsource '+MEGANHome+'/MEGANv2.10/setcase.csh')        
    file1.write('\n')
    file1.write('\nsetenv PRJ '+GDNAM) 
    file1.write('\nsetenv DOM '+GDNAM) 
    file1.write('\n')
    file1.write('\nsetenv PROMPTFLAG N')
    file1.write('\nsetenv PROG   txt2ioapi')
    file1.write('\nsetenv EXEDIR $MGNEXE')
    file1.write('\nsetenv EXEC   $EXEDIR/$PROG')
    file1.write('\nsetenv GRIDDESC $MGNRUN/GRIDDESC')
    file1.write('\nsetenv GDNAM3D ${DOM}') 
    file1.write('\n')
    file1.write('\n## File setups')
    file1.write('\n## Inputs')
    file1.write('\nsetenv EFSTXTF $MGNINP/EF210.csv')
    file1.write('\nsetenv PFTTXTF $MGNINP/PFT210.csv')
    file1.write('\nsetenv LAITXTF $MGNINP/LAI210.csv')
    file1.write('\n## Outputs')
    file1.write('\nsetenv EFMAPS  $MGNINP/EFMAPS.${DOM}.ncf')
    file1.write('\nsetenv PFTS16  $MGNINP/PFTS16.${DOM}.ncf')
    file1.write('\nsetenv LAIS46  $MGNINP/LAIS46.${DOM}.ncf')
    file1.write('\n')
    file1.write('\n## Run control')
    file1.write('\nsetenv RUN_EFS T       # [T|F]')
    file1.write('\nsetenv RUN_LAI T       # [T|F]')
    file1.write('\nsetenv RUN_PFT T       # [T|F]')
    ## Run TXT2IOAPI
    file1.write('\n########################################################################')
    file1.write('\n')
    file1.write('\n')
    file1.write('\n')
    file1.write('\n')
    file1.write('\n')
    file1.write('\n## Run TXT2IOAPI')
    file1.write('\nrm -f $EFMAPS $LAIS46 $PFTS16')
    file1.write('\nif ( ! -e $MGNLOG/$PROG ) mkdir -p $MGNLOG/$PROG')
    file1.write('\n$EXEC | tee $MGNLOG/$PROG/log.run.$PROG.${PRJ}${DOM}.txt')
    file1.write('\n')
    file1.close()
    return MEGANHome         
        
def writeRunMEGANsetcase(MEGANHome):  
    #os.remove(MEGANHome+"/MEGANv2.10/setcase.csh")
    file1 = open(MEGANHome+"/MEGANv2.10/setcase.csh","w") 
    file1.write('#\n')
    file1.write('setenv MGNHOME '+MEGANHome+'/MEGANv2.10')
    file1.write('\nsetenv MGNSRC $MGNHOME/src')
    file1.write('\nsetenv MGNLIB $MGNHOME/lib')
    file1.write('\nsetenv MGNEXE $MGNHOME/bin')
    file1.write('\nsetenv MGNRUN $MGNHOME/work')
    file1.write('\nsetenv MGNINP '+MEGANHome+'/inputs')
    file1.write('\nsetenv MGNOUT $MGNHOME/outputs')
    file1.write('\nsetenv MGNINT $MGNHOME/outputs')
    file1.write('\nsetenv MGNLOG $MGNHOME/work/logdir')
    file1.write('\n')
    file1.write('\n')          
    file1.write('\nif ( ! -e $MGNINP ) then')
    file1.write('\n   mkdir -p $MGNINP/MAP')
    file1.write('\n   mkdir -p $MGNINP/MGNMET')
    file1.write('\n   mkdir -p $MGNINP/PAR')
    file1.write('\nendif')
    file1.write('\nif ( ! -e $MGNINT ) mkdir -p $MGNINT')
    file1.write('\nif ( ! -e $MGNLOG ) mkdir -p $MGNLOG')
    file1.close()
    return MEGANHome               

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('MEGANHome')
    parser.add_argument('mcipPath')
    parser.add_argument('wrf_dir')
    parser.add_argument('GDNAM')
    parser.add_argument('YEAR')
    parser.add_argument('STJD')
    parser.add_argument('EDJD')
    parser.add_argument('ncols')
    parser.add_argument('nrows')
    args = parser.parse_args()
    MEGANHome = args.MEGANHome
    mcipPath = args.mcipPath
    wrf_dir = args.wrf_dir
    GDNAM = args.GDNAM
    YEAR = args.YEAR
    STJD = args.STJD
    EDJD = args.EDJD
    ncols = args.ncols
    nrows = args.nrows
    writeRunMEGANsetcase(MEGANHome)
    writePrepMeganInput(MEGANHome,wrf_dir,ncols,nrows)
    writeRunTxt2ioapi(MEGANHome,GDNAM)
    writeRunMet2mgn(MEGANHome,GDNAM,YEAR,STJD,EDJD,mcipPath)
    writeRunEmproc(MEGANHome,GDNAM,YEAR,STJD)
    writeRunMgn2mech(MEGANHome,GDNAM,YEAR,STJD)

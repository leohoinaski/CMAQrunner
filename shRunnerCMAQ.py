#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 19:02:01 2022

@author: leohoinaski
"""

import argparse

def writeMCIPscript(CMAQHome,wrf_dir,GDNAM,YYYYMMDD,YYYYMMDDend,YESTERDAY,wrfDomain):  
    scriptPath = CMAQHome +'/PREP/mcip/scripts'       
    file1 = open(scriptPath + "/run_mcip.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write('\n#')
    #file1.write('\nset compiler=gcc')
    file1.write('\nset CMAQ_HOME='+CMAQHome)
    file1.write('\nset CMAQ_DATA=$CMAQ_HOME/data')
    file1.write('\nsource $CMAQ_HOME/config_cmaq.csh')
    file1.write('\nset APPL       = '+GDNAM)
    file1.write('\nset CoordName  = Mercator')    # 16-character maximum
    file1.write('\nset GridName   = '+GDNAM)        # 16-character maximum
    file1.write('\nset DataPath   = $CMAQ_DATA')
    file1.write('\nset InMetDir   = '+wrf_dir)
    file1.write('\nset InGeoDir   = '+wrf_dir)
    file1.write('\nset OutDir     = $DataPath/mcip/$GridName')
    file1.write('\nset ProgDir    = $CMAQ_HOME/PREP/mcip/src')
    file1.write('\nset WorkDir    = $OutDir')
    file1.write('\nset InMetFiles = ( $InMetDir/wrfout_d0'+wrfDomain+'_'+YESTERDAY+'_00:00:00 )')
    #file1.write('\nset InMetFiles = ( $InMetDir/wrfout_d02_2019-06-01_00:00:00 )')
    file1.write('\nset IfGeo      = "T"')
    file1.write('\nset InGeoFile  = $InGeoDir/geo_em.d0'+wrfDomain+'.nc')
    file1.write('\nset LPV     = 1')
    file1.write('\nset LWOUT   = 1')
    file1.write('\nset LUVBOUT = 1')
    file1.write('\nset MCIP_START = '+YYYYMMDD+'-00:00:00.0000')  # [UTC]
    file1.write('\nset MCIP_END   = '+YYYYMMDDend+'-00:00:00.0000')  # [UTC]
    file1.write('\nset INTVL      = 60 # [min]')
    file1.write('\nset IOFORM = 1')    
    file1.write('\nset BTRIM = 0')
    str1 ='\nset X0    =  13\
\nset Y0    =  94\
\nset NCOLS =  89\
\nset NROWS = 104\
\nset LPRT_COL = 0\
\nset LPRT_ROW = 0\
\nset WRF_LC_REF_LAT = -999.0\
\nset PROG = mcip\
\ndate\
\nif ( ! -d $InMetDir ) then\
\n  echo "No such input directory $InMetDir"\
\n  exit 1\
\nendif\
\n\
\nif ( ! -d $OutDir ) then\
\n  echo "No such output directory...will try to create one"\
\n  mkdir -p $OutDir\
\n  if ( $status != 0 ) then\
\n    echo "Failed to make output directory, $OutDir"\
\n    exit 1\
\n  endif\
\nendif\
\nif ( ! -d $ProgDir ) then\
\n  echo "No such program directory $ProgDir"\
\n  exit 1\
\nendif\
\nif ( $IfGeo == "T" ) then\
\n  if ( ! -f $InGeoFile ) then\
\n    echo "No such input file $InGeoFile"\
\n    exit 1\
\n  endif\
\nendif\
\n\
\nforeach fil ( $InMetFiles )\
\n  if ( ! -f $fil ) then\
\n    echo "No such input file $fil"\
\n    exit 1\
\n  endif\
\nend\
\n#-------------------------------------------------------------------->\
\n# Make sure the executable exists.\
\n#-------------------------------------------------------------------->\
\n\
\nif ( ! -f $ProgDir/${PROG}.exe ) then\
\n  echo "Could not find ${PROG}.exe"\
\n  exit 1\
\nendif\
\n#-------------------------------------------------------------------->\
\n# Create a work directory for this job.\
\n#-------------------------------------------------------------------->\
\n\
\nif ( ! -d $WorkDir ) then\
\n  mkdir -p $WorkDir\
\n  if ( $status != 0 ) then\
\n    echo "Failed to make work directory, $WorkDir"\
\n    exit 1\
\n  endif\
\nendif\
\n\
\ncd $WorkDir\
\n#-------------------------------------------------------------------->\
\n# Set up script variables for input files.\
\n#-------------------------------------------------------------------->\
\n\
\nif ( $IfGeo == "T" ) then\
\n  if ( -f $InGeoFile ) then\
\n    set InGeo = $InGeoFile\
\n  else\
\n    set InGeo = "no_file"\
\n  endif\
\nelse\
\n  set InGeo = "no_file"\
\nendif\
\n\
\nset FILE_GD  = $OutDir/GRIDDESC\
\n\
\n#-------------------------------------------------------------------->\
\n# Create namelist with user definitions.\
\n#----------------------------------------\
\nset MACHTYPE = `uname`\
\nif ( ( $MACHTYPE == "AIX" ) || ( $MACHTYPE == "Darwin" ) ) then\
\n  set Marker = "/"\
\nelse\
\n  set Marker = "&END"\
\nendif\
\n\
\ncat > $WorkDir/namelist.${PROG} << !\
\n\
\n &FILENAMES\
\n  file_gd    = "$FILE_GD"\
\n  file_mm    = "$InMetFiles[1]",\
\n!\
\n\
\nif ( $#InMetFiles > 1 ) then\
\n  @ nn = 2\
\n  while ( $nn <= $#InMetFiles )\
\n    cat >> $WorkDir/namelist.${PROG} << !\
\n               "$InMetFiles[$nn]",\
\n!\
\n    @ nn ++\
\n  end\
\nendif\
\n\
\nif ( $IfGeo == "T" ) then\
\ncat >> $WorkDir/namelist.${PROG} << !\
\n  file_geo   = "$InGeo"\
\n!\
\nendif\
\ncat >> $WorkDir/namelist.${PROG} << !\
\n  ioform     =  $IOFORM\
\n $Marker\
\n\
\n &USERDEFS\
\n  lpv        =  $LPV\
\n  lwout      =  $LWOUT\
\n  luvbout    =  $LUVBOUT\
\n  mcip_start = "$MCIP_START"\
\n  mcip_end   = "$MCIP_END"\
\n  intvl      =  $INTVL\
\n  coordnam   = "$CoordName"\
\n  grdnam     = "$GridName"\
\n  btrim      =  $BTRIM\
\n  lprt_col   =  $LPRT_COL\
\n  lprt_row   =  $LPRT_ROW\
\n  wrf_lc_ref_lat = $WRF_LC_REF_LAT\
\n $Marker\
\n\
\n &WINDOWDEFS\
\n  x0         =  $X0\
\n  y0         =  $Y0\
\n  ncolsin    =  $NCOLS\
\n  nrowsin    =  $NROWS\
\n $Marker\
\n\
\n!\
\n#-------------------------------------------------------------------->\
\n# Set links to FORTRAN units.\
\n#-------------------------------------------------------------------->\
\n\
\nrm fort.*\
\nif ( -f $FILE_GD ) rm -f $FILE_GD\
\n\
\nln -s $FILE_GD                   fort.4\
\nln -s $WorkDir/namelist.${PROG}  fort.8\
\n\
\nset NUMFIL = 0\
\nforeach fil ( $InMetFiles )\
\n  @ NN = $NUMFIL + 10\
\n  ln -s $fil fort.$NN\
\n  @ NUMFIL ++\
\nend\
\n\
\n#-------------------------------------------------------------------->\
\n# Set output file names and other miscellaneous environment variables.\
\n#-------------------------------------------------------------------->\
\n\
\nsetenv IOAPI_CHECK_HEADERS  T\
\nsetenv EXECUTION_ID         $PROG\
\n\
\nsetenv GRID_BDY_2D          $OutDir/GRIDBDY2D_${APPL}.nc\
\nsetenv GRID_CRO_2D          $OutDir/GRIDCRO2D_${APPL}.nc\
\nsetenv GRID_DOT_2D          $OutDir/GRIDDOT2D_${APPL}.nc\
\nsetenv MET_BDY_3D           $OutDir/METBDY3D_${APPL}.nc\
\nsetenv MET_CRO_2D           $OutDir/METCRO2D_${APPL}.nc\
\nsetenv MET_CRO_3D           $OutDir/METCRO3D_${APPL}.nc\
\nsetenv MET_DOT_3D           $OutDir/METDOT3D_${APPL}.nc\
\nsetenv LUFRAC_CRO           $OutDir/LUFRAC_CRO_${APPL}.nc\
\nsetenv SOI_CRO              $OutDir/SOI_CRO_${APPL}.nc\
\nsetenv MOSAIC_CRO           $OutDir/MOSAIC_CRO_${APPL}.nc\
\nif ( -f $GRID_BDY_2D ) rm -f $GRID_BDY_2D\
\nif ( -f $GRID_CRO_2D ) rm -f $GRID_CRO_2D\
\nif ( -f $GRID_DOT_2D ) rm -f $GRID_DOT_2D\
\nif ( -f $MET_BDY_3D  ) rm -f $MET_BDY_3D\
\nif ( -f $MET_CRO_2D  ) rm -f $MET_CRO_2D\
\nif ( -f $MET_CRO_3D  ) rm -f $MET_CRO_3D\
\nif ( -f $MET_DOT_3D  ) rm -f $MET_DOT_3D\
\nif ( -f $LUFRAC_CRO  ) rm -f $LUFRAC_CRO\
\nif ( -f $SOI_CRO     ) rm -f $SOI_CRO\
\nif ( -f $MOSAIC_CRO  ) rm -f $MOSAIC_CRO\
\n\
\nif ( -f $OutDir/mcip.nc      ) rm -f $OutDir/mcip.nc\
\nif ( -f $OutDir/mcip_bdy.nc  ) rm -f $OutDir/mcip_bdy.nc\
\n\
\n#-------------------------------------------------------------------->\
\n# Execute MCIP.\
\n#-------------------------------------------------------------------->\
\n\
\n$ProgDir/${PROG}.exe\
\n\
\nif ( $status == 0 ) then\
\n  rm fort.*\
\n  exit 0\
\nelse\
\n  echo "Error running $PROG"\
\n  exit 1\
\nendif\
\n'
    file1.write(str1)
    file1.close()
    return file1

def writeICONscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD):  
    scriptPath = CMAQHome +'/PREP/icon/scripts'       
    file1 = open(scriptPath + "/run_icon.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write('\n')
    
    str1 = '\n# ======================= ICONv5.3.X Run Script ========================\
\n# Usage: run.icon.csh >&! icon.log &       \
\n#\
\n# To report problems or request help with this script/program:  \
\n#             http://www.cmascenter.org\
\n# ==================================================================== \
\n\
\n# ==================================================================\
\n#> Runtime Environment Options\
\n# ==================================================================\
\n\
\n#> Choose compiler and set up CMAQ environment with correct \
\n#> libraries using config.cmaq. Options: intel | gcc | pgi\
\n setenv compiler gcc \
\n\
\n#> Source the config_cmaq file to set the run environment\
\n pushd ../../../\
\n source ./config_cmaq.csh $compiler\
\n popd\
\n\
\n#> Check that CMAQ_DATA is set:\
\n if ( ! -e $CMAQ_DATA ) then\
\n    echo "   $CMAQ_DATA path does not exist"\
\n    exit 1\
\n endif\
\n echo " "; echo " Input data path, CMAQ_DATA set to $CMAQ_DATA"; echo " "\
\n\
\n#> Set General Parameters for Configuring the Simulation\
\n set VRSN     = v532                    #> Code Version\
\n set APPL     = '+GDNAM+'             #> Application Name\
\n set ICTYPE   = profile                  #> Initial conditions type [profile|regrid]\
\n\
\n#> Set the working directory:\
\n set BLD      = ${CMAQ_HOME}/PREP/icon/scripts/BLD_ICON_${VRSN}_${compilerString}\
\n set EXEC     = ICON_${VRSN}.exe  \
\n cat $BLD/ICON_${VRSN}.cfg; echo " "; set echo\
\n\
\n#> Horizontal grid definition \
\n setenv GRID_NAME '+GDNAM+'                #> check GRIDDESC file for GRID_NAME options\
\n setenv GRIDDESC '+mcipPath+'/GRIDDESC\
\n setenv IOAPI_ISPH 20                     #> GCTP spheroid, use 20 for WRF-based modeling\
\n\
\n#> I/O Controls\
\n setenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]\
\n setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]\
\n setenv EXECUTION_ID $EXEC    #> define the model execution id\
\n\
\n# =====================================================================\
\n#> ICON Configuration Options\
\n#\
\n# ICON can be run in one of two modes:                                     \
\n#     1) regrids CMAQ CTM concentration files (IC type = regrid)     \
\n#     2) use default profile inputs (IC type = profile)\
\n# =====================================================================\
\n\
\n setenv ICON_TYPE ` echo $ICTYPE | tr "[A-Z]" "[a-z]" ` \
\n\
\n# =====================================================================\
\n#> Input/Output Directories\
\n# =====================================================================\
\n\
\n set OUTDIR   = $CMAQ_HOME/data/icon       #> output file directory\
\n\
\n# =====================================================================\
\n#> Input Files\
\n#  \
\n#  Regrid mode (IC = regrid) (includes nested domains, windowed domains,\
\n#                             or general regridded domains)\
\n#     CTM_CONC_1 = the CTM concentration file for the coarse doma \
\n#     MET_CRO_3D_CRS = the MET_CRO_3D met file for the coarse domain \
\n#     MET_CRO_3D_FIN = the MET_CRO_3D met file for the target nested domain \
\n#\
\n#  Profile Mode (IC = profile) \
\n#     IC_PROFILE = static/default IC profiles \
\n#     MET_CRO_3D_FIN = the MET_CRO_3D met file for the target domain \
\n#\
\n# NOTE: SDATE (yyyyddd) and STIME (hhmmss) are only relevant to the\
\n#       regrid mode and if they are not set, these variables will \
\n#       be set from the input MET_CRO_3D_FIN file\
\n# =====================================================================\
\n#> Output File\
\n#     INIT_CONC_1 = gridded IC file for target domain\
\n# =====================================================================\
\n\
\n    set DATE = "'+YYYYMMDD+'" # 2019-06-02 \
\n   set YYYYJJJ  = `date -ud "${DATE}" +%Y%j`   #> Convert YYYY-MM-DD to YYYYJJJ\
\n   set YYMMDD   = `date -ud "${DATE}" +%y%m%d` #> Convert YYYY-MM-DD to YYMMDD\
\n    set YYYYMMDD = `date -ud "${DATE}" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD\
\n#   setenv SDATE           ${YYYYJJJ}\
\n#   setenv STIME           000000\
\n\
\n if ( $ICON_TYPE == regrid ) then\
\n    setenv CTM_CONC_1 /work/MOD3EVAL/sjr/CCTM_CONC_v53_intel18.0_2016_CONUS_test_${YYYYMMDD}.nc\
\n    setenv MET_CRO_3D_CRS /work/MOD3DATA/2016_12US1/met/mcip_v43_wrf_v381_ltng/METCRO3D.12US1.35L.${YYMMDD}\
\n    setenv MET_CRO_3D_FIN /work/MOD3DATA/SE53BENCH/met/mcip/METCRO3D_${YYMMDD}.nc\
\n    setenv INIT_CONC_1    "$OUTDIR/ICON_${VRSN}_${APPL}_${ICON_TYPE}_${YYYYMMDD} -v"\
\n endif\
\n\
\n if ( $ICON_TYPE == profile ) then\
\n    setenv IC_PROFILE $BLD/avprofile_cb6r3m_ae7_kmtbr_hemi2016_v53beta2_m3dry_col051_row068.csv\
\n    # setenv MET_CRO_3D_FIN /work/MOD3DATA/SE53BENCH/met/mcip/METCRO3D_${YYMMDD}.nc\
\n    setenv MET_CRO_3D_FIN '+mcipPath+'/METCRO3D_$GRID_NAME.nc\
\n    setenv INIT_CONC_1    "$OUTDIR/ICON_${VRSN}_${APPL}_${ICON_TYPE}_${YYYYMMDD} -v"\
\n endif\
\n \
\n#>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\
\n\
\n if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR\
\n\
\n ls -l $BLD/$EXEC; size $BLD/$EXEC\
\n# unlimit\
\n limit\
\n\
\n#> Executable call:\
\n time $BLD/$EXEC\
\n\
\n exit() \
\n'
    file1.write(str1)
    file1.close()
    return file1

def writeBCONscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD):  
    scriptPath = CMAQHome +'/PREP/bcon/scripts'       
    file1 = open(scriptPath + "/run_bcon.csh","w") 
    file1.write('#! /bin/csh -f')
    file1.write('\n')
    str1='\n# ======================= BCONv5.3.X Run Script ======================== \
\n# Usage: run.bcon.csh >&! bcon.log & \
\n#\
\n# To report problems or request help with this script/program:        \
\n#             http://www.cmascenter.org\
\n# ==================================================================== \
\n\
\n# ==================================================================\
\n#> Runtime Environment Options\
\n# ==================================================================\
\n\
\n#> Choose compiler and set up CMAQ environment with correct \
\n#> libraries using config.cmaq. Options: intel | gcc | pgi\
\n setenv compiler gcc \
\n\
\n#> Source the config_cmaq file to set the run environment\
\n pushd ../../../\
\n source ./config_cmaq.csh $compiler\
\n popd\
\n\
\n#> Check that CMAQ_DATA is set:\
\n if ( ! -e $CMAQ_DATA ) then\
\n    echo "   $CMAQ_DATA path does not exist"\
\n    exit 1\
\n endif\
\n echo " "; echo " Input data path, CMAQ_DATA set to $CMAQ_DATA"; echo " "\
\n\
\n#> Set General Parameters for Configuring the Simulation\
\n set VRSN     = v532                    #> Code Version\
\n set APPL     = '+GDNAM+'              #> Application Name\
\n set BCTYPE   = profile                  #> Boundary condition type [profile|regrid]\
\n\
\n#> Set the build directory:\
\n set BLD      = ${CMAQ_HOME}/PREP/bcon/scripts/BLD_BCON_${VRSN}_${compilerString}\
\n set EXEC     = BCON_${VRSN}.exe  \
\n cat $BLD/BCON_${VRSN}.cfg; echo " "; set echo\
\n\
\n#> Horizontal grid definition \
\n setenv GRID_NAME '+GDNAM+'               #> check GRIDDESC file for GRID_NAME options\
\n#setenv GRIDDESC $CMAQ_DATA/$APPL/met/mcip/GRIDDESC #> grid description file \
\n setenv GRIDDESC '+mcipPath+'/GRIDDESC\
\n setenv IOAPI_ISPH 20                     #> GCTP spheroid, use 20 for WRF-based modeling\
\n\
\n#> I/O Controls\
\n setenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]\
\n setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]\
\n setenv EXECUTION_ID $EXEC    #> define the model execution id\
\n\
\n# =====================================================================\
\n#> BCON Configuration Options\
\n#\
\n# BCON can be run in one of two modes:                                     \
\n#     1) regrids CMAQ CTM concentration files (BC type = regrid)     \
\n#     2) use default profile inputs (BC type = profile)\
\n# =====================================================================\
\n\
\n setenv BCON_TYPE ` echo $BCTYPE | tr "[A-Z]" "[a-z]" `\
\n\
\n# =====================================================================\
\n#> Input/Output Directories\
\n# =====================================================================\
\n\
\n set OUTDIR   = $CMAQ_HOME/data/bcon       #> output file directory\
\n\
\n# =====================================================================\
\n#> Input Files\
\n#  \
\n#  Regrid mode (BC = regrid) (includes nested domains, windowed domains,\
\n#                             or general regridded domains)\
\n#     CTM_CONC_1 = the CTM concentration file for the coarse domain          \
\n#     MET_CRO_3D_CRS = the MET_CRO_3D met file for the coarse domain\
\n#     MET_BDY_3D_FIN = the MET_BDY_3D met file for the target nested domain\
\n#                                                                            \
\n#  Profile mode (BC type = profile)\
\n#     BC_PROFILE = static/default BC profiles \
\n#     MET_BDY_3D_FIN = the MET_BDY_3D met file for the target domain \
\n#\
    \
\n# NOTE: SDATE (yyyyddd), STIME (hhmmss) and RUNLEN (hhmmss) are only \
\n#       relevant to the regrid mode and if they are not set,  \
\n#       these variables will be set from the input MET_BDY_3D_FIN file\
\n# =====================================================================\
\n#> Output File\n#     BNDY_CONC_1 = gridded BC file for target domain\
\n# =====================================================================\
\n \
\n    set DATE = "'+YYYYMMDD+'"\
\n    set YYYYJJJ  = `date -ud "${DATE}" +%Y%j`   #> Convert YYYY-MM-DD to YYYYJJJ\
\n    set YYMMDD   = `date -ud "${DATE}" +%y%m%d` #> Convert YYYY-MM-DD to YYMMDD\
\n    set YYYYMMDD = `date -ud "${DATE}" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD\
\n#   setenv SDATE           ${YYYYJJJ}\
\n#   setenv STIME           000000\
\n#   setenv RUNLEN          240000\
\n\
\n if ( $BCON_TYPE == regrid ) then \
\n    setenv CTM_CONC_1 /work/MOD3EVAL/sjr/CCTM_CONC_v53_intel18.0_2016_CONUS_test_${YYYYMMDD}.nc\
\n    setenv MET_CRO_3D_CRS /work/MOD3DATA/2016_12US1/met/mcip_v43_wrf_v381_ltng/METCRO3D.12US1.35L.${YYMMDD}\
\n    setenv MET_BDY_3D_FIN /work/MOD3DATA/SE53BENCH/met/mcip/METBDY3D_${YYMMDD}.nc\
\n    setenv BNDY_CONC_1    "$OUTDIR/BCON_${VRSN}_${APPL}_${BCON_TYPE}_${YYYYMMDD} -v"\
\n endif\
\n\
\n if ( $BCON_TYPE == profile ) then\
\n    setenv BC_PROFILE $BLD/avprofile_cb6r3m_ae7_kmtbr_hemi2016_v53beta2_m3dry_col051_row068.csv\
\n    setenv MET_BDY_3D_FIN '+mcipPath+'/METBDY3D_$GRID_NAME.nc\
\n    setenv BNDY_CONC_1    "$OUTDIR/BCON_${VRSN}_${APPL}_${BCON_TYPE}_${YYYYMMDD} -v"\
\n endif\
\n\
\n# =====================================================================\
\n#> Output File\
\n# =====================================================================\
\n \
\n#>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\
\n\
\n if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR\
\n\
\n ls -l $BLD/$EXEC; size $BLD/$EXEC\
\n# unlimit\
\n limit\
\n\
\n#> Executable call:\
\n time $BLD/$EXEC\
\n\
\n exit() '
    file1.write(str1)
    file1.close()
    return file1

def writeCCTMscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD,YYYYMMDDend,NPCOL,NPROW,NLAYS,NEW_START,YYYYMMDDi):  
    scriptPath = CMAQHome +'/CCTM/scripts'       
    file1 = open(scriptPath + "/run_cctm.csh","w") 
    str1="#!/bin/csh -f\
\n\
\n# ===================== CCTMv5.3.X Run Script ========================= \
\n# Usage: run.cctm >&! cctm_Bench_2016_12SE1.log &                               \
\n#\
\n# To report problems or request help with this script/program:     \
\n#             http://www.epa.gov/cmaq    (EPA CMAQ Website)\
\n#             http://www.cmascenter.org  (CMAS Website)\
\n# ===================================================================  \
\n\
\n# ===================================================================\
\n#> Runtime Environment Options\
\n# ===================================================================\
\n\
\necho 'Start Model Run At ' `date`\
\n\
\n#> Toggle Diagnostic Mode which will print verbose information to \
\n#> standard output\
\n setenv CTM_DIAG_LVL 0\
\n\
\n#> Choose compiler and set up CMAQ environment with correct \
\n#> libraries using config.cmaq. Options: intel | gcc | pgi\
\n if ( ! $?compiler ) then\
\n   setenv compiler gcc\
\n endif\
\n if ( ! $?compilerVrsn ) then\
\n   setenv compilerVrsn Empty\
\n endif\
\n\
\n#> Source the config.cmaq file to set the build environment\
\n cd ../..\
\n source ./config_cmaq.csh $compiler \
\n cd CCTM/scripts\
\n\
\n#> Set General Parameters for Configuring the Simulation\
\n set VRSN      = v532              #> Code Version\
\n set PROC      = mpi               #> serial or mpi\
\n set MECH      = cb6r3_ae7_aq      #> Mechanism ID\
\n set APPL      = "+GDNAM+"  #> Application Name (e.g. Gridname)\
\n                                                       \
\n#> Define RUNID as any combination of parameters above or others. By default,\
\n#> this information will be collected into this one string, $RUNID, for easy\
\n#> referencing in output binaries and log files as well as in other scripts.\
\n setenv RUNID  ${VRSN}_${compilerString}_${APPL}\
\n\
\n#> Set the build directory (this is where the CMAQ executable\
\n#> is located by default).\
\n set BLD       = ${CMAQ_HOME}/CCTM/scripts/BLD_CCTM_${VRSN}_${compilerString}\
\n set EXEC      = CCTM_${VRSN}.exe  \
\n\
\n#> Output Each line of Runscript to Log File\
\n if ( $CTM_DIAG_LVL != 0 ) set echo \
\n\
\n#> Set Working, Input, and Output Directories\
\n setenv WORKDIR ${CMAQ_HOME}/CCTM/scripts          #> Working Directory. Where the runscript is.\
\n setenv OUTDIR  ${CMAQ_DATA}/output_CCTM_${RUNID}  #> Output Directory\
\n setenv INPDIR  ${CMAQ_DATA}/inputs/"+GDNAM+"            #> Input Directory\
\n setenv LOGDIR  ${OUTDIR}/LOGS     #> Log Directory Location\
\n setenv NMLpath ${BLD}             #> Location of Namelists. Common places are: \
\n                                   #>   ${WORKDIR} | ${CCTM_SRC}/MECHS/${MECH} | ${BLD}\
\n\
\n echo "+'""'+"\
\n echo "+'"Working Directory is $WORKDIR"'+"\
\n echo "+'"Build Directory is $BLD"'+"\
\n echo "+'"Output Directory is $OUTDIR"'+"\
\n echo "+'"Log Directory is $LOGDIR"'+"\
\n echo "+'"Executable Name is $EXEC"'+"\
\n\
\n# =====================================================================\
\n#> CCTM Configuration Options\
\n# =====================================================================\
\n\
\n#> Set Start and End Days for looping\
\n setenv NEW_START "+NEW_START+"             #> Set to FALSE for model restart\
\n set START_DATE = "+'"'+YYYYMMDD+'"'+"     #> beginning date (July 1, 2016)\
\n set END_DATE   = "+'"'+YYYYMMDDend+'"'+"     #> ending date    (July 1, 2016)\
\n\
\n#> Set Timestepping Parameters\
\nset STTIME     = 000000            #> beginning GMT time (HHMMSS)\
\nset NSTEPS     = 240000            #> time duration (HHMMSS) for this run\
\nset TSTEP      = 010000            #> output time step interval (HHMMSS)\
\n\
\n#> Horizontal domain decomposition\
\nif ( $PROC == serial ) then\
\n   setenv NPCOL_NPROW "+'"1 1"'+"; set NPROCS   = 1 # single processor setting\
\nelse\
\n   @ NPCOL  =  "+NPCOL+"; @ NPROW =  "+NPROW+"\
\n   @ NPROCS = $NPCOL * $NPROW\
\n   setenv NPCOL_NPROW "+'"$NPCOL $NPROW"'+"; \
\nendif\
\n\
\n#   @ NPROCS = \
\n\
\n#> Define Execution ID: e.g. [CMAQ-Version-Info]_[User]_[Date]_[Time]\
\nsetenv EXECUTION_ID "+'"CMAQ_CCTM${VRSN}_`id -u -n`_`date -u +%Y%m%d_%H%M%S_%N`"'+"    #> Inform IO/API of the Execution ID\
\necho "+'""'+"\
\necho "+'"---CMAQ EXECUTION ID: $EXECUTION_ID ---"'+"\
\n\
\n#> Keep or Delete Existing Output Files\
\nset CLOBBER_DATA = TRUE \
\n\
\n#> Logfile Options\
\n#> Master Log File Name; uncomment to write standard output to a log, otherwise write to screen\
\n#setenv LOGFILE $CMAQ_HOME/$RUNID.log  \
\nif (! -e $LOGDIR ) then\
\n  mkdir -p $LOGDIR\
\nendif\
\nsetenv PRINT_PROC_TIME Y           #> Print timing for all science subprocesses to Logfile\
\n                                   #>   [ default: TRUE or Y ]\
\nsetenv STDOUT T                    #> Override I/O-API trying to write information to both the processor \
\n                                   #>   logs and STDOUT [ options: T | F ]\
\n\
\nsetenv GRID_NAME "+GDNAM+"         #> check GRIDDESC file for GRID_NAME options\
\nsetenv GRIDDESC ${CMAQ_HOME}/data/mcip/${APPL}/GRIDDESC    #> grid description file\
\n\
\n#> Retrieve the number of columns, rows, and layers in this simulation\
\nset NZ = "+NLAYS+"\
\nset NX = `grep -A 1 ${GRID_NAME} ${GRIDDESC} | tail -1 | sed 's/  */ /g' | cut -d' ' -f6`\
\nset NY = `grep -A 1 ${GRID_NAME} ${GRIDDESC} | tail -1 | sed 's/  */ /g' | cut -d' ' -f7`\
\nset NCELLS = `echo "+'"${NX} * ${NY} * ${NZ}"'+" | bc -l`\
\n\
\n#> Output Species and Layer Options\
\n   #> CONC file species; comment or set to 'ALL' to write all species to CONC\
\n   setenv CONC_SPCS "+'"ALL"'+"\
\n   setenv CONC_BLEV_ELEV "+'" 1 1"'+" #> CONC file layer range; comment to write all layers to CONC\
\n\
\n   #> ACONC file species; comment or set to 'ALL' to write all species to ACONC\
\n   setenv AVG_CONC_SPCS "+'"O3 NO CO NO2 ASO4I ASO4J NH3 SO2"'+" \
\n   setenv ACONC_BLEV_ELEV "+'" 1 1"'+" #> ACONC file layer range; comment to write all layers to ACONC\
\n   setenv AVG_FILE_ENDTIME N     #> override default beginning ACONC timestamp [ default: N ]\
\n\
\n#> Synchronization Time Step and Tolerance Options\
\nsetenv CTM_MAXSYNC 300       #> max sync time step (sec) [ default: 720 ]\
\nsetenv CTM_MINSYNC  60       #> min sync time step (sec) [ default: 60 ]\
\nsetenv SIGMA_SYNC_TOP 0.7    #> top sigma level thru which sync step determined [ default: 0.7 ] \
\n#setenv ADV_HDIV_LIM 0.95    #> maximum horiz. div. limit for adv step adjust [ default: 0.9 ]\
\nsetenv CTM_ADV_CFL 0.95      #> max CFL [ default: 0.75]\
\n#setenv RB_ATOL 1.0E-09      #> global ROS3 solver absolute tolerance [ default: 1.0E-07 ] \
\n\
\n#> Science Options\
\nsetenv CTM_OCEAN_CHEM Y      #> Flag for ocean halgoen chemistry and sea spray aerosol emissions [ default: Y ]\
\nsetenv CTM_WB_DUST N         #> use inline windblown dust emissions [ default: Y ]\
\nsetenv CTM_WBDUST_BELD BELD3 #> landuse database for identifying dust source regions \
\n                             #>    [ default: UNKNOWN ]; ignore if CTM_WB_DUST = N \
\nsetenv CTM_LTNG_NO N         #> turn on lightning NOx [ default: N ]\
\nsetenv KZMIN Y               #> use Min Kz option in edyintb [ default: Y ], \
\n                             #>    otherwise revert to Kz0UT\
\nsetenv CTM_MOSAIC N          #> landuse specific deposition velocities [ default: N ]\
\nsetenv CTM_FST N             #> mosaic method to get land-use specific stomatal flux \
\n                             #>    [ default: N ]\
\nsetenv PX_VERSION Y          #> WRF PX LSM\
\nsetenv CLM_VERSION N         #> WRF CLM LSM\
\nsetenv NOAH_VERSION N        #> WRF NOAH LSM\
\nsetenv CTM_ABFLUX N          #> ammonia bi-directional flux for in-line deposition \
\n                             #>    velocities [ default: N ]\
\nsetenv CTM_BIDI_FERT_NH3 N   #> subtract fertilizer NH3 from emissions because it will be handled\
\n                             #>    by the BiDi calculation [ default: Y ]\
\nsetenv CTM_HGBIDI N          #> mercury bi-directional flux for in-line deposition \
\n                             #>    velocities [ default: N ]\
\nsetenv CTM_SFC_HONO Y        #> surface HONO interaction [ default: Y ]\
\nsetenv CTM_GRAV_SETL Y       #> vdiff aerosol gravitational sedimentation [ default: Y ]\
\nsetenv CTM_BIOGEMIS N        #> calculate in-line biogenic emissions [ default: N ]\
\n\
\n#> Vertical Extraction Options\
\nsetenv VERTEXT N\
\nsetenv VERTEXT_COORD_PATH ${WORKDIR}/lonlat.csv\
\n\
\n#> I/O Controls\
\nsetenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]\
\nsetenv FL_ERR_STOP N         #> stop on inconsistent input files\
\nsetenv PROMPTFLAG F          #> turn on I/O-API PROMPT*FILE interactive mode [ options: T | F ]\
\nsetenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]\
\nsetenv IOAPI_CHECK_HEADERS N #> check file headers [ options: Y | N ]\
\nsetenv CTM_EMISCHK N         #> Abort CMAQ if missing surrogates from emissions Input files\
\nsetenv EMISDIAG N            #> Print Emission Rates at the output time step after they have been\
\n                             #>   scaled and modified by the user Rules [options: F | T or 2D | 3D | 2DSUM ]\
\n                             #>   Individual streams can be modified using the variables:\
\n                             #>       GR_EMIS_DIAG_## | STK_EMIS_DIAG_## | BIOG_EMIS_DIAG\
\n                             #>       MG_EMIS_DIAG    | LTNG_EMIS_DIAG   | DUST_EMIS_DIAG\
\n                             #>       SEASPRAY_EMIS_DIAG   \
\n                             #>   Note that these diagnostics are different than other emissions diagnostic\
\n                             #>   output because they occur after scaling.\
\nsetenv EMISDIAG_SUM F        #> Print Sum of Emission Rates to Gridded Diagnostic File\
\n\
\n#> Diagnostic Output Flags\
\nsetenv CTM_CKSUM N           #> checksum report [ default: Y ]\
\nsetenv CLD_DIAG N            #> cloud diagnostic file [ default: N ]\
\n\
\nsetenv CTM_PHOTDIAG N        #> photolysis diagnostic file [ default: N ]\
\nsetenv NLAYS_PHOTDIAG "+'"1"'+"    #> Number of layers for PHOTDIAG2 and PHOTDIAG3 from \
\n                             #>     Layer 1 to NLAYS_PHOTDIAG  [ default: all layers ] \
\n#setenv NWAVE_PHOTDIAG "+'"294 303 310 316 333 381 607"'+"  #> Wavelengths written for variables\
\n                                                      #>   in PHOTDIAG2 and PHOTDIAG3 \
\n                                                      #>   [ default: all wavelengths ]\
\n\
\nsetenv CTM_PMDIAG N          #> Instantaneous Aerosol Diagnostic File [ default: Y ]\
\nsetenv CTM_APMDIAG N         #> Hourly-Average Aerosol Diagnostic File [ default: Y ]\
\nsetenv APMDIAG_BLEV_ELEV "+'"1 1"'+"  #> layer range for average pmdiag = NLAYS\
\n\
\nsetenv CTM_SSEMDIAG N        #> sea-spray emissions diagnostic file [ default: N ]\
\nsetenv CTM_DUSTEM_DIAG N     #> windblown dust emissions diagnostic file [ default: N ]; \
\n                             #>     Ignore if CTM_WB_DUST = N\
\nsetenv CTM_DEPV_FILE N       #> deposition velocities diagnostic file [ default: N ]\
\nsetenv VDIFF_DIAG_FILE N     #> vdiff & possibly aero grav. sedimentation diagnostic file [ default: N ]\
\nsetenv LTNGDIAG N            #> lightning diagnostic file [ default: N ]\
\nsetenv B3GTS_DIAG N          #> BEIS mass emissions diagnostic file [ default: N ]\
\nsetenv CTM_WVEL N            #> save derived vertical velocity component to conc \
\n                             #>    file [ default: Y ]\
\n\
\n# =====================================================================\
\n#> Input Directories and Filenames\
\n# =====================================================================\
\n\
\nset ICpath    = ${CMAQ_HOME}/data/icon                        #> initial conditions input directory \
\nset BCpath    = ${CMAQ_HOME}/data/bcon                        #> boundary conditions input directory\
\nset EMISpath  = $INPDIR   #> gridded emissions input directory\
\nset EMISpath2 = #$INPDIR/emis/gridded_area/rwc       #> gridded surface residential wood combustion emissions directory\
\nset IN_PTpath = #$INPDIR/emis/inln_point             #> point source emissions input directory\
\nset IN_LTpath = #$INPDIR/lightning                   #> lightning NOx input directory\
\nset METpath   = ${CMAQ_HOME}/data/mcip/${APPL}              #> meteorology input directory \
\n#set JVALpath  = $INPDIR/jproc                      #> offline photolysis rate table directory\
\nset OMIpath   = $BLD                                #> ozone column data for the photolysis model\
\nset LUpath    = #$INPDIR/land                        #> BELD landuse data for windblown dust model\
\nset SZpath    = $INPDIR                        #> surf zone file for in-line seaspray emissions\
\n\
\n# =====================================================================\
\n#> Begin Loop Through Simulation Days\
\n# =====================================================================\
\nset rtarray = "+'""'+"\
\n\
\nset TODAYG = ${START_DATE}\
\nset TODAYJ = `date -ud "+'"${START_DATE}"'+" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ\
\nset START_DAY = ${TODAYJ} \
\nset STOP_DAY = `date -ud "+'"${END_DATE}"'+" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ\
\nset NDAYS = 1\
\n\
\nwhile ($TODAYJ <= $STOP_DAY )  #>Compare dates in terms of YYYYJJJ\
\n  \
\n  set NDAYS = `echo "+'"${NDAYS} + 1"'+" | bc -l`\
\n\
\n  #> Retrieve Calendar day Information\
\n  set YYYYMMDD = `date -ud "+'"${TODAYG}"'+" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD\
\n  set YYYYMM = `date -ud "+'"${TODAYG}"'+" +%Y%m`     #> Convert YYYY-MM-DD to YYYYMM\
\n  set YYMMDD = `date -ud "+'"${TODAYG}"'+" +%y%m%d`   #> Convert YYYY-MM-DD to YYMMDD\
\n  set YYYYJJJ = $TODAYJ\
\n\
\n  #> Calculate Yesterday's Date\
\n  set YESTERDAY = `date -ud "'"${TODAYG}-1days"'+" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYJJJ\
\n\
\n# =====================================================================\
\n#> Set Output String and Propagate Model Configuration Documentation\
\n# =====================================================================\
\n  echo "+'""'+"\
\n  echo "+'"Set up input and output files for Day ${TODAYG}."'+"\
\n\
\n  #> set output file name extensions\
\n  setenv CTM_APPL ${RUNID}_${YYYYMMDD} \
\n  \
\n  #> Copy Model Configuration To Output Folder\
\n  if ( ! -d "+'"$OUTDIR"'+" ) mkdir -p $OUTDIR\
\n  cp $BLD/CCTM_${VRSN}.cfg $OUTDIR/CCTM_${CTM_APPL}.cfg\
\n\
\n# =====================================================================\
\n#> Input Files (Some are Day-Dependent)\
\n# =====================================================================\
\n\
\n  #> Initial conditions\
\n  if ($NEW_START == true || $NEW_START == TRUE ) then\
\n     setenv ICFILE ICON_v532_"+GDNAM+"_profile_"+YYYYMMDDi+"\
\n     setenv INIT_MEDC_1 notused\
\n     setenv INITIAL_RUN Y #related to restart soil information file\
\n  else\
\n     set ICpath = $OUTDIR\
\n     setenv ICFILE CCTM_CGRID_${RUNID}_${YESTERDAY}.nc\
\n     setenv INIT_MEDC_1 $ICpath/CCTM_MEDIA_CONC_${RUNID}_${YESTERDAY}.nc\
\n     setenv INITIAL_RUN N\
\n  endif\
\n\
\n  #> Boundary conditions\
\n  set BCFILE = BCON_v532_"+GDNAM+"_profile_"+YYYYMMDDi+"\
\n\
\n  #> Off-line photolysis rates \
\n  #set JVALfile  = JTABLE_${YYYYJJJ}\
\n\
\n  #> Ozone column data\
\n  set OMIfile   = OMI_1979_to_2019.dat\
\n\
\n  #> Optics file\
\n  set OPTfile = PHOT_OPTICS.dat\
\n\
\n  #> MCIP meteorology files \
\n  setenv GRID_BDY_2D $METpath/GRIDBDY2D_${APPL}.nc  # GRID files are static, not day-specific\
\n  setenv GRID_CRO_2D $METpath/GRIDCRO2D_${APPL}.nc\
\n  setenv GRID_CRO_3D $METpath/GRIDCRO3D_${APPL}.nc\
\n  setenv GRID_DOT_2D $METpath/GRIDDOT2D_${APPL}.nc\
\n  setenv MET_CRO_2D $METpath/METCRO2D_${APPL}.nc\
\n  setenv MET_CRO_3D $METpath/METCRO3D_${APPL}.nc\
\n  setenv MET_DOT_3D $METpath/METDOT3D_${APPL}.nc\
\n  setenv MET_BDY_3D $METpath/METBDY3D_${APPL}.nc\
\n  setenv LUFRAC_CRO $METpath/LUFRAC_CRO_${APPL}.nc\
\n\
\n  #> Emissions Control File\
\n  #>\
\n  #> IMPORTANT NOTE\
\n  #>\
\n  #> The emissions control file defined below is an integral part of controlling the behavior of the model simulation.\
\n  #> Among other things, it controls the mapping of species in the emission files to chemical species in the model and\
\n  #> several aspects related to the simulation of organic aerosols.\
\n  #> Please carefully review the emissions control file to ensure that it is configured to be consistent with the assumptions\
\n  #> made when creating the emission files defined below and the desired representation of organic aerosols.\
\n  #> For further information, please see:\
\n  #> + AERO7 Release Notes section on 'Required emission updates':\
\n  #>   https://github.com/USEPA/CMAQ/blob/master/DOCS/Release_Notes/aero7_overview.md\
\n  #> + CMAQ User's Guide section 6.9.3 on 'Emission Compatability': \
\n  #>   https://github.com/USEPA/CMAQ/blob/master/DOCS/Users_Guide/CMAQ_UG_ch06_model_configuration_options.md#6.9.3_Emission_Compatability\
\n  #> + Emission Control (DESID) Documentation in the CMAQ User's Guide: \
\n  #>   https://github.com/USEPA/CMAQ/blob/master/DOCS/Users_Guide/Appendix/CMAQ_UG_appendixB_emissions_control.md \
\n  #>\
\n  setenv EMISSCTRL_NML ${BLD}/EmissCtrl_${MECH}.nml\
\n\
\n  #> Spatial Masks For Emissions Scaling\
\n  # setenv CMAQ_MASKS ${EMISpath}/OCEAN #> horizontal grid-dependent surf zone file\
\n\
\n  #> Gridded Emissions Files \
\n  setenv N_EMIS_GR 4\
\n\
\n  set EMISfile  = BRAVESout\
\n  setenv GR_EMIS_001 ${EMISpath}/${EMISfile}\
\n  setenv GR_EMIS_LAB_001 GRIDDED_EMIS\
\n  setenv GR_EM_SYM_DATE_001 F # To change default behaviour please see Users Guide for EMIS_SYM_DATE\
\n\
\n  set EMISfile  = FINNout\
\n  setenv GR_EMIS_002 ${EMISpath}/${EMISfile}\
\n  setenv GR_EMIS_LAB_002 GR_FIRES\
\n  setenv GR_EM_SYM_DATE_002 F # \
\n\
\n  set EMISfile  = MEGANout\
\n  setenv GR_EMIS_003 ${EMISpath}/${EMISfile}\
\n  setenv GR_EMIS_LAB_003 GRIDDED_BIO\
\n  setenv GR_EM_SYM_DATE_003 F #\
\n  setenv GR_EMIS_DIAG_003 F \
\n\
\n  set EMISfile  = INDout\
\n  setenv GR_EMIS_004 ${EMISpath}/${EMISfile}\
\n  setenv GR_EMIS_LAB_004 GRIDDED_IND\
\n  setenv GR_EM_SYM_DATE_004 F #\
\n  setenv GR_EMIS_DIAG_004 F \
\n\
\n#  set EMISfile  = emis_mole_rwc_${YYYYMMDD}_12US1_cmaq_cb6_2016ff_16j.nc\
\n#  setenv GR_EMIS_002 ${EMISpath2}/${EMISfile}\
\n#  setenv GR_EMIS_LAB_002 GR_RES_FIRES\
\n#  setenv GR_EM_SYM_DATE_002 F # To change default behaviour please see Users Guide for EMIS_SYM_DATE\
\n\
\n  #> In-line point emissions configuration\
\n  setenv N_EMIS_PT  0         #> Number of elevated source groups\
\n\
\n  set STKCASEG = 12US1_2016ff_16j           # Stack Group Version Label\
\n  set STKCASEE = 12US1_cmaq_cb6_2016ff_16j  # Stack Emission Version Label\
\n\
\n  # Time-Independent Stack Parameters for Inline Point Sources\
\n  setenv STK_GRPS_001 $IN_PTpath/stack_groups/stack_groups_ptnonipm_${STKCASEG}.nc\
\n  setenv STK_GRPS_002 $IN_PTpath/stack_groups/stack_groups_ptegu_${STKCASEG}.nc\
\n  setenv STK_GRPS_003 $IN_PTpath/stack_groups/stack_groups_othpt_${STKCASEG}.nc\
\n  setenv STK_GRPS_004 $IN_PTpath/stack_groups/stack_groups_ptagfire_${YYYYMMDD}_${STKCASEG}.nc\
\n  setenv STK_GRPS_005 $IN_PTpath/stack_groups/stack_groups_ptfire_${YYYYMMDD}_${STKCASEG}.nc\
\n  setenv STK_GRPS_006 $IN_PTpath/stack_groups/stack_groups_ptfire_othna_${YYYYMMDD}_${STKCASEG}.nc\
\n  setenv STK_GRPS_007 $IN_PTpath/stack_groups/stack_groups_pt_oilgas_${STKCASEG}.nc\
\n  setenv STK_GRPS_008 $IN_PTpath/stack_groups/stack_groups_cmv_c3_${STKCASEG}.nc\
\n\
\n  # Emission Rates for Inline Point Sources\
\n  setenv STK_EMIS_001 $IN_PTpath/ptnonipm/inln_mole_ptnonipm_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_002 $IN_PTpath/ptegu/inln_mole_ptegu_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_003 $IN_PTpath/othpt/inln_mole_othpt_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_004 $IN_PTpath/ptagfire/inln_mole_ptagfire_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_005 $IN_PTpath/ptfire/inln_mole_ptfire_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_006 $IN_PTpath/ptfire_othna/inln_mole_ptfire_othna_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_007 $IN_PTpath/pt_oilgas/inln_mole_pt_oilgas_${YYYYMMDD}_${STKCASEE}.nc\
\n  setenv STK_EMIS_008 $IN_PTpath/cmv_c3/inln_mole_cmv_c3_${YYYYMMDD}_${STKCASEE}.nc\
\n\
\n  # Label Each Emissions Stream\
\n  setenv STK_EMIS_LAB_001 PT_NONEGU\
\n  setenv STK_EMIS_LAB_002 PT_EGU\
\n  setenv STK_EMIS_LAB_003 PT_OTHER\
\n  setenv STK_EMIS_LAB_004 PT_AGFIRES\
\n  setenv STK_EMIS_LAB_005 PT_FIRES\
\n  setenv STK_EMIS_LAB_006 PT_OTHFIRES\
\n  setenv STK_EMIS_LAB_007 PT_OILGAS\
\n  setenv STK_EMIS_LAB_008 PT_CMV\
\n\
\n  # Stack emissions diagnostic files\
\n  #setenv STK_EMIS_DIAG_001 2DSUM\
\n  #setenv STK_EMIS_DIAG_002 2DSUM\
\n  #setenv STK_EMIS_DIAG_003 2DSUM\
\n  #setenv STK_EMIS_DIAG_004 2DSUM\
\n  #setenv STK_EMIS_DIAG_005 2DSUM\
\n\
\n  # Allow CMAQ to Use Point Source files with dates that do not\
\n  # match the internal model date\
\n  # To change default behaviour please see Users Guide for EMIS_SYM_DATE\
\n  setenv STK_EM_SYM_DATE_001 T\
\n  setenv STK_EM_SYM_DATE_002 T\
\n  setenv STK_EM_SYM_DATE_003 T\
\n  setenv STK_EM_SYM_DATE_004 T\
\n  setenv STK_EM_SYM_DATE_005 T\
\n  setenv STK_EM_SYM_DATE_006 T\
\n  setenv STK_EM_SYM_DATE_007 T\
\n  setenv STK_EM_SYM_DATE_008 T\
\n\
\n  #> Lightning NOx configuration\
\n  if ( $CTM_LTNG_NO == 'Y' ) then\
\n     setenv LTNGNO "+'"InLine"'+"    #> set LTNGNO to "+'"Inline"'+" to activate in-line calculation\
\n\
\n  #> In-line lightning NOx options\
\n     setenv USE_NLDN  Y        #> use hourly NLDN strike file [ default: Y ]\
\n     if ( $USE_NLDN == Y ) then\
\n        setenv NLDN_STRIKES ${IN_LTpath}/NLDN.12US1.${YYYYMMDD}_bench.nc\
\n     endif\
\n     setenv LTNGPARMS_FILE ${IN_LTpath}/LTNG_AllParms_12US1_bench.nc #> lightning parameter file\
\n  endif\
\n\
\n  #> In-line biogenic emissions configuration\
\n  if ( $CTM_BIOGEMIS == 'Y' ) then   \
\n     set IN_BEISpath = ${INPDIR}/land\
\n     setenv GSPRO      $BLD/gspro_biogenics.txt\
\n     setenv B3GRD      $IN_BEISpath/b3grd_bench.nc\
\n     setenv BIOSW_YN   Y     #> use frost date switch [ default: Y ]\
\n     setenv BIOSEASON  $IN_BEISpath/bioseason.cmaq.2016_12US1_full_bench.ncf \
\n                             #> ignore season switch file if BIOSW_YN = N\
\n     setenv SUMMER_YN  Y     #> Use summer normalized emissions? [ default: Y ]\
\n     setenv PX_VERSION Y     #> MCIP is PX version? [ default: N ]\
\n     setenv SOILINP    $OUTDIR/CCTM_SOILOUT_${RUNID}_${YESTERDAY}.nc\
\n                             #> Biogenic NO soil input file; ignore if INITIAL_RUN = Y\
\n  endif\
\n\
\n  #> Windblown dust emissions configuration\
\n  if ( $CTM_WB_DUST == 'Y' ) then\
\n     # Input variables for BELD3 Landuse option\
\n     setenv DUST_LU_1 $LUpath/beld3_12US1_459X299_output_a_bench.nc\
\n     setenv DUST_LU_2 $LUpath/beld4_12US1_459X299_output_tot_bench.nc\
\n  endif\
\n\
\n  #> In-line sea spray emissions configuration\
\n  setenv OCEAN_1 ${EMISpath}/OCEAN #> horizontal grid-dependent surf zone file\
\n\
\n  #> Bidirectional ammonia configuration\
\n  if ( $CTM_ABFLUX == 'Y' ) then\
\n     setenv E2C_SOIL ${LUpath}/epic_festc1.4_20180516/2016_US1_soil_bench.nc\
\n     setenv E2C_CHEM ${LUpath}/epic_festc1.4_20180516/2016_US1_time${YYYYMMDD}_bench.nc\
\n     setenv E2C_CHEM_YEST ${LUpath}/epic_festc1.4_20180516/2016_US1_time${YESTERDAY}_bench.nc\
\n     setenv E2C_LU ${LUpath}/beld4_12kmCONUS_2011nlcd_bench.nc\
\n  endif\
\n\
\n#> Inline Process Analysis \
\n  setenv CTM_PROCAN N        #> use process analysis [ default: N]\
\n  if ( $?CTM_PROCAN ) then   # $CTM_PROCAN is defined\
\n     if ( $CTM_PROCAN == 'Y' || $CTM_PROCAN == 'T' ) then\
\n#> process analysis global column, row and layer ranges\
\n#       setenv PA_BCOL_ECOL "'"10 90"'+"  # default: all columns\
\n#       setenv PA_BROW_EROW "+'"10 80"'+"  # default: all rows\
\n#       setenv PA_BLEV_ELEV "+'"1  4"'+"   # default: all levels\
\n        setenv PACM_INFILE ${NMLpath}/pa_${MECH}.ctl\
\n        setenv PACM_REPORT $OUTDIR/"+'"PA_REPORT"'+".${YYYYMMDD}\
\n     endif\
\n  endif\
\n\
\n#> Integrated Source Apportionment Method (ISAM) Options\
\n setenv CTM_ISAM N\
\n if ( $?CTM_ISAM ) then\
\n    if ( $CTM_ISAM == 'Y' || $CTM_ISAM == 'T' ) then\
\n       setenv SA_IOLIST ${WORKDIR}/isam_control.txt\
\n       setenv ISAM_BLEV_ELEV "+'" 1 1"'+"\
\n       setenv AISAM_BLEV_ELEV "+'" 1 1"'+"\
\n\
\n       #> Set Up ISAM Initial Condition Flags\
\n       if ($NEW_START == true || $NEW_START == TRUE ) then\
\n          setenv ISAM_NEW_START Y\
\n          setenv ISAM_PREVDAY\
\n       else\
\n          setenv ISAM_NEW_START N\
\n          setenv ISAM_PREVDAY "+'"$OUTDIR/CCTM_SA_CGRID_${RUNID}_${YESTERDAY}.nc"'+"\
\n       endif\
\n\
\n       #> Set Up ISAM Output Filenames\
\n       setenv SA_ACONC_1      "+'"$OUTDIR/CCTM_SA_ACONC_${CTM_APPL}.nc -v"'+"\
\n       setenv SA_CONC_1       "+'"$OUTDIR/CCTM_SA_CONC_${CTM_APPL}.nc -v"'+"\
\n       setenv SA_DD_1         "+'"$OUTDIR/CCTM_SA_DRYDEP_${CTM_APPL}.nc -v"'+"\
\n       setenv SA_WD_1         "+'"$OUTDIR/CCTM_SA_WETDEP_${CTM_APPL}.nc -v"'+"\
\n       setenv SA_CGRID_1      "+'"$OUTDIR/CCTM_SA_CGRID_${CTM_APPL}.nc -v"'+"\
\n\
\n       #> Set optional ISAM regions files\
\n       #setenv ISAM_REGIONS $INPDIR/GRIDMASK_STATES_12SE1.nc\
\n\
\n\
\n    endif\
\n endif\
\n\
\n\
\n#> Sulfur Tracking Model (STM)\
\n setenv STM_SO4TRACK N        #> sulfur tracking [ default: N ]\
\n if ( $?STM_SO4TRACK ) then\
\n    if ( $STM_SO4TRACK == 'Y' || $STM_SO4TRACK == 'T' ) then\
\n\
\n      #> option to normalize sulfate tracers [ default: Y ]\
\n      setenv STM_ADJSO4 Y\
\n\
\n    endif\
\n endif\
\n\
\n#> CMAQ-DDM-3D\
\n setenv CTM_DDM3D N\
\n set NPMAX    = 1\
\n setenv SEN_INPUT ${WORKDIR}/sensinput.dat\
\n\
\n setenv DDM3D_HIGH N     # allow higher-order sensitivity parameters [ T | Y | F | N ] (default is N/F)\
\n\
\n if ($NEW_START == true || $NEW_START == TRUE ) then\
\n    setenv DDM3D_RST N   # begins from sensitivities from a restart file [ T | Y | F | N ] (default is Y/T)\
\n    set S_ICpath =\
\n    set S_ICfile =\
\n else\
\n    setenv DDM3D_RST Y\
\n    set S_ICpath = $OUTDIR\
\n    set S_ICfile = CCTM_SENGRID_${RUNID}_${YESTERDAY}.nc\
\n endif\
\n\
\n setenv DDM3D_BCS F      # use sensitivity bc file for nested runs [ T | Y | F | N ] (default is N/F)                                            \
\n set S_BCpath =\
\n set S_BCfile =\
\n\
\n setenv CTM_NPMAX       $NPMAX\
\n setenv CTM_SENS_1      "+'"$OUTDIR/CCTM_SENGRID_${CTM_APPL}.nc -v"'+"\
\n setenv A_SENS_1        "+'"$OUTDIR/CCTM_ASENS_${CTM_APPL}.nc -v"'+"\
\n setenv CTM_SWETDEP_1   "+'"$OUTDIR/CCTM_SENWDEP_${CTM_APPL}.nc -v"'+"\
\n setenv CTM_SDRYDEP_1   "+'"$OUTDIR/CCTM_SENDDEP_${CTM_APPL}.nc -v"'+"\
\n setenv CTM_NPMAX       $NPMAX\
\n    if ( $?CTM_DDM3D ) then\
\n       if ( $CTM_DDM3D == 'Y' || $CTM_DDM3D == 'T' ) then \
\n setenv INIT_SENS_1     $S_ICpath/$S_ICfile\
\n setenv BNDY_SENS_1     $S_BCpath/$S_BCfile\
\n       endif\
\n    endif\
\n \
\n# =====================================================================\
\n#> Output Files\
\n# =====================================================================\
\n\
\n  #> set output file names\
\n  setenv S_CGRID         "+'"$OUTDIR/CCTM_CGRID_${CTM_APPL}.nc"'+"         #> 3D Inst. Concentrations\
\n  setenv CTM_CONC_1      "+'"$OUTDIR/CCTM_CONC_${CTM_APPL}.nc -v"'+"        #> On-Hour Concentrations\
\n  setenv A_CONC_1        "+'"$OUTDIR/CCTM_ACONC_${CTM_APPL}.nc -v"'+"       #> Hourly Avg. Concentrations\
\n  setenv MEDIA_CONC      "+'"$OUTDIR/CCTM_MEDIA_CONC_${CTM_APPL}.nc -v"'+"  #> NH3 Conc. in Media\
\n  setenv CTM_DRY_DEP_1   "+'"$OUTDIR/CCTM_DRYDEP_${CTM_APPL}.nc -v"'+"      #> Hourly Dry Deposition\
\n  setenv CTM_DEPV_DIAG   "+'"$OUTDIR/CCTM_DEPV_${CTM_APPL}.nc -v"'+"        #> Dry Deposition Velocities\
\n  setenv B3GTS_S         "+'"$OUTDIR/CCTM_B3GTS_S_${CTM_APPL}.nc -v"'+"     #> Biogenic Emissions\
\n  setenv SOILOUT         "+'"$OUTDIR/CCTM_SOILOUT_${CTM_APPL}.nc"'+"        #> Soil Emissions\
\n  setenv CTM_WET_DEP_1   "+'"$OUTDIR/CCTM_WETDEP1_${CTM_APPL}.nc -v"'+"     #> Wet Dep From All Clouds\
\n  setenv CTM_WET_DEP_2   "+'"$OUTDIR/CCTM_WETDEP2_${CTM_APPL}.nc -v"'+"     #> Wet Dep From SubGrid Clouds\
\n  setenv CTM_PMDIAG_1    "+'"$OUTDIR/CCTM_PMDIAG_${CTM_APPL}.nc -v"'+"      #> On-Hour Particle Diagnostics\
\n  setenv CTM_APMDIAG_1   "+'"$OUTDIR/CCTM_APMDIAG_${CTM_APPL}.nc -v"'+"     #> Hourly Avg. Particle Diagnostics\
\n  setenv CTM_RJ_1        "+'"$OUTDIR/CCTM_PHOTDIAG1_${CTM_APPL}.nc -v"'+"   #> 2D Surface Summary from Inline Photolysis\
\n  setenv CTM_RJ_2        "+'"$OUTDIR/CCTM_PHOTDIAG2_${CTM_APPL}.nc -v"'+"   #> 3D Photolysis Rates \
\n  setenv CTM_RJ_3        "+'"$OUTDIR/CCTM_PHOTDIAG3_${CTM_APPL}.nc -v"'+"   #> 3D Optical and Radiative Results from Photolysis\
\n  setenv CTM_SSEMIS_1    "+'"$OUTDIR/CCTM_SSEMIS_${CTM_APPL}.nc -v"'+"      #> Sea Spray Emissions\
\n  setenv CTM_DUST_EMIS_1 "+'"$OUTDIR/CCTM_DUSTEMIS_${CTM_APPL}.nc -v"'+"    #> Dust Emissions\
\n  setenv CTM_IPR_1       "+'"$OUTDIR/CCTM_PA_1_${CTM_APPL}.nc -v"'+"        #> Process Analysis\
\n  setenv CTM_IPR_2       "+'"$OUTDIR/CCTM_PA_2_${CTM_APPL}.nc -v"'+"        #> Process Analysis\
\n  setenv CTM_IPR_3       "+'"$OUTDIR/CCTM_PA_3_${CTM_APPL}.nc -v"'+"        #> Process Analysis\
\n  setenv CTM_IRR_1       "+'"$OUTDIR/CCTM_IRR_1_${CTM_APPL}.nc -v"'+"       #> Chem Process Analysis\
\n  setenv CTM_IRR_2       "+'"$OUTDIR/CCTM_IRR_2_${CTM_APPL}.nc -v"'+"       #> Chem Process Analysis\
\n  setenv CTM_IRR_3       "+'"$OUTDIR/CCTM_IRR_3_${CTM_APPL}.nc -v"'+"       #> Chem Process Analysis\
\n  setenv CTM_DRY_DEP_MOS "+'"$OUTDIR/CCTM_DDMOS_${CTM_APPL}.nc -v"'+"       #> Dry Dep\
\n  setenv CTM_DRY_DEP_FST "+'"$OUTDIR/CCTM_DDFST_${CTM_APPL}.nc -v"'+"       #> Dry Dep\
\n  setenv CTM_DEPV_MOS    "+'"$OUTDIR/CCTM_DEPVMOS_${CTM_APPL}.nc -v"'+"     #> Dry Dep Velocity\
\n  setenv CTM_DEPV_FST    "+'"$OUTDIR/CCTM_DEPVFST_${CTM_APPL}.nc -v"'+"     #> Dry Dep Velocity\
\n  setenv CTM_VDIFF_DIAG  "+'"$OUTDIR/CCTM_VDIFF_DIAG_${CTM_APPL}.nc -v"'+"  #> Vertical Dispersion Diagnostic\
\n  setenv CTM_VSED_DIAG   "+'"$OUTDIR/CCTM_VSED_DIAG_${CTM_APPL}.nc -v"'+"   #> Particle Grav. Settling Velocity\
\n  setenv CTM_LTNGDIAG_1  "+'"$OUTDIR/CCTM_LTNGHRLY_${CTM_APPL}.nc -v"'+"    #> Hourly Avg Lightning NO\
\n  setenv CTM_LTNGDIAG_2  "+'"$OUTDIR/CCTM_LTNGCOL_${CTM_APPL}.nc -v"'+"     #> Column Total Lightning NO\
\n  setenv CTM_VEXT_1      "+'"$OUTDIR/CCTM_VEXT_${CTM_APPL}.nc -v"'+"        #> On-Hour 3D Concs at select sites\
\n\
\n  #> set floor file (neg concs)\
\n  setenv FLOOR_FILE ${OUTDIR}/FLOOR_${CTM_APPL}.txt\
\n\
\n  #> look for existing log files and output files\
\n  ( ls CTM_LOG_???.${CTM_APPL} > buff.txt ) >& /dev/null\
\n  ( ls ${LOGDIR}/CTM_LOG_???.${CTM_APPL} >> buff.txt ) >& /dev/null\
\n  set log_test = `cat buff.txt`; rm -f buff.txt\
\n\
\n  set OUT_FILES = (${FLOOR_FILE} ${S_CGRID} ${CTM_CONC_1} ${A_CONC_1} ${MEDIA_CONC} ${CTM_DRY_DEP_1} $CTM_DEPV_DIAG $B3GTS_S $SOILOUT $CTM_WET_DEP_1 $CTM_WET_DEP_2 $CTM_PMDIAG_1 $CTM_APMDIAG_1 $CTM_RJ_1 $CTM_RJ_2 $CTM_RJ_3 $CTM_SSEMIS_1 $CTM_DUST_EMIS_1 $CTM_IPR_1 $CTM_IPR_2 $CTM_IPR_3 $CTM_IRR_1 $CTM_IRR_2 $CTM_IRR_3 $CTM_DRY_DEP_MOS $CTM_DRY_DEP_FST $CTM_DEPV_MOS $CTM_DEPV_FST $CTM_VDIFF_DIAG $CTM_VSED_DIAG $CTM_LTNGDIAG_1 $CTM_LTNGDIAG_2 $CTM_VEXT_1 )\
\n  if ( $?CTM_ISAM ) then\
\n     if ( $CTM_ISAM == 'Y' || $CTM_ISAM == 'T' ) then\
\n        set OUT_FILES = (${OUT_FILES} ${SA_ACONC_1} ${SA_CONC_1} ${SA_DD_1} ${SA_WD_1} ${SA_CGRID_1} )\
\n     endif\
\n  endif\
\n  if ( $?CTM_DDM3D ) then\
\n     if ( $CTM_DDM3D == 'Y' || $CTM_DDM3D == 'T' ) then\
\n        set OUT_FILES = (${OUT_FILES} ${CTM_SENS_1} ${A_SENS_1} ${CTM_SWETDEP_1} ${CTM_SDRYDEP_1} )\
\n     endif\
\n  endif\
\n  set OUT_FILES = `echo $OUT_FILES | sed "+'"s; -v;;g"'+" | sed "+'"s;MPI:;;g"'+" `\
\n  ( ls $OUT_FILES > buff.txt ) >& /dev/null\
\n  set out_test = `cat buff.txt`; rm -f buff.txt\
\n  \
\n  #> delete previous output if requested\
\n  if ( $CLOBBER_DATA == true || $CLOBBER_DATA == TRUE  ) then\
\n     echo \
\n     echo "+'"Existing Logs and Output Files for Day ${TODAYG} Will Be Deleted"'+"\
\n\
\n     #> remove previous log files\
\n     foreach file ( ${log_test} )\
\n        #echo "+'"Deleting log file: $file"'+"\
\n        /bin/rm -f $file  \
\n     end\
\n \
\n     #> remove previous output files\
\n     foreach file ( ${out_test} )\
\n        #echo "+'"Deleting output file: $file"'+"\
\n        /bin/rm -f $file  \
\n     end\
\n     /bin/rm -f ${OUTDIR}/CCTM_EMDIAG*${RUNID}_${YYYYMMDD}.nc\
\n\
\n  else\
\n     #> error if previous log files exist\
\n     if ( "+'"$log_test"'+" != "+'""'+" ) then\
\n       echo "+'"*** Logs exist - run ABORTED ***"'+"\
\n       echo "+'"*** To overide, set CLOBBER_DATA = TRUE in run_cctm.csh ***"'+"\
\n       echo "+'"*** and these files will be automatically deleted. ***"'+"\
\n       exit 1\
\n     endif\
\n     \
\n     #> error if previous output files exist\
\n     if ( "+'"$out_test"'+" != "+'""'+" ) then\
\n       echo "+'"*** Output Files Exist - run will be ABORTED ***"'+"\
\n       foreach file ( $out_test )\
\n          echo "+'" cannot delete $file"'+"\
\n       end\
\n       echo "+'"*** To overide, set CLOBBER_DATA = TRUE in run_cctm.csh ***"'+"\
\n       echo "+'"*** and these files will be automatically deleted. ***"'+"\
\n       exit 1\
\n     endif\
\n  endif\
\n\
\n  #> for the run control ...\
\n  setenv CTM_STDATE      $YYYYJJJ\
\n  setenv CTM_STTIME      $STTIME\
\n  setenv CTM_RUNLEN      $NSTEPS\
\n  setenv CTM_TSTEP       $TSTEP\
\n  setenv INIT_CONC_1 $ICpath/$ICFILE\
\n  setenv BNDY_CONC_1 $BCpath/$BCFILE\
\n  setenv OMI $OMIpath/$OMIfile\
\n  setenv OPTICS_DATA $OMIpath/$OPTfile\
\n #setenv XJ_DATA $JVALpath/$JVALfile\
\n \
\n  #> species defn & photolysis\
\n  setenv gc_matrix_nml ${NMLpath}/GC_$MECH.nml\
\n  setenv ae_matrix_nml ${NMLpath}/AE_$MECH.nml\
\n  setenv nr_matrix_nml ${NMLpath}/NR_$MECH.nml\
\n  setenv tr_matrix_nml ${NMLpath}/Species_Table_TR_0.nml\
\n \
\n  #> check for photolysis input data\
\n  setenv CSQY_DATA ${NMLpath}/CSQY_DATA_$MECH\
\n\
\n  if (! (-e $CSQY_DATA ) ) then\
\n     echo "+'" $CSQY_DATA  not found "'+"\
\n     exit 1\
\n  endif\
\n  if (! (-e $OPTICS_DATA ) ) then\
\n     echo "+'" $OPTICS_DATA  not found "'+"\
\n     exit 1\
\n  endif\
\n\
\n# ===================================================================\
\n#> Execution Portion\
\n# ===================================================================\
\n\
\n  #> Print attributes of the executable\
\n  if ( $CTM_DIAG_LVL != 0 ) then\
\n     ls -l $BLD/$EXEC\
\n     size $BLD/$EXEC\
\n     unlimit\
\n     limit\
\n  endif\
\n\
\n  #> Print Startup Dialogue Information to Standard Out\
\n  echo \
\n  echo "+'"CMAQ Processing of Day $YYYYMMDD Began at `date`"'+"\
\n  echo \
\n\
\n  #> Executable call for single PE, uncomment to invoke\
\n  #( /usr/bin/time -p $BLD/$EXEC ) |& tee buff_${EXECUTION_ID}.txt\
\n\
\n  #> Executable call for multi PE, configure for your system \
\n  # set MPI = /usr/local/intel/impi/3.2.2.006/bin64\
\n  # set MPIRUN = $MPI/mpirun\
\n  ( /usr/bin/time -p mpirun -np $NPROCS $BLD/$EXEC ) |& tee buff_${EXECUTION_ID}.txt\
\n  \
\n  #> Harvest Timing Output so that it may be reported below\
\n  set rtarray = "+'"${rtarray} `tail -3 buff_${EXECUTION_ID}.txt | grep -Eo '+"'[+-]?[0-9]+([.][0-9]+)?'"+' | head -1` "'+"\
\n  rm -rf buff_${EXECUTION_ID}.txt\
\n\
\n  #> Abort script if abnormal termination\
\n  if ( ! -e $OUTDIR/CCTM_CGRID_${CTM_APPL}.nc ) then\
\n    echo ""\
\n    echo "+'"**************************************************************"'+"\
\n    echo "+'"** Runscript Detected an Error: CGRID file was not written. **"'+"\
\n    echo "+'"**   This indicates that CMAQ was interrupted or an issue   **"'+"\
\n    echo "+'"**   exists with writing output. The runscript will now     **"'+"\
\n    echo "+'"**   abort rather than proceeding to subsequent days.       **"'+"\
\n    echo "+'"**************************************************************"'+"\
\n    break\
\n  endif\
\n\
\n  #> Print Concluding Text\
\n  echo \
\n  echo "+'"CMAQ Processing of Day $YYYYMMDD Finished at `date`"'+"\
\n  echo\
\n  echo "+'"\\\\\=====\\\\\=====\\\\\=====\\\\\=====/////=====/////=====/////=====/////"'+"\
\n  echo\
\n\
\n# ===================================================================\
\n#> Finalize Run for This Day and Loop to Next Day\
\n# ===================================================================\
\n\
\n  #> Save Log Files and Move on to Next Simulation Day\
\n  mv CTM_LOG_???.${CTM_APPL} $LOGDIR\
\n  if ( $CTM_DIAG_LVL != 0 ) then\
\n    mv CTM_DIAG_???.${CTM_APPL} $LOGDIR\
\n  endif\
\n\
\n  #> The next simulation day will, by definition, be a restart\
\n  setenv NEW_START false\
\n\
\n  #> Increment both Gregorian and Julian Days\
\n  set TODAYG = `date -ud "+'"${TODAYG}+1days"'+" +%Y-%m-%d` #> Add a day for tomorrow\
\n  set TODAYJ = `date -ud "+'"${TODAYG}"'+" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ\
\n\
\nend  #Loop to the next Simulation Day\
\n\
\n# ===================================================================\
\n#> Generate Timing Report\
\n# ===================================================================\
\nset RTMTOT = 0\
\nforeach it ( `seq ${NDAYS}` )\
\n    set rt = `echo ${rtarray} | cut -d' ' -f${it}`\
\n    set RTMTOT = `echo "+'"${RTMTOT} + ${rt}"'+" | bc -l`\
\nend\
\n\
\nset RTMAVG = `echo "+'"scale=2; ${RTMTOT} / ${NDAYS}"'+" | bc -l`\
\nset RTMTOT = `echo "+'"scale=2; ${RTMTOT} / 1"'+" | bc -l`\
\n\
\necho\
\necho "+'"=================================="'+"\
\necho "+'"  ***** CMAQ TIMING REPORT *****"'+"\
\necho "+'"=================================="'+"\
\necho "+'"Start Day: ${START_DATE}"'+"\
\necho "+'"End Day:   ${END_DATE}"'+"\
\necho "+'"Number of Simulation Days: ${NDAYS}"'+"\
\necho "+'"Domain Name:               ${GRID_NAME}"'+"\
\necho "+'"Number of Grid Cells:      ${NCELLS}  (ROW x COL x LAY)"'+"\
\necho "+'"Number of Layers:          ${NZ}"'+"\
\necho "+'"Number of Processes:       ${NPROCS}"'+"\
\necho "+'"   All times are in seconds."'+"\
\necho\
\necho "+'"Num  Day        Wall Time"'+"\
\nset d = 0\
\nset day = ${START_DATE}\
\nforeach it ( `seq ${NDAYS}` )\
\n    # Set the right day and format it\
\n    set d = `echo "+'"${d} + 1"'+"  | bc -l`\
\n    set n = `printf "+'"%02d"'+" ${d}`\
\n\
\n    # Choose the correct time variables\
\n    set rt = `echo ${rtarray} | cut -d' ' -f${it}`\
\n\
\n    # Write out row of timing data\
\n    echo "+'"${n}   ${day}   ${rt}"'+"\
\n\
\n    # Increment day for next loop\
\n    set day = `date -ud "+'"${day}+1days"'+" +%Y-%m-%d`\
\nend\
\necho "+'"     Total Time = ${RTMTOT}"'+"\
\necho "+'"      Avg. Time = ${RTMAVG}"'+"\
\n\
\nexit"
    
    file1.write(str1)
    file1.close()
    return file1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('CMAQHome')
    parser.add_argument('wrf_dir')
    parser.add_argument('GDNAM')
    parser.add_argument('YYYYMMDD')
    parser.add_argument('YYYYMMDDend')
    parser.add_argument('NPCOL')
    parser.add_argument('NPROW')
    parser.add_argument('NLAYS')
    parser.add_argument('NEW_START')
    parser.add_argument('YYYYMMDDi')
    parser.add_argument('YESTERDAY')
    parser.add_argument('wrfDomain')
    args = parser.parse_args()
    CMAQHome = args.CMAQHome
    wrf_dir = args.wrf_dir
    GDNAM = args.GDNAM
    YYYYMMDD = args.YYYYMMDD
    YYYYMMDDend = args.YYYYMMDDend
    YYYYMMDDi = args.YYYYMMDDi
    NPCOL = args.NPCOL
    NPROW = args.NPROW
    NLAYS = args.NLAYS
    NEW_START = args.NEW_START
    YESTERDAY = args.YESTERDAY
    wrfDomain = args.wrfDomain
    mcipPath = CMAQHome+'/data/mcip/'+GDNAM
    writeMCIPscript(CMAQHome,wrf_dir,GDNAM,YYYYMMDD,YYYYMMDDend,YESTERDAY,wrfDomain)
    writeICONscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD)
    writeBCONscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD)
    writeCCTMscript(CMAQHome,mcipPath,GDNAM,YYYYMMDD,YYYYMMDDend,NPCOL,NPROW,NLAYS,NEW_START,YYYYMMDDi)

#!/bin/bash

# ===============================CMAQrunner.sh=========================================
#
# This bash script runs CMAQ automatically in Brazil by setting the group of inputs 
# bellow. It runs using vehicular emissions from BRAVES, biogenic emissions from MEGAN, 
# Industrial emissions from local inventories and biomass burning from FINN. The 
# following auxiliary codes has been used in this script:
#
#       finn2cmaq: https://github.com/barronh/finn2cmaq 
#       BRAVES: https://github.com/leohoinaski/BRAVES
#       Industrial emissions: https://github.com/leohoinaski/IND_Inventory
#       MEGAN: in my github page
# 
# All functions must be in the CMAQ_REPO root directory. 
#
# List of auxiliary scripts:
#     - shRunnerBRAVES_database.py - main script for running BRAVES
#     - shRunnerIND_inventory.py - main script for running IND_inventory
#     - shRunnerMEGAN.py - main script for running MEGAN
#     - MEGAN2_fixLAI_netCDF.py - script for fixing MEGAN intermediate files
#
# To install netCDF and other libraries required by CMAQ I have developed a bash script, 
# which is in my github webpage. The script to set and compile CMAQv5.3.2 has also been
# available in the githu page.
#
# 
# Required packeges:
# sudo apt-get install libgfortran5
# sudo apt-get -y install nco 
#
# Developed by Leonardo Hoinaski - leonardo.hoinaski@ufsc.br
#
#
#---------------------------------- Inputs --------------------------------------------
CDIR=$PWD
CMAQ_HOME=/media/leohoinaski/HDD/CMAQ_REPO
GDNAM=SC_2019
STARTDAY=2019-06-02
NDAYS=2
ncols=233
nrows=178
runOrnotRoadDens=0
runOrnotRoadEmiss=0
runOrnotMergeRoadEmiss=0
runOrnotBRAVES2netCDF=0
runOrnotCMAQemiss=1

mcipPath=${CMAQ_HOME}/data/mcip/${GDNAM}
wrf_dir=${CMAQ_HOME}/data/met/wrf/${GDNAM}
MEGANHome=${CMAQ_HOME}/PREP/emis/MEGAN21
BRAVEShome=${CMAQ_HOME}/PREP/emis/BRAVES_database
INDinventoryPath=${CMAQ_HOME}/PREP/emis/IND_inventory
finn2cmaqPath=${CMAQ_HOME}/PREP/emis/finn2cmaq-master
YYYYMMDDi=`date -ud "${STARTDAY}" +%Y%m%d`
YYYYJJJi=`date -ud "${STARTDAY}" +%Y%j`
NPCOL=2 # Define number of processors to use - NPCOL*NPROW
NPROW=1
NLAYS=32
NEW_START=TRUE

#==========================================PROCESSING==================================

if [ ! -d "${CMAQ_HOME}/data/inputs" ]; then
  echo "Creating input directory"
  mkdir ${CMAQ_HOME}/data/inputs
fi

if [ ! -d "${CMAQ_HOME}/data/inputs/${GDNAM}" ]; then
  echo "Creating input directory ${CMAQ_HOME}/data/inputs/${GDNAM}"
  mkdir ${CMAQ_HOME}/data/inputs/${GDNAM}
fi

for day in {0..1}
do
  YYYYMMDD=`date -ud "${STARTDAY} +${day}days" +%Y-%m-%d`
  YYYY=`date -ud "${YYYYMMDD}" +%Y`
  MM=`date -ud "${YYYYMMDD}" +%m`
  DD=`date -ud "${YYYYMMDD}" +%d`
  YYYYJJJ=`date -ud "${YYYYMMDD}" +%Y%j`
  STJD=`date -ud "${YYYYMMDD}" +%j`
  EDJD=`date -ud "${YYYYMMDD}" +%j`
  echo "DAY $YYYYJJJ"
  python3 ${CDIR}/shRunnerCMAQ.py ${CMAQ_HOME} ${GDNAM} ${YYYYMMDD} ${NPCOL} ${NPROW} ${NLAYS} ${NEW_START} ${YYYYMMDDi}
  echo '----------------------------------Running MCIP---------------------------------'
  cd  ${CMAQ_HOME}/PREP/mcip/scripts && ./run_mcip.csh  >&! mcip.log; cd -

  if test ${day} -lt 1 ;then
    YYYY=`date -ud "${YYYYMMDD}" +%Y`
    YYYYJJJ=`date -ud "${YYYYMMDD}" +%Y%j`
    STJD=`date -ud "${YYYYMMDD}" +%j`
    EDJD=`date -ud "${YYYYMMDD}" +%j`
    echo '------------------------------Running PREPMEGAN------------------------------'
    if [ ! -f "${wrf_dir}/wrfout" ]; then
      ln -sf ${wrf_dir}/wrfout_d02_'+YYYYMMDD+'_00:00:00 ${wrf_dir}/wrfout
    fi
    python3 ${CDIR}/shRunnerMEGAN.py ${MEGANHome} ${mcipPath} ${wrf_dir} ${GDNAM} ${YYYY} ${STJD} ${EDJD} ${ncols} ${nrows}
    cd ${MEGANHome}/prepmegan4cmaq_2014-06-02 && ./run_prepmegan4cmaq.csh >&! prepmegan.log; cd -
    echo 'Running txt2ioapi'${pwd}
    cd ${MEGANHome}/MEGANv2.10/work && ./run.txt2ioapi.v210.csh >&! txtioapi.log; cd -
    echo 'Fixing txt2ioapi files'
    python3 ${CDIR}/MEGAN2_fixLAI_netCDF.py ${MEGANHome}  
    mv ${MEGANHome}/inputs/LAIS46.SC_2019.fixed.ncf ${MEGANHome}/inputs/LAIS46.SC_2019.ncf
    echo '---------------------------------Running ICON--------------------------------'
    cd ${CMAQ_HOME}/PREP/icon/scripts &&./run_icon.csh >&! icon.log; cd - &
    echo '---------------------------------Running BCON--------------------------------'
    cd ${CMAQ_HOME}/PREP/bcon/scripts &&./run_bcon.csh >&! bcon.log; cd -
    if [ ! -f "${CMAQ_HOME}/PREP/Spatial-Allocator/data/ocean_file_${GDNAM}.ncf" ]; then
      echo '--------------------------Running OCEAN - SURFZONE-------------------------'
      python3 ${CDIR}/hoinaskiSURFZONE.py ${CMAQ_HOME}/PREP/Spatial-Allocator ${GDNAM} ${mcipPath} 
      ln -sf ${CMAQ_HOME}/PREP/Spatial-Allocator/data/ocean_file_${GDNAM}.ncf ${CMAQ_HOME}/data/inputs/${GDNAM}/OCEAN
    else
      echo 'You already have the OCEAN file'
    fi
    echo 'Seting next step as NEWSTART=FALSE'
  fi
  wait

  echo '------------------------------Running BRAVES_database--------------------------'
  # Check shRunnerBRAVES_database.py for more input configurations
  python3 ${CDIR}/shRunnerBRAVES_database.py ${BRAVEShome} ${mcipPath} ${GDNAM} ${YYYY} ${runOrnotRoadDens} ${runOrnotRoadEmiss} ${runOrnotMergeRoadEmiss} ${runOrnotBRAVES2netCDF} ${runOrnotCMAQemiss} &
 
  echo '# -----------------------------Running IND_Inventory---------------------------'
  python3 ${CDIR}/shRunnerIND_inventory.py ${INDinventoryPath} ${mcipPath} ${GDNAM} &

  echo '---------------------------------Running finn2cmaq-----------------------------'
  cd ${finn2cmaqPath} && ./scripts/get_nrt.py ${YYYYMMDD}; cd -
  cd ${finn2cmaqPath} && ./scripts/txt2daily.py ${mcipPath}/GRIDDESC ${GDNAM} ${YYYY} ${finn2cmaqPath}/www.acom.ucar.edu/Data/fire/data/finn1/FINNv1.5_2019.GEOSCHEM.tar.gz ${finn2cmaqPath}/daily/${YYYY}/FINNv1.5_${YYYYMMDD}.GEOSCHEM.NRT.${GDNAM}.nc; cd -
  cd ${finn2cmaqPath} && ./scripts/daily2hourly3d.py -d ${STARTDAY} ${finn2cmaqPath}/daily/${YYYY}/FINNv1.5_${YYYYMMDD}.GEOSCHEM.NRT.${GDNAM}.nc ${finn2cmaqPath}/hourly/${YYYY}/${MM}/FINNv1.5_2016.CB6r3.NRT.${GDNAM}.3D.${YYYY}-${MM}-${DD}.nc; cd - & 

  echo '----------------------------------Running MEGAN--------------------------------'
  # Check shRunnerMEGAN.py for more input configurations
  python3 ${CDIR}/shRunnerMEGAN.py ${MEGANHome} ${mcipPath} ${wrf_dir} ${GDNAM} ${YYYY} ${STJD} ${EDJD} ${ncols} ${nrows}
  cd ${MEGANHome}/MEGANv2.10/work && ./run.met2mgn.v210.csh >&! met2mgn.log; cd -
  cd ${MEGANHome}/MEGANv2.10/work && ./run.emproc.v210.csh >&! emproc.log; cd -
  cd ${MEGANHome}/MEGANv2.10/work && ./run.mgn2mech.v210.csh >&! mgn2mech.log; cd -
  ncatted -O -h -a NVARS,global,m,d,24 ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf
  ncatted -O -h -a VAR-LIST,global,m,c,"ISOP            TERP            PAR             XYL             OLE             NR              MEOH            CH4             NH3             NO              ALD2            ETOH            FORM            ALDX            TOL             IOLE            CO              ETHA            ETH             ETHY            PRPA            BENZ            ACET            KET             " ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf
  ncks -O -x -v GDAY ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf
  
  wait

  echo '-----------------------Copying input files to CMAQ input folder----------------'
  ln -sf ${MEGANHome}/MEGANv2.10/outputs/MEGANv2.10.${GDNAM}.CB6.${YYYYJJJ}.ncf ${CMAQ_HOME}/data/inputs/${GDNAM}/MEGANout
  ln -sf ${BRAVEShome}/Outputs/${GDNAM}/BRAVESdatabase2CMAQ_${YYYY}_${MM}_${DD}_0000_to_${YYYY}_${MM}_${DD}_2300.nc ${CMAQ_HOME}/data/inputs/${GDNAM}/BRAVESout
  ln -sf ${INDinventoryPath}/Outputs/${GDNAM}/IND2CMAQ_${YYYY}_${MM}_${DD}_0000_to_${YYYY}_${MM}_${DD}_2300.nc ${CMAQ_HOME}/data/inputs/${GDNAM}/INDout
  ln -sf ${finn2cmaqPath}/hourly/${YYYY}/$MM/FINNv1.5_2016.CB6r3.NRT.${GDNAM}.3D.${YYYYMMDD}.nc ${CMAQ_HOME}/data/inputs/${GDNAM}/FINNout
  cd ${CMAQ_HOME}/data/inputs/${GDNAM} 
  echo 'Converting to netCDF3' 
  ncks -3 -O BRAVESout BRAVESout
  ncks -3 -O INDout INDout
  if [ ! -f "${CMAQ_HOME}/data/inputs/${GDNAM}/OCEAN" ]; then
    ln -sf ${CMAQ_HOME}/PREP/Spatial-Allocator/data/ocean_file_${GDNAM}.ncf ${CMAQ_HOME}/data/inputs/${GDNAM}/OCEAN
  fi

  echo '-----------------------------------Running CCTM--------------------------------'
  cd ${CMAQ_HOME}/CCTM/scripts && ./run_cctm.csh
  NEW_START=FALSE
done




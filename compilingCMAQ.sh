#!/bin/bash

#=============================================================================
# Download CMAQv5.3.2 from github = https://github.com/USEPA/CMAQ/tree/5.3.2
# Cloning CMAQ to server
ROOT=/home/lcqar
cd ${ROOT}
git clone https://github.com/USEPA/CMAQ.git
mv CMAQ CMAQ_REPO
cd CMAQ_REPO
git checkout bf2630f2b31acad8f9b31e07981c544016b06a0d
export CMAQ_HOME=$PWD

sudo apt-get install -y git
sudo apt-get install -y csh

CMAQ_REPO=${CMAQ_HOME}

cd ${CMAQ_REPO}

# Building project
sudo ./bldit_project.csh

# Seting and fixing config_cmaq.csh
sudo sed -i 's:setenv IOAPI_INCL_DIR   iopai_inc_gcc   #> I/O API include header files:setenv IOAPI_INCL_DIR   /usr/local/ioapi_3.2/ioapi/fixed_src   #> I/O API include header files:' config_cmaq.csh
sudo sed -i 's:setenv IOAPI_LIB_DIR    ioapi_lib_gcc   #> I/O API libraries:setenv IOAPI_LIB_DIR    /usr/local/ioapi_3.2/Linux2_x86_64gfort   #> I/O API libraries:' config_cmaq.csh
sudo sed -i 's:setenv NETCDF_LIB_DIR   netcdf_lib_gcc  #> netCDF C directory path:setenv NETCDF_LIB_DIR   /usr/local/netcdf/lib  #> netCDF C directory path:' config_cmaq.csh
sudo sed -i 's:setenv NETCDF_INCL_DIR  netcdf_inc_gcc  #> netCDF C directory path:setenv NETCDF_INCL_DIR  /usr/local/netcdf/include  #> netCDF C directory path:' config_cmaq.csh
sudo sed -i 's:setenv NETCDFF_LIB_DIR  netcdff_lib_gcc #> netCDF Fortran directory path:setenv NETCDFF_LIB_DIR  /usr/local/netcdf/lib #> netCDF Fortran directory path:' config_cmaq.csh
sudo sed -i 's:setenv NETCDFF_INCL_DIR netcdff_inc_gcc #> netCDF Fortran directory path:setenv NETCDFF_INCL_DIR /usr/local/netcdf/include #> netCDF Fortran directory path:' config_cmaq.csh
sudo sed -i 's:setenv MPI_LIB_DIR      mpi_lib_gcc     #> MPI directory path:setenv MPI_LIB_DIR      /usr/local/mpich     #> MPI directory path:' config_cmaq.csh
sudo sed -i 's:setenv myFC mpifort:setenv myFC /usr/local/mpich/bin/mpifort:' config_cmaq.csh
sudo ./config_cmaq.csh gcc

sudo mv ${CMAQ_REPO}/lib/x86_64/gcc/netcdff/includ ${CMAQ_REPO}/lib/x86_64/gcc/netcdff/include

# Compiling CCTM
cd ${CMAQ_REPO}/CCTM/scripts
sudo sed -i "668,668s:^:csh:" bldit_cctm.csh 
sudo ./bldit_cctm.csh gcc 
cd BLD_CCTM_v532_gcc
sudo make clean
sudo make DEBUG=TRUE
cd ..

# Compiling BCON
cd ${CMAQ_REPO}/PREP/bcon/scripts 
sudo ./bldit_bcon.csh gcc

# Compiling ICON
cd ${CMAQ_REPO}/PREP/icon/scripts
sudo ./bldit_icon.csh gcc	

# Compiling MCIP
cd ${CMAQ_REPO}/PREP/mcip/src
sudo sed -i '49,57s/^/#/' Makefile
sudo sed -i '38,38s:^:FC	= gfortran :' Makefile
sudo sed -i 's:#NETCDF = /usr/local/apps/netcdf-4.6.3/gcc-6.1.0:NETCDF = /usr/local/netcdf:' Makefile
sudo sed -i 's:#IOAPI_ROOT = /usr/local/apps/ioapi-3.2_20181011/gcc-6.1.0:IOAPI_ROOT = /usr/local/ioapi_3.2:' Makefile
sudo sed -i '41,41s:^:FFLAGS= -O3 -I$(NETCDF)/include -I$(IOAPI_ROOT)/Linux2_x86_64gfort  :' Makefile
sudo sed -i '45,45s:^:LIBS    = -L$(IOAPI_ROOT)/Linux2_x86_64gfort -lioapi -L$(NETCDF)/lib -lnetcdff -lnetcdf :' Makefile
sudo make clean
sudo make 

cd ${CMAQ_REPO}
cd data 
sudo mkdir met
cd met
sudo mkdir wrf

cd ${CMAQ_REPO}/


# Downloading benchmark files
#sudo wget ftp://newftp.epa.gov/exposure/CMAQ/V5_3_2/Benchmark/CMAQv5.3.2_Benchmark_2Day_Input.tar.gz




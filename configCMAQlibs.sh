#!/bin/bash

#========================================================
# Shell script para instalar pacotes para rodar o CMAQ
#
# Authores: Leonardo Hoinaski - leonardo.hoinaski@ufsc.br
#	    	
# Last update: 06-11-2020
#--------------------------------------------------------
export CDIR=$PWD
echo 'Starting shell scritp for compiling CMAQ'
echo 'Developer: Leonardo Hoinaski'

# Setting environmental variables
#for netcdf
echo 'export NETCDF=/usr/local/netcdf' >> ~/.bashrc 
echo 'export PATH=$NETCDF/bin:$PATH' >> ~/.bashrc 
echo 'export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH' >> ~/.bashrc 

#for mpich
echo 'export PATH=/usr/local/mpich/bin:${PATH}' >> ~/.bashrc 
echo 'export LD_LIBRARY_PATH=/usr/local/mpich/lib:${LD_LIBRARY_PATH}' >> ~/.bashrc 
echo 'export MANPATH=/usr/local/mpich/share/man:${MANPATH}' >> ~/.bashrc 
echo 'export BIN=Linux2_x86_64gfort' >> ~/.bashrc
source ~/.bashrc

# Installing essential packages
sudo apt update -y
sudo apt install -y build-essential
sudo apt-get install -y manpages-dev
gcc --version
sudo apt-get install -y g++ vim make csh
sudo apt-get install -y tcsh samba cpp m4 quota cvs
sudo apt-get install -y gfortran gfortran-multilib g++ gcc
sudo apt-get install -y curl
sudo apt install -y libnetcdff-dev

# Removing openmpi
sudo apt-get -y remove openmpi-common
sudo apt-get -y purge openmpi-common

cd /usr/local
# Installing zlib
sudo wget 'http://zlib.net/zlib-1.2.12.tar.gz'
sudo tar xf zlib-1.2.12.tar.gz
cd zlib-1.2.12
sudo ./configure --prefix=/usr/local/netcdf
sudo make
sudo make check
sudo make install
cd ..
sudo rm -rf zlib-1.2.12.tar.gz

# Installing HDF5
sudo wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz
sudo tar xf hdf5-1.12.0.tar.gz
sudo rm -rf hdf5-1.12.0.tar.gz
cd hdf5-1.12.0
sudo ./configure --prefix=/usr/local/netcdf --enable-shared --enable-hl --with-zlib=/usr/local/netcdf
sudo make -j 4
sudo make -j 4 check
sudo make -j 4 install
cd ..

# Installing netCDF
sudo wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.1.tar.gz
sudo tar xf netcdf-4.3.3.1.tar.gz
cd netcdf-4.3.3.1
export FC=gfortran
export CC=gcc
export CXX=g++
LDFLAGS=-L/usr/local/netcdf/lib CPPFLAGS=-I/usr/local/netcdf/include ./configure --disable-netcdf-4 --disable-dap --prefix=/usr/local/netcdf
sudo make
sudo make check
sudo make install
cd ..
sudo rm -rf netcdf-4.3.3.1.tar.gz

# Installing netCDF c++
sudo wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx-4.2.tar.gz
sudo tar xf netcdf-cxx-4.2.tar.gz
sudo rm -rf netcdf-cxx-4.2.tar.gz
cd netcdf-cxx-4.2
LDFLAGS=-L/usr/local/netcdf/lib CPPFLAGS=-I/usr/local/netcdf/include ./configure --enable-shared --disable-netcdf-4 --disable-dap --prefix=/usr/local/netcdf
sudo make
sudo make check
sudo make install
cd ..

# Installing netCDF fortran
sudo wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.2.tar.gz
sudo tar xf netcdf-fortran-4.4.2.tar.gz
sudo rm -rf netcdf-fortran-4.4.2.tar.gz
cd netcdf-fortran-4.4.2
LDFLAGS=-L/usr/local/netcdf/lib CPPFLAGS=-I/usr/local/netcdf/include ./configure --prefix=/usr/local/netcdf
sudo make
sudo make check
sudo make install
cd ..

# Installing MPICH
sudo wget http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz
sudo tar xf mpich-3.1.4.tar.gz
sudo rm -rf mpich-3.1.4.tar.gz
cd mpich-3.1.4
sudo ./configure --prefix=/usr/local/mpich
sudo make -j 4
sudo make -j 4 check
sudo make -j 4 install
cd ..


# Installing ioapi
sudo mkdir ioapi_3.2
cd ioapi_3.2

## Download IOAPI Libraries and untar downloaded source code in this directory
sudo wget https://www.cmascenter.org/ioapi/download/ioapi-3.2.tar.gz
sudo tar -xzvf ioapi-3.2.tar.gz
sudo rm -rf ioapi-3.2.tar.gz
#ln -sf /usr/local/netcdf/lib/* Linux2_x86_64gfort/
sudo cp ioapi/Makefile.nocpl ioapi/Makefile
sudo cp m3tools/Makefile.nocpl m3tools/Makefile
sudo cp Makefile.template Makefile

### Set up your Linux system environment
export BIN='Linux2_x86_64gfort'
export BASEDIR='/usr/local/ioapi_3.2'
export CPLMODE='nocpl'


# Fixing flags
sudo sed -i 's:NCFLIBS    = -lnetcdff -lnetcdf:NCFLIBS = -L/usr/local/netcdf/lib -lnetcdff -lnetcdf -lnetcdf:g' Makefile
sudo sed -i 's:BASEDIR    = ${PWD}:BASEDIR    = /usr/local/ioapi_3.2:g' Makefile
sudo sed -i "190,190s:^:BIN=Linux2_x86_64gfort:" Makefile 
sudo sed -i "199,199s:^:CPLMODE=nocpl:" Makefile 

cd ioapi
sudo sed -i 's:OMPFLAGS  = -fopenmp:OMPFLAGS = # -fopenmp:g' Makeinclude.Linux2_x86_64gfort
sudo sed -i 's:OMPLIBS   = -fopenmp:OMPLIBS = # -fopenmp:g' Makeinclude.Linux2_x86_64gfort
#sudo sed -i 's: -DNEED_ARGS=1: -DIOAPI_NCF4=1:g' Makeinclude.Linux2_x86_64gfort

sudo sed -i 's:BASEDIR = ${HOME}/ioapi-3.2:BASEDIR = /usr/local/ioapi_3.2:g' Makefile
sudo sed -i "84,84s:^:BIN=Linux2_x86_64gfort:" Makefile 
sudo sed -i 's:include /usr/local/ioapi_3.2/ioapi/Makeinclude.$(BIN):include /usr/local/ioapi_3.2/ioapi/Makeinclude.Linux2_x86_64gfort:g' Makefile

cd ..
sudo make configure

# Fixing flags after make configure
cd ioapi
sudo sed -i 's:include /usr/local/ioapi_3.2/ioapi/Makeinclude.$(BIN):include /usr/local/ioapi_3.2/ioapi/Makeinclude.Linux2_x86_64gfort:g' Makefile

cd ..
cd m3tools
sudo sed -i "40,40s:^:BIN=Linux2_x86_64gfort:" Makefile 
sudo sed -i 's: LIBS = -L${OBJDIR} -lioapi -L/usr/local/netcdf/lib -lnetcdf -L/usr/local/netcdf/lib -lnetcdff $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS):LIBS = -L${OBJDIR} -lioapi -L/usr/local/netcdf/lib -lnetcdf -L/usr/local/netcdf/lib -lnetcdff $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS):g' Makefile
cd ..
sudo make


sudo apt-get install libgfortran5
sudo apt-get -y install nco 
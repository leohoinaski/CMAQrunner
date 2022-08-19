
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
#======================================================================================
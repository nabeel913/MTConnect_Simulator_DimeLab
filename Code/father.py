# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 16:51:37 2018

@author: smehdi@ncsu.edu
"""
import os
from control_panel import ORGS as ORG
# ==============================================================================
# Function to create directories & subdirectories
# ==============================================================================
#this file would generate folders/subfolders for organizations to be simulated and would make sure that there is no conflict.
#As of now it has basic functionality.
def orgDirs(ORG):
    if(ORG<200):
        # Create directory
        for i in range(ORG):
            dirName = 'temp_folder/'+'Org '+str(i+1)
            try:
                os.mkdir(dirName)
            except FileExistsError:
                pass        
            # Create sub directory
            dirName = dirName+'/adapters'
            try:
                os.makedirs(dirName)    
            except FileExistsError:
                pass
        print(f"Created {ORG} virtual orgs directories")
    else:
        print("Number of ORGS should be <= 20")# -*- coding: utf-8 -*-
orgDirs(ORG)
cncBrands = ['DMG','Mazak','GF','Haas','Doosan','AMS']
# -*- coding: utf-8 -*-


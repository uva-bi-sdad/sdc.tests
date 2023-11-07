# Test for adhering to file name conventions

import os
import logging
from pathlib import Path
from enum import Enum
import pandas as pd
from datetime import datetime
import json
import urllib.request
from string import Template
import traceback
from test import Test
import re


def evaluate_folder(dirpath):
    report = ""

    # LOOP THROUGH EACH REPO (SDC. ...) ---------------------
   
    for dir in os.listdir(dirpath):
        subdir = os.path.join(dirpath, dir)
        if not os.path.isdir(subdir):
            continue
        report += "<h3> %s </h3>\n" % (dir)
        
        # CHECK EACH DATA/DISTRIBUTION FILE ------------------------
        
        for path in Path(subdir).rglob("data/distribution/**/*"):
            logging.debug("\tEvaluating: %s" % path.name)

            if not os.path.isfile(path):
                # if path is not a file, skip to the next file to check
                continue

            try:    
                parent_dir = str(path.parent).split('sdc.').pop()
                parent_dir = re.search('/(.*?)/data/distribution', parent_dir).group(1)
            except:
                parent_dir = "PARENT_DIRECTORY"
                       
            full_path = path.name  
                
            # check measure_info files
                
            if path.suffix in [".json"]: 
                
                if full_path not in ["measure_info.json"]:
                    report += "\t<p><font color='#D55E00'> [ERROR: MEASURE INFO FILE NAME] </font> %s: %s</p>\n" % (parent_dir, full_path)
                else: 
                    report += "\t<p><font color='#009E73'> [VALID] </font> %s: %s</p>\n" % (parent_dir, full_path)
                    
            # check data files        
            
            elif path.suffix in [".xz", ".csv"]:
                
                coverage_area = ['ncr', 'va', 'us', 'va013', 'va059']
                resolution = ['bl', 'bg', 'tr', 'nb', 'ct', 'hd', 'co', 'pl', 'pr', 'bz', 'ca', 'ahec']
                data_source = ['acs5', 'lodes', 'pseo', 'qwi', 'mcig', 'hifld', 'ookla', 'webmd', 'sdad', 'abc', 'usda', 'fa', 'acs', 'vdh', 'nchs', 'samhsa', 'schev', 'gmap']
                
                fname = full_path.split('_')
                length = len(fname)
                flag = 0
                
                area = fname[0]
                res = fname[1]
                src = fname[2]
                year = fname[3]
                
                if area not in coverage_area:
                    flag = 1
                    print("Error in coverage area", fname)
                
                if res == 'ahec':
                    continue
                else:
                    for i in range(0, len(res), 2):
                        code = res[i:i+2]
                        if code not in resolution:
                            flag = 1
                            print("Error in resolution", fname)
                            break

                if src not in data_source:
                    flag = 1
                    print("Error in data source", fname)
                
                if not (year.isdigit()):
                    flag = 1

                if flag == 1:
                    report += "\t<p><font color='#D55E00'> [ERROR: DATA FILE NAME] </font> %s: %s</p>\n" % (parent_dir, full_path)
                else: 
                    report += "\t<p><font color='#009E73'> [VALID] </font> %s: %s</p>\n" % (parent_dir, full_path)
                  
            else:  
                report += "\t<p><font color='#D55E00'> [ERROR: DATA FILE NAME] </font> %s: %s</p>\n" % (parent_dir, full_path)
                    
                    
    return report


if __name__ == "__main__":
    test = Test(
        __file__,
        "File Name Test",
        "Checks file name conventions",
    )
    report = evaluate_folder("./data")
    test.export_html(report)

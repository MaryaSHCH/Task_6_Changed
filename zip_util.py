""" 
    This is a utility module for ZIP code assignment
    
    To use this module, first import it:

    import zip_util

    Use the read_zip_all() function to read the data
    on ZIP codes:

    zip_codes = zip_util.read_zip_all()
    print(zip_codes[4108])
    
    Author: Konstantin Kuzmin
    Date: 2/19/2019

"""

import os.path
import math


def read_zip_all():
    i = 0
    header = []
    zip_codes = []
    zip_data = []
    skip_line = False
    # http://notebook.gaslampmedia.com/wp-content/uploads/2013/08/zip_codes_states.csv
    for line in open('zip_codes_states.csv').read().split("\n"):
        skip_line = False
        m = line.strip().replace('"', '').split(",")
        i += 1
        if i == 1:
            for val in m:
                header.append(val)
        else:
            zip_data = []
            for idx in range(0,len(m)):
                if m[idx] == '':
                    skip_line = True
                    break
                if header[idx] == "latitude" or header[idx] == "longitude":
                    val = float(m[idx])
                else:
                    val = m[idx]
                zip_data.append(val)
            if not skip_line:
                zip_codes.append(zip_data)
    return zip_codes

if __name__ == "__main__":
    zip_codes = read_zip_all()
    print(zip_codes[4108])


import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import *


# ******************************************************************************
def main():
    n0debug_calc(Path(__file__))
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")



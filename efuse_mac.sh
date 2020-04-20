#!/bin/bash

# Unfortunately eFUSE burning for the DTM and DPMs is broken after
# Vivado version 2016.3. It is no longer allowed outside of JTAG boot mode.
# We'll use this script to enforce the version used. Sigh.

source /afs/slac/g/reseng/xilinx/vivado_2016.3/Vivado/2016.3/settings64.sh

#vivado -mode batch  -source efuse.tcl -tclargs $@
vivado -mode batch -quiet -nolog -nojournal -notrace -source efuse.tcl -tclargs $@


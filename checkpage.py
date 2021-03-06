#!/bin/env python
#-*-Mode: Python;-*-
## @file
# @brief Accept a series of page IDs or URLs containing page IDs.
# Run checks on the corresponding Confluence pages
# assuming that they describe devices.
# @verbatim
#                               Copyright 2014
#                                    by
#                       The Board of Trustees of the
#                    Leland Stanford Junior University.
#                           All rights reserved.
# @endverbatim
#
# @par Facility:
# DAT
#
# @author
# Stephen Tether <tether@slac.stanford.edu>
#
# @par Date created:
# 2014/03/28
#
# @par Last commit:
# \$Date: 2017-08-04 14:29:49 -0700 (Fri, 04 Aug 2017) $ by \$Author: ruckman $.
#
# @par Revision number:
# \$Revision: 13682 $
#
# @par Location in repository:
# \$HeadURL: file:///afs/slac/g/reseng/svn/repos/hwdb/trunk/checkpage.py $
#
# @par Credits:
# SLAC

# Standard Python library.
import getpass, sys

# HWDB software.
import check, cli, page

def main():
    print "Check device pages in the hardware database in Confluence."
    print "Type control-D or control-C at a prompt to terminate."
    print
    pwd = getpass.getpass("Confluence password for %s: " % getpass.getuser())
    rc = cli.login(getpass.getuser(), pwd, page.SPACE_KEY)
    if rc:
        return 1
    while True:
        print
        ans = raw_input("Enter page ID (or URL with page ID in it): ")
        cid = page.extractPageId(ans)
        if cid is None:
            print "Could not find a page ID in that."
        elif check.validDevicePage(cid):
            print "OK"

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (EOFError, KeyboardInterrupt):
        print
        sys.exit(0)
    except cli.AuthFailure, err:
        print
        sys.exit(err.rc)



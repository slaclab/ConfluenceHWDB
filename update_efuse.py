#!/bin/env python

import getpass, sys, re, argparse
from HTMLParser import HTMLParser
from string import Template

import cli, page, fields
    
def add_efuse(cid, efuse='', force=False, dryrun=False):
        
    p = page.pageFromId(cid)

    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

    efuse_field = []
    if efuse:
        efuse_field.append(fields.EFUSEField(efuse))
    else:
        try:
            efuse_field = fields.buildEFUSEFields()
        except fields.AbortPage:
            print "Page Aborted"
            return False    

    if not efuse_field or not p.addField(efuse_field, force=force):
        print "Couldn't add EFUSE %s - Aborting Page Update"%efuse
        return False    
        
    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

    if dryrun:
        print "Dry Run, not writing to HWDB"
        return True

    return cli.storePage(p.getMarkup(), cid=cid)

def main(args):

    while True:
        try:
            pwd = getpass.getpass("Confluence password for %s: "\
                                      % getpass.getuser())
            rc = cli.login(getpass.getuser(), pwd, page.SPACE_KEY)
            break
        except cli.AuthFailure:
            pass

    if args.page:
        cid = page.extractPageId(args.page)
        if not cid:
            return False
    else:
        while True:
            try:
                cid = page.askForPageId()
                break
            except fields.AbortPage:
                print
                print "-ERROR- Page aborted."
            except KeyboardInterrupt:
                return False

    return add_efuse(cid=cid,efuse=args.efuse,force=args.force, dryrun=args.dryrun)

if __name__ == "__main__":

    desc = """ 
This program is used to update/add EFUSE value fields to the 
Hardeware Database.
"""
    epilog = """
Parameters that are not supplied on the command line will be prompted for.

The KEYWORD for searching for a page can be the pageId, URL, Short URL, 
AssetTag, Page Title, or other identifying content. It may need to be quoted. 
"""

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-e", "--efuse", metavar="EFUSE",
                        help="EFUSE to assign")
    parser.add_argument("-p", "--page",
                        help="Search term for HWDB page", 
                        metavar="KEYWORD")
    parser.add_argument("-f", "--force", help="Allow overwriting of existing values",
                        action="store_true")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="Do not save new page to HWDB")

    args = parser.parse_args()

    sys.exit(main(args))

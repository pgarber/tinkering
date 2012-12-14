#!/usr/bin/env python
import gzip
import sys
import yum
from yum.update_md import UpdateMetadata, UpdateNotice

from optparse import OptionParser

def parse_updateinfo(input):
    um = UpdateMetadata()
    if input.endswith(".gz"):
        f = gzip.GzipFile(input, 'r')
        um.add(f)
    else:
        um.add(input)
    notices = []
    count = 0
    for info in um.get_notices():
        md = info.get_metadata()
        notices.append(md)
        count += 1
        print "Count %s:  %s" % (count, md['title'])
    return notices


if __name__ == "__main__":
    parser = OptionParser(description="Parse errata information")
    parser.add_option("--file", action="store", help="Updateinfo.xml file to parse", default=None)
    (opts, args) = parser.parse_args()

    if opts.file is None:
        print "Please re-run with '--file' specified" 
        sys.exit(1)

    parse_updateinfo(opts.file)


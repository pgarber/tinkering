#!/usr/bin/env python
import sys
from find_errata import init, find_errata
from optparse import OptionParser

from pulp_rpm.yum_plugin import updateinfo

def translate_to_unit(errata):
    class Unit(object):
        def __init__(self, id, metadata):
            self.unit_key = {"id":id}
            self.metadata = metadata
    return Unit(errata["id"], errata)

def form_xml(errata_unit, outdir):
    updateinfo.updateinfo([errata_unit], outdir)

if __name__ == "__main__":
    parser = OptionParser(description="Find an errata by ID in mongo")
    parser.add_option("--id", action="store", help="Errata ID", default=None)
    parser.add_option("--db_name", action="store", help="MongoDB Database Name", default="pulp_database")
    parser.add_option("--outdir", action="store", help="Output directory, defaults to './'", 
            default="./")
    (opts, args) = parser.parse_args()

    if not opts.id:
        print "Please re-run with --id"
        sys.exit(1)
    errata_id = opts.id
    outdir = opts.outdir
    db = init(opts.db_name)
    errata = find_errata(db, errata_id)
    if not errata:
        print "Unable to find errata for ID: %s" % (errata_id)
        sys.exit(1)
    errata_unit = translate_to_unit(errata) 
    form_xml(errata_unit, outdir)
    print "XML output written to: %s" % (outdir)

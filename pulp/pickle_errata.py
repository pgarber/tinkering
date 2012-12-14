#!/usr/bin/env python

from optparse import OptionParser

from find_errata import init, find_errata
import pickle

def pickle_errata(db, errata_id, output_file):
    errata = find_errata(db, errata_id)
    if not errata:
        return False
    f = open(output_file, 'w')
    try:
        pickle.dump(errata, f)
    finally:
        f.close()
    return True

if __name__ == "__main__":
    parser = OptionParser(description="Find an errata by ID in mongo")
    parser.add_option("--id", action="store", help="Errata ID", default=None)
    parser.add_option("--db_name", action="store", help="MongoDB Database Name", default="pulp_database")
    parser.add_option("--out", action="store", help="Output file to store pickled errata", default="errata.pkl")
    (opts, args) = parser.parse_args()
    if not opts.id:
        print "Please re-run with --id specified"
    db = init(db_name=opts.db_name)
    if pickle_errata(db, opts.id, opts.out):
        print "Errata has been pickled to: %s" % (opts.out)
    else: 
        print "Error pickling errata"


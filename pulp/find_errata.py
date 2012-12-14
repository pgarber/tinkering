#!/usr/bin/env python

from optparse import OptionParser
from pymongo import Connection
from pymongo.son_manipulator import AutoReference, NamespaceInjector

def init(db_name):
    connection = Connection()
    db = getattr(connection, db_name)
    db.add_son_manipulator(NamespaceInjector())
    db.add_son_manipulator(AutoReference(db))
    return db

def find_errata(db, errata_id, collection_name="units_erratum"):
    coll = getattr(db, collection_name)
    result = coll.find({"id":errata_id})
    if result and result.count() > 0:
        return result[0]
    else:
        return None

if __name__ == "__main__":
    parser = OptionParser(description="Find an errata by ID in mongo")
    parser.add_option("--id", action="store", help="Errata ID", default=None)
    parser.add_option("--db_name", action="store", help="MongoDB Database Name", default="pulp_database")
    (opts, args) = parser.parse_args()
    if not opts.id:
        print "Please re-run with --id specified"
    db = init(db_name=opts.db_name)
    errata = find_errata(db, opts.id)
    if not errata:
        print "No errata found for errata id: %s" % (opts.id)
    else:
        print errata

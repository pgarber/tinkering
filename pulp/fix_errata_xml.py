#!/usr/bin/env python

from optparse import OptionParser

import pickle
import sys
from pulp_rpm.yum_plugin import updateinfo

from create_updateinfoxml import translate_to_unit

import yum

def find_closing_pkglist_tags(blob):
    tag_indexes = []
    curr_index = 0
    while True:
        result = blob.find("</pkglist>", curr_index)
        if result < 0:
            break
        tag_indexes.append(result)
        curr_index = result + 1
    return tag_indexes

def fix_xml(blob):
    closing_pkglist_indexes = find_closing_pkglist_tags(blob)
    fixed_blob = ""
    # Remove all but last closing pkglist tag
    if len(closing_pkglist_indexes) > 1:
        # We want to form a new list ignoring the last element which is the closing tag we want to keep
        sub_set_tag_indexes = closing_pkglist_indexes[0:(len(closing_pkglist_indexes)-1)]
        len_closing_tag = len("</pkglist>")
        start_index = 0
        for end_index in sub_set_tag_indexes:
            fixed_blob += blob[start_index:end_index]
            start_index = end_index+len_closing_tag
        fixed_blob += blob[start_index:]
        return fixed_blob
    else:
        return blob

def remove_extra_pkglist_closing_tag(self):
    # Assumes that the XML should be formated with only one <pkglist>...</pkglist>
    # Therefore all extra </pkglist> beyond the final closing tag are invalid
    orig_xml = YUM_UPDATE_MD_UPDATE_NOTICE_ORIG_XML_METHOD(self)
    fixed_xml = fix_xml(orig_xml)
    return fixed_xml

YUM_UPDATE_MD_UPDATE_NOTICE_ORIG_XML_METHOD = yum.update_md.UpdateNotice.xml
yum.update_md.UpdateNotice.xml = remove_extra_pkglist_closing_tag


def form_xml(errata_unit, outdir):
    updateinfo.updateinfo([errata_unit], outdir)

def load_errata_from_pickle(input_file):
    f = open(input_file, 'r')
    try:
        try:
            errata = pickle.load(f)
        finally:
            f.close()
    except Exception, e:
        print e
        return None
    return errata

if __name__ == "__main__":
    parser = OptionParser(description="Find an errata by ID in mongo")
    parser.add_option("--pickle", action="store", help="Pickled errata file", default=None)
    parser.add_option("--outdir", action="store", help="Output directory, defaults to './'", 
            default="./")
    (opts, args) = parser.parse_args()
    if not opts.pickle:
        print "Please re-run with --pickle specified"
    errata = load_errata_from_pickle(opts.pickle)
    if not errata:
        print "Failed load errata"
        sys.exit(1)
    errata_unit = translate_to_unit(errata)
    form_xml(errata_unit, opts.outdir)
    print "Wrote XML file 'updateinfo.xml' to %s" % (opts.outdir)

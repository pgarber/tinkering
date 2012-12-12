#!/usr/bin/env python

import datetime
import os
import yum
import sys
import tempfile
import time
from optparse import OptionParser

def create_yum_repo(label, repo_url, repo_dir=None):
    repo = yum.yumRepo.YumRepository(label)
    repo.basecachedir = repo_dir
    repo.base_persistdir = repo_dir
    repo.cache = 0
    repo.metadata_expire = 0
    repo.baseurl = [repo_url]
    repo.baseurlSetup()
    return repo

def process_metadata(repo):
    for ftype in repo.repoXML.fileTypes():
        print "Fetching: %s" % (ftype)
        repo.retrieveMD(ftype)

def get_package_list(repo, newest=False):
    sack = repo.getPackageSack()
    sack.populate(repo, 'metadata', None, 0)
    if newest:
        return sack.returnNewestByNameArch()
    return sack.returnPackages()

if __name__ == "__main__":
    parser = OptionParser(description="Tool to download yum repo metadata and display # of available packages")
    parser.add_option("--url", action="store", help="URL of source repository", default=None)
    parser.add_option("--dir", action="store", help="Directory to store metadata in", default="./output")
    parser.add_option("--label", action="store", help="Label", default="yum_repo_metadata_%s" % (datetime.datetime.now().strftime("%d_%m_%y_%H%M_%S")))
    (opts, args) = parser.parse_args()
    
    label = opts.label
    repo_url = opts.url
    repo_dir = opts.dir
    if not repo_url:
        print "Please re-run with --url"
        sys.exit(1)

    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    repo = create_yum_repo(label, repo_url, repo_dir)
    print "Begin download of metadata from: %s" % (repo_url)
    a = time.time()
    process_metadata(repo)
    b = time.time()
    packages = get_package_list(repo)
    c = time.time()
    print "%s seconds to download metadata" % (b - a)
    print "%s seconds to parse metadata" % (c - b)
    print "%s total time" % (c - a)
    print "YUM Repository Metadata for %s has been saved at: %s" % (repo_url, os.path.join(repo_dir, label))
    print "%s packages are available" % (len(packages))

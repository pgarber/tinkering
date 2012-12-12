#!/usr/bin/env python

import datetime
import yum
import sys
import tempfile
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
    parser.add_option("--dir", action="store", help="Directory to store metadata in", default=None)
    parser.add_option("--label", action="store", help="Label", default="yum_repo_metadata_%s" % (datetime.datetime.now().strftime("%d_%m_%y_%H%M")))
    (opts, args) = parser.parse_args()

    label = opts.label
    repo_url = opts.url
    if not repo_url:
        print "Please re-run with --url"
        sys.exit(1)
    repo_dir = opts.dir
    if not repo_dir:
        repo_dir = "./"
    repo = create_yum_repo(label, repo_url, repo_dir)
    process_metadata(repo)
    packages = get_package_list(repo)

    print "YUM Repository Metadata for %s has been saved at: %s" % (repo_url, repo_dir)
    print "%s packages are available" % (len(packages))

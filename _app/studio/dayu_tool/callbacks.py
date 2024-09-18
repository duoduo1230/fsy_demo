#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero.core as hcore
import hiero.ui as hui
import hiero.core.VersionScanner as VS
from db.disk_path import DiskPath

if not hasattr(VS.VersionScanner, "default_filterVersion"):
    VS.VersionScanner.default_filterVersion = VS.VersionScanner.filterVersion
if not hasattr(VS.VersionScanner, "default_versionLessThan"):
    VS.VersionScanner.default_versionLessThan = VS.VersionScanner.versionLessThan
if not hasattr(VS.VersionScanner, "default_findNewVersions"):
    VS.VersionScanner.default_findNewVersions = VS.VersionScanner.findNewVersions
if not hasattr(VS.VersionScanner, 'default_doScan'):
    VS.VersionScanner.default_doScan = VS.VersionScanner.doScan
if not hasattr(VS.VersionScanner, 'default_findVersionFiles'):
    VS.VersionScanner.default_findVersionFiles = VS.VersionScanner.findVersionFiles


def db_find_version_files(self, version, orm=None, formats=None):
    print 'db_find_version_files'
    binitem = version.parent()
    origfilename = DiskPath(self.getFilename(version))
    self._origextension = origfilename.ext
    foundVersions = self.findNewVersions(version, orm=orm, formats=formats)
    foundVersions = filter(lambda v: self.filterVersion(binitem, v), foundVersions)
    foundVersions = self.sortVersions(foundVersions)

    return foundVersions


def db_do_scan(self, version, orm=None, formats=None):
    print 'db_do_scan'
    if orm is None:
        foundVersionFiles = self.findVersionFiles(version, formats=formats)
        binitem = version.parent()
        newVersions = self.insertVersions(binitem, foundVersionFiles)
        return newVersions
    else:
        found_versions = self.findNewVersions(version, orm=orm, formats=formats)
        binitem = version.parent()
        newVersions = self.insertVersions(binitem, found_versions)
        return newVersions


def db_find_new_versions(self, version, orm=None, formats=None):
    print 'db_find_new_versions'
    file_set = set()
    all_orms = None
    version_path = DiskPath(version.item().mediaSource().fileinfos()[0].filename())
    # print version_path
    if orm:
        print 'using scan database (with orm)'
        level = version_path.replace(orm.disk_path, '').strip('/').split('/')[0]
        all_versions = [x for x in orm.parent.sub_files if level in x.sub_level._structure]
    else:
        print 'using scan database (parse file path)'
        orm = version_path.orm(disk_type='publish')
        if orm:
            level = '/'.join(version_path.replace(orm.disk_path(), '').strip('/').split('/')[:-1])
            for v in orm.parent.sub_files:
                for s in v.sub_level.walk(collapse=True):
                    if level in s.filename:
                        file_set.add(s.filename)

    if file_set:
        self.using_db = True
        pass
    else:
        print 'using scan disk'
        file_set = self.default_findNewVersions(version)

    return file_set


def db_filter_version(self, binItem, newVersionFile, active_version=None, formats=None):
    # print 'db_filter_version'
    # todo: a better way to check if file exists?
    if getattr(self, 'using_db'):
        print '===== filter using db ===='
        av = active_version \
            if active_version \
            else DiskPath(binItem.activeItem().mediaSource().fileinfos()[0].filename())

        orm = av.orm()
        if orm:
            sub_level = av.parent.replace(orm.disk_path(), '').strip('/')
            new_path = DiskPath(newVersionFile)
            new_sub_level = new_path.parent.replace(new_path.orm().disk_path(), '').strip('/')
            print sub_level, new_sub_level
            return self.default_filterVersion(binItem, newVersionFile) and sub_level == new_sub_level

    return self.default_filterVersion(binItem, newVersionFile)


VS.VersionScanner.filterVersion = db_filter_version
VS.VersionScanner.findNewVersions = db_find_new_versions
VS.VersionScanner.findVersionFiles = db_find_version_files
VS.VersionScanner.doScan = db_do_scan

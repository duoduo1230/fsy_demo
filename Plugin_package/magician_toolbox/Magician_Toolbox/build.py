#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build Windows python2 rez package."""
# Import built-in modules
import os
import shutil
import stat


class FileAlreadyExistError(Exception):
    """When the file already exist."""
    pass


class Builder(object):
    """Copy all files into package root."""

    def __init__(self):
        """Initialize builder."""
        self.build_path = os.environ["REZ_BUILD_PATH"]
        self.install_path = os.environ["REZ_BUILD_INSTALL_PATH"]
        self.name = os.environ["REZ_BUILD_PROJECT_NAME"]
        self.version = os.environ["REZ_BUILD_PROJECT_VERSION"]
        self.source_path = os.environ["REZ_BUILD_SOURCE_PATH"]
        self.variant_index = os.environ["REZ_BUILD_VARIANT_INDEX"]
        self.workspace = os.path.join(self.build_path, "workspace")

    def build(self):
        """Build rez package."""
        self.create_work_dir()
        self.copy_tree(self.source_path, self.workspace, dirs_exist_ok=True)
        self.install()

    def create_work_dir(self):
        """Create the work directory.

        If the work directory already exists, remove the old one and create it.
        """
        if os.path.exists(self.workspace):
            self.remove_tree(self.workspace)
        os.makedirs(self.workspace)

    def install(self):
        """Copy files from work directory to self.install_path."""
        if os.environ.get("REZ_BUILD_INSTALL") == "1":
            if os.path.exists(self.install_path):
                self.remove_tree(self.install_path)
            shutil.copytree(self.workspace, self.install_path, symlinks=True)

    def copy_tree(self, src, dst, dirs_exist_ok=False, follow_symlinks=True, file_overwrite=False):
        """
        """
        if not dirs_exist_ok or not os.path.exists(dst):
            shutil.copytree(src, dst, symlinks=follow_symlinks, ignore=lambda path, files: ["build"])
        else:
            for file in os.listdir(src):
                src_ = os.path.join(src, file)
                dst_ = os.path.join(dst, file)
                if file == "build" and os.path.isdir(src_):
                    continue
                if os.path.isfile(src_) or os.path.islink(src_):
                    if not os.path.exists(dst_):
                        shutil.copy2(src_, dst_)
                    elif os.path.exists(dst_) and file_overwrite:
                        shutil.copy2(src_, dst_)
                    else:
                        raise FileAlreadyExistError(
                            "File {dst_} already exist. Set the file_overwrite as True if you want overwrite it.".format(
                                dst_=dst_))
                else:
                    self.copy_tree(
                        src_, dst_, dirs_exist_ok=dirs_exist_ok, follow_symlinks=follow_symlinks,
                        file_overwrite=file_overwrite)

    @staticmethod
    def remove_tree(path):
        """Remove directory.

        Args:
            path (str): The directory to remove.
        """
        def rm_readonly(func, path_, _):
            """Remove read-only files on Windows.

            Reference from https://stackoverflow.com/questions/1889597 and
            https://github.com/ansible/ansible/issues/34335

            Args:
                func (function): Function which will remove the file/folder.
                path_ (str): Path to file/folder which should be removed.
                _: ignore.
            """
            os.chmod(path_, stat.S_IWRITE)
            func(path_)

        shutil.rmtree(path, onerror=rm_readonly)


if __name__ == '__main__':
    Builder().build()
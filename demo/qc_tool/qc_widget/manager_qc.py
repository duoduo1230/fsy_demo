# -*- coding: utf-8 -*-

import os
from pathlib import Path
from importlib.machinery import SourceFileLoader

from traceback import format_exc

class MyQC():

    error_qc = []
    @staticmethod
    def run_all(qc_instance_list):
        error_result = []
        for qc in qc_instance_list:
            try:
                result = qc.run()
                if not result:
                    error_result.append(qc)
            except:
                print(format_exc())

        return error_result

    @staticmethod
    def repair(qc_instance_list):
        for qc in qc_instance_list:
            result = qc.repair()

    @staticmethod
    def get_qc_items(path):
        # 此处获取质检项环节的分类
        folder = Path(path)
        module_list = folder.glob("*.py")
        result = []
        for md in module_list:
            result.append(md.stem)
        return result

    @staticmethod
    def import_module(py_path):
        """
        Import python module from python file.
        """
        name = py_path.stem
        module = SourceFileLoader(name, py_path.__str__()).load_module()
        # Doesn't have "get_qc" function
        if not hasattr(module, "get_qc"):
            return

        instance = module.get_qc()
        # Doesn't have "run" function
        if not hasattr(instance, "run"):
            return

        return instance


if __name__ == "__main__":
    MyQC.import_module()

    detail_information_titel = {
        'Usage:': 'Usage',
        'Result': 'result',
        'Info': 'info'
    }





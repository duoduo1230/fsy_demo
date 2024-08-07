# -*- coding: utf-8 -*-

class CheckNamespace(object):
    name = 'Validate Namespace'

    def __init__(self):
        super().__init__()

    def run(self):
        print("run")
        return False
        import pymel.core as pm
        namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        namespaces.remove("UI")
        namespaces.remove("shared")
        namespaces.sort(reverse=True)

        for name_space in namespaces:
            try:
                pm.namespace(moveNamespace=[name_space, ":"], force=True)
                pm.namespace(removeNamespace=name_space)
            except:
                pass

        return True

    def repair(self, *args, **kwargs):
        print("repair")

def get_qc():
    return CheckNamespace()




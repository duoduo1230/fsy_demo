# -*- coding: utf-8 -*-

class CheckReference():
    name = 'Remove Reference'
    Usage = 'Delete useless reference files'

    def __init__(self):
        super().__init__()

    def run(self):
        import maya.cmds as cmds
        self.error_message = ''
        self.all_reference = cmds.ls(type='reference')
        print('There are Referenced files')
        print(self.all_reference )
        return self.all_reference   

    def repair(self, *args, **kwargs):
        import maya.cmds as cmds
        import pymel.core as pm
        for reference in self.all_reference:
            if not cmds.referenceQuery(reference, isLoaded=True):
                cmds.file(removeReference=True, referenceNode=reference)
        print('The referenced file has been deleted')

        if not self.all_reference:
            print('None')
        else:
            for refer_node in self.all_reference:
                # Reference file path not found
                if refer_node.referenceFile() == None:
                    refer_node.unlock()
                    pm.delete(refer_node)
                    continue
                # This reference file does not have a parent reference, remove the reference
                if not refer_node.parentReference():
                    import pymel.core as pm
                    pm.FileReference(refer_node).remove()

def get_qc():
    return CheckReference()




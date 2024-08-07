# -*- coding: utf-8 -*-

class CheckHistory():
    name = 'Clear Polygon History'

    def __init__(self):
        super().__init__()
        self.error_mesh = []
        self.extra_data = []
        self.check_info = ''

    def get_all(self):
        import pymel.core as pm
        base_paths = ['|ASSET']
        for base_path in pm.ls(base_paths, type='mesh', dag=1):
            yield base_path

    def run(self):
        intermediateObjects = 1
        self.error_message = ''
        self.history_nodes = []
        self.intermediate_object = []
        result = True
        for shape in self.get_all():
            if shape.intermediateObject.get():
                print(u'This shape node is an intermediate object')
                self.intermediate_object.append(shape)
                result = False
                continue

            if shape.inputs():
                print('Nodes with history')
                self.history_nodes.append(shape)
                result = False
        print(self.history_nodes)

        return result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import app._maya.util as util

        error_nodes = []

        for shape in self.history_nodes:
            try:
                pm.delete(shape, ch=1)
                for attr_tuple in shape.inputs(c=1, p=1):
                    pm.disconnectAttr(attr_tuple[1], attr_tuple[0])
            except:
                error_nodes.append(shape)

        for intermediate_shape in self.intermediate_object:
            try:
                if intermediate_shape.isLocked():
                    intermediate_shape.unlock()
                pm.delete(intermediate_shape)
            except:
                error_nodes.append(intermediate_shape)

        if error_nodes:
            util.message(u'Cannot be repaired', dialog=True)

def get_qc():
    return CheckHistory()




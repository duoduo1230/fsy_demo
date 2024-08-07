# -*- coding: utf-8 -*-

class OverlayMesh():
    name = 'Overlay Mesh'

    def __init__(self):
        super().__init__()
        self.error_mesh = []
        self.extra_data = []
        self.check_info = ''

    def get_all(self,):
        import pymel.core as pm
        re = []
        temp = [shape_node.parent(0) for shape_node in pm.ls(type='mesh', dag=1, noIntermediate=1)]
        re.append(temp)
        return re

    def run(self):
        import pymel.core as pm

        for level in self.get_all():
            overlay_mesh = {}
            overlay_mesh['vernum'] = {}
            overlay_mesh['verposition'] = {}
            for node in level:
                print(node)
                x, y, z, xx, yy, zz = pm.xform(node, q=1, ws=1, bb=1)
                bb = '%.3f' % x + ',' + '%.3f' % y + ',' + '%.3f' % z + ',' + '%.3f' % xx + ',' + '%.3f' % yy + ',' + '%.3f' % zz
                overlay_mesh['vernum'].setdefault((bb, node.numVertices()), []).append(node)

            for tran_num, node_list in overlay_mesh['vernum'].items():
                if len(node_list) > 1:
                    ver_num = tran_num[1]
                    import random
                    count = 20 if ver_num > 20 else ver_num
                    random_ver = random.sample(range(ver_num), count)
                    for num_node in node_list:
                        for index in random_ver:
                            num_node_ver = num_node.vtx[index]
                            overlay_mesh['verposition'].setdefault(num_node_ver.getPosition().get(), []).append(
                                num_node)

                    result = True
                    for ver_position, same_ver_position in overlay_mesh['verposition'].items():
                        if len(same_ver_position) < 2:
                            result = False
                            break
                    if result:
                        self.extra_data.extend(same_ver_position)

        if self.extra_data:
            for overlay_node in self.extra_data:
                self.error_mesh.append(overlay_node)
            self.check_info = '{} There are duplicate models present'.format(self.error_mesh)
            return False
        else:
            self.check_info = 'Quality inspection passed'
            return True

    def repair(self):
        if self.extra_data:
            import pymel.core as pm
            pm.select(self.extra_data)
            self.check_info = 'Select duplicate models'

def get_qc():
    return OverlayMesh()
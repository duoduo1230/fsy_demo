# -*- coding: utf-8 -*-

class OverlayMesh():

    def __init__(self):
        super().__init__()
        self.description = u'检查重复模型'
        self.error_message = u''
        self.check_result = ''

        self.extra_data = []

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

                    for ver_position, same_ver_position in overlay_mesh['verposition'].items():
                        if len(same_ver_position) >= 2:
                            self.extra_data.extend(same_ver_position)

        self.extra_data = set(self.extra_data)
        if self.extra_data:
            self.error_message = u'存在重复模型{}'.format(self.extra_data)
            self.check_result = 'FAILED'
        else:
            self.error_message = u''
            self.check_result = 'PASSED'

        return self.error_message, self.check_result

    def repair(self):
        if self.extra_data:
            import pymel.core as pm
            pm.select(self.extra_data)
            self.error_message = u'已选中重复模型'
            self.check_result = 'EXCEPTION'

        return self.error_message, self.check_result

def get_qc():
    return OverlayMesh()
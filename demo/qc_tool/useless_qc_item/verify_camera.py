# -*- coding: utf-8 -*-

class CheckReference():

    def __init__(self):
        super().__init__()
        self.description = u'校验相机Fit Resolution Gate属性，是否设置为Horizontal'
        self.error_message = ''
        self.check_result = ''

    def run(self):
        import pymel.core as pm
        self.extra_data = []
        all_reference_nodes = pm.ls(rf=1)
        all_reference_names = [node for node in all_reference_nodes if not node.isLoaded()]
        self.extra_data = [node.name() for node in all_reference_nodes if not node.isLoaded()]
        if all_reference_names:
            self.error_message = u'未加载的reference {}'.format(all_reference_names)
            self.check_result = 'FAILED'

        else:
            self.check_result = 'PASSED'

        return self.error_message, self.check_result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.extra_data:
            for refer_node in self.extra_data:
                pm.FileReference(refer_node).remove()
        self.error_message = u'未引用文件已删除'
        self.check_result = 'PASSED'

        return self.error_message, self.check_result

def get_qc():
    return CheckReference()




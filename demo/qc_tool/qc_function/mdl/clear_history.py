# -*- coding: utf-8 -*-

class CheckHistory():

    def __init__(self):
        super().__init__()
        self.description = u'清除mesh历史'
        self.error_message = u''
        self.check_result = ''

        self.extra_data = []
        self.intermediate_obj = []
        self.history_obj = []

    def get_all(self):
        import pymel.core as pm
        for base_path in pm.ls(type='mesh', dag=1):
            yield base_path

    def run(self):
        for shape in self.get_all():
            if shape.intermediateObject.get():
                self.intermediate_obj.append(shape)
            if shape.inputs():
                self.history_obj.append(shape)

        if self.intermediate_obj or self.history_obj:
            self.extra_data = self.intermediate_obj + self.history_obj
            self.error_message = u'历史操作存在 {}'.format(self.extra_data)
            self.check_result = 'FAILED'
        else:
            self.check_result = 'PASSED'

        return self.error_message, self.check_result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        error_nodes = []
        for shape in self.history_obj:
            try:
                pm.delete(shape, ch=1)
                for attr_tuple in shape.inputs(c=1, p=1):
                    pm.disconnectAttr(attr_tuple[1], attr_tuple[0])
            except:
                error_nodes.append(shape)

        for intermediate_shape in self.intermediate_obj:
            try:
                if intermediate_shape.isLocked():
                    intermediate_shape.unlock()
                pm.delete(intermediate_shape)
            except:
                error_nodes.append(intermediate_shape)

        if error_nodes:
            self.error_message = '不能修复，请亲自检查'
            self.check_result = 'EXCEPTION'

        else:
            self.error_message = '历史信息已删除'
            self.check_result = 'PASSED'

        return self.error_message, self.check_result


def get_qc():
    return CheckHistory()




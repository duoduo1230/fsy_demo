# -*- coding: utf-8 -*-

class CheckNamespace(object):

    def __init__(self):
        super().__init__()
        self.description = u'检查当前场景是否存在命名空间'
        self.check_info = ''
        self.check_result = ''

    def run(self):
        import pymel.core as pm
        self.extra_data = []
        namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        namespaces.remove("UI")
        namespaces.remove("shared")
        namespaces.sort(reverse=True)
        if namespaces:
            self.extra_data = namespaces
            self.check_info = u'存在命名空间 {}'.format(namespaces)

            self.check_result = 'FAILED'

        else:
            self.check_result = 'PASSED'

        return self.check_info, self.check_result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        error_list = []
        if self.extra_data:
            for name_space in self.extra_data:
                try:
                    pm.namespace(moveNamespace=[name_space, ":"], force=True)
                    pm.namespace(removeNamespace=name_space)
                except:
                    error_list.append(name_space)

            if error_list:
                self.check_info = u'该命名空间不能修复 {}'.format(error_list)
                self.check_result = 'EXCEPTION'

            else:
                self.check_result = 'PASSED'

        return self.check_info, self.check_result



def get_qc():
    return CheckNamespace()




# -*- coding: utf-8 -*-

class CheckUV():

    def __init__(self):
        super().__init__()
        self.description = u'修复法线'
        self.error_message = u''
        self.check_result = ''

    def get_all(self, *args, **kwargs):
        import pymel.core as pm
        return pm.ls(type='mesh', dag=1)

    def run(self):
        import pymel.core as pm
        all_nodes = self.get_all()
        if all_nodes:
            try:
                pm.refresh(suspend=True)
                pm.select(all_nodes)
                # 使用 polyNormalPerVertex 命令锁定法线，ufn=1 表示解锁法线。
                pm.polyNormalPerVertex(ufn=1)
                # 使用 MEL 命令删除历史记录。
                pm.mel.eval('DeleteHistory')
                pm.refresh(suspend=False)
                self.check_result = 'PASSED'
            except:
                self.check_result = 'EXCEPTION'
                self.error_message = u'法线锁定请手动修复'

        return self.error_message, self.check_result

    def repair(self, *args, **kwargs):
        pass

def get_qc():
    return CheckUV()




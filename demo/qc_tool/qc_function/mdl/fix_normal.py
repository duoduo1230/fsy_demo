# -*- coding: utf-8 -*-

class CheckUV():
    name = 'Check UV'

    def __init__(self):
        super().__init__()
    def get_all(self, *args, **kwargs):
        import pymel.core as pm
        base_paths = ['|ASSET', '|SCENE']
        return pm.ls(base_paths, type='mesh', dag=1)

    def run(self):
        import pymel.core as pm
        self.error_message = ''
        try:
            pm.refresh(suspend=True)
            all_nodes = self.get_all()
            pm.select(all_nodes)
            pm.polyNormalPerVertex(ufn=1)
            pm.mel.eval('DeleteHistory')
            pm.refresh(suspend=False)
            return True
        except Exception as e:
            print(e)
            self.error_message += u'There is a normal lock, please manually fix it'
            return False

    def repair(self, *args, **kwargs):
        pass

def get_qc():
    return CheckUV()




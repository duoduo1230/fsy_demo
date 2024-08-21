# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase
try:
    import pymel.core as pm
except:
    pass

element_info_config = {
    # 环节: element type
    'rig': 'mdl',
    'srf': 'mdl',
    'ldev': 'mdl',

}


class CheckAsset(MQCBase):
    name = 'Check Asset'
    usage = u'检查层级命名层级点线面数量'

    def __init__(self, parent=None):
        super(CheckAsset, self).__init__(parent)
        from ui_center.widgets import MAppContext
        self.context = MAppContext.MAppContext()
        self.current_step = self.context.current_step
        self.map_step = element_info_config.get(self.current_step,None)
        from app.utils import which_app
        self.app_name = which_app()
        self.extra_data = []
        self.error_message = ''
        self.qc_statu = True
        self.tab_space = '&nbsp;&nbsp;&nbsp;&nbsp;'

    def validate(self, options):
        if self.app_name != 'maya':
            return False
        if options.get('type_group') in ['element'] and options.get('type') in ['srf', 'rig']:
            import db
            if db.util.get_current_user().name in ['wuqingjun','yangzhuo','muyanru']:
                return False
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        version_orm, asset_orm = self.get_asset_orm_from_work_file()
        if not version_orm:
            self.error_message = u'当前工程文件没有在dayu流程内'
            return False

        # 生成当前工程文件得 层级信息
        from app._maya import util as mutil
        asset_hierarchy_info = self.get_hierarchy_info()

        # 拿到对应orm下的 compare jason 文件
        map_step = element_info_config.get(self.current_step)
        comment = u'发现该资产下存在多个resource element，请选择需要作比较得{}类型element:'.format(self.map_step) # todo comment
        element_map_orm = mutil.get_element_from_asset(map_step, asset_orm.id,comment=comment)

        if not element_map_orm:
            return True
        element_asset_hierarchy_info = self.get_element_hierarchy_info(element_map_orm)

        # 也有可能 hierarchy_info 文件没有拿到 暂时直接通过
        # 可能是因为 之前的资产 也可能是没有提交 element 就没有拿到
        # 如果没有拿到对应orm 信息， 跳过此qc
        if not element_asset_hierarchy_info:
            return True
        # 拿到信息， 进行对比
        return self.check_hierarchy_info(asset_hierarchy_info, element_asset_hierarchy_info)

    @staticmethod
    def get_element_hierarchy_info(element_orm):
        """
        todo 拿到对应element 对比参考文件
        :param element_orm: ldev orm 或者 rig orm
        :return: <dict> 对比文件中得字典信息
        """
        # 如果对比文件不存在的时候 返回空
        import json
        compare_json = element_orm.disk_path(disk_type='publish').child('compare.json')
        if not compare_json.exists():
            return None

        with open(compare_json, 'r') as f:
            hierarchy_info = json.load(f)

        return hierarchy_info

    @staticmethod
    def get_asset_orm_from_work_file():
        """
        返回 orm 或者 None
        :return:
        """
        from db.disk_path import DiskPath
        version_orm = DiskPath(pm.sceneName()).orm(disk_type='work')
        asset_orm = DiskPath(pm.sceneName()).ancestor(5).orm(disk_type='work')
        return (version_orm, asset_orm) or (None, None)

    @staticmethod
    def get_hierarchy_info():
        """
        生成当前工程文件得 层级信息
        :return:
        """
        from app._maya.tools import compare_mesh
        reload(compare_mesh)
        hierarchy_info = compare_mesh.get_hierarchy_info()
        return hierarchy_info

    def check_hierarchy_info(self, current_info, check_info):
        """
        对比这两个字典信息 如果这两字典一样返回 True 否则 返回 False 并添加出 错误信息
        :param current_info: 当前工程文件得 层级信息
        :param check_info:  需要对比得工程文件信息
        :return: <bool>
        """
        # 检查字典结构是否一模一样 层级结构是否一模一样
        if current_info == check_info:
            self.error_message = u'当前{}和{}文件层级结构以及模型点线面数量完全一模一样'.format(self.current_step,self.map_step)
            return True

        # 检查层级  求出交集的层级， 非交集层级输出到错误信息里)
        # other 层级结构里面的信息不做对比
        check_hie_info = [ch for ch in check_info.keys() if '|GEO|HIG|' in ch]
        current_hie_info = [ch for ch in current_info.keys() if '|GEO|HIG|' in ch]
        intersections = self.check_hierarchy(current_hie_info, check_hie_info)

        # 检查相同层级下的 mesh 和 transform 信息 是否一致
        for inter in intersections:
            # todo 对比其中的单个层级里面的 变换信息 和点线面信息
            current_hierarchy_info = current_info.get(inter)
            check_hierarchy_info = check_info.get(inter)
            # 如果是transform 节点
            if current_hierarchy_info.get('type') == 'transform':
                self.check_translate(inter, current_hierarchy_info.get('transform'), check_hierarchy_info.get('transform'))

            # 如果是mesh形态节点
            elif current_hierarchy_info.get('type') == 'mesh':
                self.check_meshinfo(inter, current_hierarchy_info.get('mesh_info'), check_hierarchy_info.get('mesh_info'))

        return self.qc_statu

    def check_hierarchy(self, current_hierarchy_list, check_hierarchy_list):
        """
        只处理层级结构 需要两边对比 会存在 A集合里面有得 B集合里面没有 B集合里面有得 A集合里面没有
        因为都是扫描固定层级记录出的信息，所以两个文件信息都是以 |ASSET 作为key值
        :param current_hierarchy_list: 当前工程文件有哪些层级结构
        :param check_hierarchy_list: 对比文件有哪些层级结构
        :return: 返回两边集合得 交集信息
        """
        intersections = set(current_hierarchy_list) & set(check_hierarchy_list)
        different_current = set(current_hierarchy_list) - set(check_hierarchy_list)
        different_check = set(check_hierarchy_list) - set(current_hierarchy_list)

        template = u'<br/>==== {}层级里没有{}层级里的以下层级 ==== <br/>' + self.tab_space

        if different_current:
            current_info = template.format(element_info_config[self.current_step], self.current_step)
            msg = current_info + ('<br/>' + self.tab_space).join(list(different_current)) + '<br/>'
            self.error_message += msg
            self.qc_statu = False
        if different_check:
            check_info = template.format(self.current_step, element_info_config[self.current_step])
            msg = check_info + ('<br/>' + self.tab_space).join(list(different_check)) + '<br/>'
            self.error_message += msg
            self.qc_statu = False
        return intersections

    def check_translate(self, inter, current_translate_info, check_translate_info):
        """
        对比给定得 变换属性是否一模一样
        :param current_translate_info: 当前变换信息
        :param check_translate_info: 对比变换信息
        # 当前%s环节 与 对应%s环节里的 对应层级的属性不一致:
            |GEO|HIG|pCube1|pCubeShape1
                vertex:
                    srf: 110
                    rig: 520
                face:
                    srf: 222
                    rig: 444
        """
        header = u'==== 当前{}环节 与 对应{}环节里的 对应translate层级的属性不一致 ==== <br/>'.format(self.current_step, self.map_step)

        obj_path = self.tab_space + inter + '<br/>'
        base_str = header + obj_path
        attr_str_format = ''
        if not current_translate_info == check_translate_info:
            for attr, value in current_translate_info.items():
                map_value = check_translate_info[attr]
                if value != map_value:
                    attr_str = self.tab_space * 2 + '{attr}: {c_step}: {c_value} --- {m_step}: {m_value}' + '<br/>'
                    attr_str = attr_str.format(attr=attr,
                                               c_step=self.current_step,
                                               c_value=value,
                                               m_step=self.map_step,
                                               m_value=map_value)
                    attr_str_format += attr_str

        if attr_str_format:
            self.error_message += (base_str + attr_str_format)
            self.qc_statu = False

    def check_meshinfo(self, inter, current_mesh_info, check_mesh_info):
        """
        对比给定得 mesh点线面数量
        :param current_mesh_info:
        :param check_mesh_info:
        :return:
        """
        header = u'==== 当前{}环节 与 对应{}环节里的 对应mesh层级的属性不一致 ==== <br/>'
        header = header.format(self.current_step, self.map_step)

        obj_path = self.tab_space + inter + '<br/>'
        base_str = header + obj_path
        attr_str_format = ''
        if not current_mesh_info == check_mesh_info:
            for attr, value in current_mesh_info.items():
                map_value = check_mesh_info[attr]
                if value != map_value and attr != 'uvcoord':
                    attr_str = self.tab_space * 2 + '{attr}: {c_step}: {c_value} --- {m_step}: {m_value}' + '<br/>'
                    attr_str = attr_str.format(attr=attr,
                                               c_step=self.current_step,
                                               c_value=value,
                                               m_step=self.map_step,
                                               m_value=map_value)
                    attr_str_format += attr_str

        if attr_str_format:
            self.error_message += (base_str + attr_str_format)
            self.qc_statu = False

    def repair(self, *args, **kwargs):
        self.error_message = ''


def get_qc():
    return CheckAsset()


def debug():
    from app._maya.qc import check_asset
    reload(check_asset)
    cls = check_asset.CheckAsset()
    cls.run()

from pathlib import Path

def get_qc_items(path):
    # 此处获取质检项环节的分类
    folder = Path(path)
    module_list = folder.glob("*.py")
    result = []
    for md in module_list:
        result.append(md.stem)
    return result
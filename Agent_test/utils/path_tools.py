'''
提供统一的绝对路径
'''

import os

def get_project_root() -> str:
    '''
    获取项目根目录
    '''
    # 当前运行文件所在文件夹的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 根目录
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    '''
    获取相对路径对应的绝对路径
    '''
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path



if __name__ == "__main__":
    print(get_project_root())
    print(get_abs_path(r"RAG_test\data"))
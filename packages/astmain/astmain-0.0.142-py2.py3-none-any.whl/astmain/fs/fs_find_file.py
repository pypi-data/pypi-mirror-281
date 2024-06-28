import os
import multiprocessing as mp
from typing import List, Optional


def find_file(root_dir, filename):
    """在给定的根目录中搜索指定的文件名,并返回文件的绝对路径。 如果找到文件,返回文件路径;否则返回 None。 """
    file_path = os.path.join(root_dir, filename)
    if os.path.exists(file_path):
        return file_path
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower() == filename.lower():
                return os.path.join(dirpath, file)
    return None


def fs_find_file(dirs: List[str], filenames: List[str]) -> Optional[str]:
    """ EXPLAIN :
        根,目录,搜索,文件名,如果找到任何文件,则返回文件的绝对路径,否则返回 None。
        EXAMPLE :  
        dirs = ['C:\\Program Files (x86)', 'C:\\Program Files', 'C:\\']
        filenames = ['chrome.exe', 'notepad.exe']
        file_path = fs_find_file(dirs, filenames)
    """
    results = []
    with mp.Pool(processes=len(dirs)) as pool:
        # 使用 apply_async 并行处理每个根目录和文件名的搜索任务
        for root_dir in dirs:
            for filename in filenames:
                results.append(pool.apply_async(find_file, args=(root_dir, filename)))
        # 等待所有任务完成,并返回找到的第一个文件路径
        for result in results:
            file_path = result.get()
            if file_path is not None:
                return file_path
    return "None"


if __name__ == '__main__':
    dirs = ['C:\\Program Files (x86)', 'C:\\Program Files', 'C:\\']
    filenames = ['chrome.exe', 'notepad.exe']
    file_path = fs_find_file(dirs, filenames)
    if file_path:
        print(f'Found file at: {file_path}')
    else:
        print(f'Files not found.')

# 不要使用列表推导式#不要使用lambda表达式#运行速度在快一点,我写好正文注释

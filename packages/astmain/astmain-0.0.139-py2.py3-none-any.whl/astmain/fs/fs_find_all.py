import os
import multiprocessing as mp


def find_chrome_exe(root_dir):
    chrome_exe_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower() == 'chrome.exe':
                chrome_exe_paths.append(os.path.join(dirpath, filename))
    return chrome_exe_paths


def parallel_search():
    root_dirs = ['C:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    with mp.Pool(processes=len(root_dirs)) as pool:
        results = pool.map(find_chrome_exe, root_dirs)

    chrome_exe_paths = []
    for result in results:
        chrome_exe_paths.extend(result)

    return chrome_exe_paths


if __name__ == '__main__':
    chrome_exe_paths = parallel_search()
    if chrome_exe_paths:
        print('Found chrome.exe files:')
        for path in chrome_exe_paths:
            print(path)
    else:
        print('chrome.exe not found.')

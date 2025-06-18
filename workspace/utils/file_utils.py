import os


def scan(directory_path):
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # 检查是否为文件
            files.append(file_path)
    return files

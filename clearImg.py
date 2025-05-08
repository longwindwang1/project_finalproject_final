import os

dataset_path = 'D:/project/train/train/'

def clearImg(dataset_type):
    """
    清理数据集中标注数据为空的文件，并删除没有对应标注的图片
    """
    # 目录路径
    label_path = os.path.join(dataset_path, dataset_type, 'labels')
    img_path = os.path.join(dataset_path, dataset_type, 'images')

    # 如果 labels 目录不存在，则不执行
    if not os.path.exists(label_path) or not os.path.exists(img_path):
        print(f"目录 {label_path} 或 {img_path} 不存在，跳过")
        return

    # 获取所有标注文件
    label_file_names = os.listdir(label_path)
    img_files = set()  # 用于存储有对应标注的图片名

    # 删除空的标注文件，并记录非空文件的对应图片名
    for file_name in label_file_names:
        file_path = os.path.join(label_path, file_name)

        # 处理文件权限（解除 "只读" 状态）
        os.chmod(file_path, 0o777)

        # 检查文件大小
        if os.stat(file_path).st_size == 0:
            try:
                os.remove(file_path)
                print(f"删除空标注文件: {file_path}")
            except PermissionError:
                print(f"无法删除 {file_path}，文件可能被占用")
            continue  # 跳过后续处理

        # 进一步检查文件内容是否为空（只包含空格或换行）
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()  # 去掉空格和换行符

        if not content:  # 如果内容为空，删除
            try:
                os.remove(file_path)
                print(f"删除内容为空的标注文件: {file_path}")
            except PermissionError:
                print(f"无法删除 {file_path}，文件可能被占用")
            continue

        # 记录不为空的标注文件对应的图片名
        base_name = os.path.splitext(file_name)[0]
        img_files.add(base_name)

    # 获取 images 目录下所有图片文件
    img_file_names = os.listdir(img_path)

    for file_name in img_file_names:
        file_path = os.path.join(img_path, file_name)

        # 获取文件名（无扩展名）
        base_name, ext = os.path.splitext(file_name)

        # 如果该图片没有对应的标注文件，则删除
        if base_name not in img_files:
            try:
                os.remove(file_path)
                print(f"delete empty: {file_path}")
            except PermissionError:
                print(f"cant delete {file_path}，might be using")

# 运行数据清理
clearImg("test_small")

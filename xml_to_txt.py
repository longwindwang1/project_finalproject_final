import os
import xml.etree.ElementTree as ET

# 定义类别映射，根据需要调整
classes = {"car": 0, "truck": 1}

def convert_annotation(xml_file, txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图片尺寸
    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    lines = []
    # 遍历每个 object 节点
    for obj in root.findall('object'):
        cls_name = obj.find('name').text
        # 如果类别不在定义的映射中则跳过
        if cls_name not in classes:
            continue
        class_id = classes[cls_name]

        # 找到 polygon 节点，并提取多边形坐标
        polygon = obj.find('polygon')
        if polygon is None:
            continue

        xs, ys = [], []
        # 假设 polygon 中有 x1,y1 ... x4,y4 四个点，如果点数不同可以自行调整
        for i in range(1, 5):
            x = int(polygon.find(f'x{i}').text)
            y = int(polygon.find(f'y{i}').text)
            xs.append(x)
            ys.append(y)
        
        # 计算外接矩形
        x_min = min(xs)
        y_min = min(ys)
        x_max = max(xs)
        y_max = max(ys)

        # 计算中心点、宽度和高度，并归一化到 [0,1]
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        bbox_width = (x_max - x_min) / img_width
        bbox_height = (y_max - y_min) / img_height

        # 生成一行字符串：类别索引 归一化中心点x 归一化中心点y 归一化宽度 归一化高度
        line = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
        lines.append(line)
    
    # 写入到 TXT 文件
    with open(txt_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')

def process_folder(folder_path):
    # 遍历文件夹中所有 XML 文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.xml'):
            xml_path = os.path.join(folder_path, filename)
            # 将 .xml 后缀替换为 .txt
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(folder_path, txt_filename)
            print(f"转换 {xml_path} 为 {txt_path}")
            convert_annotation(xml_path, txt_path)

if __name__ == '__main__':
    folder_path = r"D:/毕业设计/train/train/trainlabel"  # 修改为你的文件夹路径
    process_folder(folder_path)

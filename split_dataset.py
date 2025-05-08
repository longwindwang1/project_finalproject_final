import os
import cv2
import numpy as np

# 数据路径
source_dir = "D:/project/train/train/test"
save_dir = "D:/project/train/train/test_small"

# 计算切割尺寸（840×712 -> 4×4 小图，每张 210×178）
patch_size_x = 210
patch_size_y = 178

# 计算 16 个小图的坐标区域
smallImgArea = {}
for i in range(4):
    for j in range(4):
        x1, y1 = j * patch_size_x, i * patch_size_y
        x2, y2 = x1 + patch_size_x, y1 + patch_size_y
        smallImgArea[f"{i}_{j}"] = [(x1, y1), (x2, y2)]  # 只存左上角和右下角

def check_overlap(rect1, rect2):
    """
    判断两个矩形是否有重叠区域
    rect1: [(x_min, y_min), (x_max, y_max)]
    rect2: [(x_min, y_min), (x_max, y_max)]
    """
    x1_min, y1_min = rect1[0]
    x1_max, y1_max = rect1[1]

    x2_min, y2_min = rect2[0]
    x2_max, y2_max = rect2[1]

    # 计算交叉区域
    overlap_x = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
    overlap_y = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

    return overlap_x > 0 and overlap_y > 0  # 只要有重叠就返回 True

def split_image(image_path, filename, save_dir):
    """
    将大图像拆分成 16 个 210×178 小图并保存
    """
    image = cv2.imread(image_path)
    rows, cols = 4, 4

    for i in range(rows):
        for j in range(cols):
            x1 = j * patch_size_x
            y1 = i * patch_size_y
            x2 = x1 + patch_size_x
            y2 = y1 + patch_size_y
            
            patch = image[y1:y2, x1:x2]
            save_path = os.path.join(save_dir, "images", f"{filename.replace('.jpg','')}_{i}_{j}.jpg")
            cv2.imwrite(save_path, patch)

if __name__ == "__main__":
    # 创建保存目录
    os.makedirs(os.path.join(save_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(save_dir, "labels"), exist_ok=True)

    for filename in os.listdir(os.path.join(source_dir, "images")):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(source_dir, "images", filename)
            txt_path = os.path.join(source_dir, "labels", filename).replace(".jpg", ".txt").replace(".png", ".txt")
            
            print(f"Processing: {image_path}")
            split_image(image_path, filename, save_dir)

            # 处理标注文件
            labelDatas = {f"{i}_{j}": [] for i in range(4) for j in range(4)}
            
            with open(txt_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                boxData = line.strip().split(" ")
                if len(boxData) != 5:  # 确保 YOLO 格式正确
                    print(f"⚠️ 标注格式错误，跳过：{line}")
                    continue

                class_id = boxData[0]
                x_center, y_center, w, h = map(float, boxData[1:])

                # 计算原图坐标（恢复归一化）
                x_center *= 840
                y_center *= 712
                w *= 840
                h *= 712

                # 转换为 (x1, y1) 和 (x2, y2)
                x1 = int(x_center - w / 2)
                y1 = int(y_center - h / 2)
                x2 = int(x_center + w / 2)
                y2 = int(y_center + h / 2)

                # 查找标注框在哪个小图区域
                for area, (tl, br) in smallImgArea.items():
                    if check_overlap([tl, br], [(x1, y1), (x2, y2)]):
                        row, col = map(int, area.split("_"))
                        x_offset, y_offset = col * patch_size_x, row * patch_size_y

                        # 计算新的 x_center, y_center, w, h（归一化）
                        new_x_center = ((x_center - x_offset) / patch_size_x)
                        new_y_center = ((y_center - y_offset) / patch_size_y)
                        new_w = w / patch_size_x
                        new_h = h / patch_size_y

                        # 保证框不超出 0-1
                        new_x_center = max(0, min(new_x_center, 1))
                        new_y_center = max(0, min(new_y_center, 1))
                        new_w = max(0, min(new_w, 1))
                        new_h = max(0, min(new_h, 1))

                        labelDatas[area].append(f"{class_id} {new_x_center:.6f} {new_y_center:.6f} {new_w:.6f} {new_h:.6f}")

        # 保存新标注文件（YOLO 格式）
        for area, boxes in labelDatas.items():
            new_label_path = os.path.join(save_dir, "labels", f"{filename.replace('.jpg', '')}_{area}.txt")
            with open(new_label_path, 'w') as file:
                file.write("\n".join(boxes) + "\n")

        print(f"Saved annotations for {filename}")

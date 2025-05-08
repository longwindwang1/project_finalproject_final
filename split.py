import os
import random
import shutil

# 设置路径
dataset_path = "D:/project/train/train/test"
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")

# 目标路径
split_dirs = ["train", "val", "test"]
for split in split_dirs:
    os.makedirs(os.path.join(dataset_path, "images", split), exist_ok=True)
    os.makedirs(os.path.join(dataset_path, "labels", split), exist_ok=True)

# 获取所有图片文件（假设只有 .jpg 或 .png）
image_files = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png"))]
random.shuffle(image_files)  # 随机打乱

# 设置划分比例
train_ratio, val_ratio, test_ratio = 0.8, 0.1, 0.1
total_images = len(image_files)

train_count = int(total_images * train_ratio)
val_count = int(total_images * val_ratio)

train_images = image_files[:train_count]
val_images = image_files[train_count:train_count + val_count]
test_images = image_files[train_count + val_count:]

# 划分数据集
def move_files(image_list, split):
    for image in image_list:
        image_src = os.path.join(images_path, image)
        label_src = os.path.join(labels_path, image.replace(".jpg", ".txt").replace(".png", ".txt"))

        image_dst = os.path.join(dataset_path, "images", split, image)
        label_dst = os.path.join(dataset_path, "labels", split, image.replace(".jpg", ".txt").replace(".png", ".txt"))

        # 确保有对应的标注文件才移动
        if os.path.exists(label_src):
            shutil.move(image_src, image_dst)
            shutil.move(label_src, label_dst)
        else:
            print(f" 跳过：{image} 没有对应的标注文件")

# 移动文件
move_files(train_images, "train")
move_files(val_images, "val")
move_files(test_images, "test")

print("数据集已划分完成！")

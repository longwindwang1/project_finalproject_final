import os
import argparse
from ultralytics import YOLO


def train_yolov10(data_yaml, model_name, epochs, batch_size, img_size, device):
    """
    训练 YOLOv10 模型
    """
    # 加载模型
    model = YOLO(model_name)

    # 训练
    model.train(
        data=data_yaml,  # 数据集路径
        epochs=epochs,  # 训练轮数
        batch=batch_size,  # 批量大小
        imgsz=(img_size,img_size),  # 输入图片大小
        device=device,  # 设备（CPU/GPU）
        workers=4  # 加载数据线程数
    )

    print("训练完成！模型已保存到 runs/detect/train/weights/")

    # 评估模型
    print("开始评估模型...")
    metrics = model.val()
    print("评估结果: ", metrics)

def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="Train YOLOv10 Model")
    parser.add_argument("--data", type=str, default="D:/project/train/train/test/data.yaml",
                        help="数据集配置文件 (data.yaml)")
    parser.add_argument("--model", type=str, default="D:\project\yolov10n.pt",
                        help="选择 YOLOv10 预训练模型 (yolov10n.pt / yolov10s.pt / yolov10m.pt)")
    parser.add_argument("--epochs", type=int, default=100, help="训练轮数")
    parser.add_argument("--batch", type=int, default=16, help="批量大小")
    parser.add_argument("--imgsz", type=int, default=840, help="输入图片大小 (默认640x640)")
    parser.add_argument("--device", type=str, default="cuda:0",
                        help="训练设备 (cpu / cuda:0 / cuda:1)")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    train_yolov10(args.data, args.model, args.epochs, args.batch, args.imgsz, args.device)

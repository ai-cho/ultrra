import torch
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import os

# ============================
# COLMAP 텍스트 파일 읽기 함수
# ============================
def read_extrinsics_text(filepath):
    extrinsics = {}
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.strip().split()
        image_id = int(parts[0])
        qvec = np.array([float(p) for p in parts[1:5]])  # quaternion
        tvec = np.array([float(p) for p in parts[5:8]])  # translation vector
        extrinsics[image_id] = {"qvec": qvec, "tvec": tvec}

    return extrinsics

def read_intrinsics_text(filepath):
    intrinsics = {}
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.strip().split()
        cam_id = int(parts[0])
        width, height = int(parts[1]), int(parts[2])
        focal_length = float(parts[3])
        intrinsics[cam_id] = {
            "width": width,
            "height": height,
            "focal_length": focal_length,
        }

    return intrinsics

def read_points_text(filepath):
    points = []
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.strip().split()
        xyz = np.array([float(p) for p in parts[:3]])
        rgb = np.array([int(p) for p in parts[3:6]])
        points.append({"xyz": xyz, "rgb": rgb})

    return points

# ============================
# 렌더링 함수
# ============================
def render(scene_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 파일 읽기
    extrinsics = read_extrinsics_text(os.path.join(scene_dir, "images.txt"))
    intrinsics = read_intrinsics_text(os.path.join(scene_dir, "cameras.txt"))
    points3D = read_points_text(os.path.join(scene_dir, "point3D.txt"))

    print("Extrinsics:", len(extrinsics))
    print("Intrinsics:", len(intrinsics))
    print("3D Points:", len(points3D))

    # 이미지 렌더링 (간단한 예제)
    for img_id, cam_params in extrinsics.items():
        image = np.zeros((intrinsics[img_id]["height"], intrinsics[img_id]["width"], 3), dtype=np.uint8)

        for point in points3D:
            # 포인트 색상으로 이미지 채우기
            x, y, z = point["xyz"]
            r, g, b = point["rgb"]
            u = int(x) % image.shape[1]
            v = int(y) % image.shape[0]
            image[v, u] = [r, g, b]

        # 이미지 저장
        img = Image.fromarray(image)
        img.save(os.path.join(output_dir, f"{img_id:05d}.png"))

        print(f"Rendered image saved: {output_dir}/{img_id:05d}.png")

# ============================
# 실행 스크립트
# ============================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render COLMAP scene.")
    parser.add_argument("--scene_dir", type=str, required=True, help="Path to COLMAP text files.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to save rendered images.")
    args = parser.parse_args()

    render(args.scene_dir, args.output_dir)

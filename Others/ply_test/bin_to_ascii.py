import open3d as o3d
import numpy as np

# 입력 파일명과 출력 파일명 설정
INPUT_FILE = "./points.ply"
OUTPUT_FILE = "./points_ascii.ply"

print(f"1. {INPUT_FILE} 파일 로드 (바이너리 형식)")
# Open3D는 바이너리 PLY 파일을 자동으로 읽을 수 있습니다.
pcd = o3d.io.read_point_cloud(INPUT_FILE)

# (선택 사항: 로드된 포인트 개수 확인)
num_points = np.asarray(pcd.points).shape[0]
print(f"   -> 로드된 포인트 개수: {num_points}개")

# 2. ASCII 형식으로 저장
# write_ascii=True 옵션을 사용하여 ASCII 텍스트 형식으로 저장하도록 지시합니다.
# Open3D의 기본 PointCloud 객체는 (X, Y, Z, R, G, B)만 저장하므로,
# 원본 points.ply에 있던 Alpha 속성은 자동으로 제거됩니다.
o3d.io.write_point_cloud(OUTPUT_FILE, pcd, write_ascii=True)

print(f"2. {OUTPUT_FILE} 파일 생성 완료 (ASCII 형식, 6개 속성)")
print("   -> 이제 이 파일을 기존 load_ply 함수로 읽을 수 있습니다.")
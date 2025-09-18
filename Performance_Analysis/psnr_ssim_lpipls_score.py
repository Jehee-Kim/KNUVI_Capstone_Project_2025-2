# import os
# import numpy as np
# from PIL import Image
# from tqdm import tqdm
# from skimage.metrics import peak_signal_noise_ratio as compare_psnr
# from skimage.metrics import structural_similarity as compare_ssim

# def load_image(path):
#     """이미지를 [0, 1] 범위로 정규화된 float32 배열로 로드"""
#     return np.array(Image.open(path).convert('RGB')).astype(np.float32) / 255.0

# def compute_psnr_ssim(gt_dir, pred_dir):
#     gt_images = sorted([f for f in os.listdir(gt_dir) if f.endswith(('png', 'jpg', 'jpeg'))])
#     pred_images = sorted([f for f in os.listdir(pred_dir) if f.endswith(('png', 'jpg', 'jpeg'))])

#     if len(gt_images) != len(pred_images):
#         raise ValueError("GT and prediction folders must contain the same number of images.")

#     psnr_list, ssim_list = [], []
#     for gt_img, pred_img in tqdm(zip(gt_images, pred_images), total=len(gt_images), desc='Computing PSNR & SSIM'):
#         gt_path = os.path.join(gt_dir, gt_img)
#         pred_path = os.path.join(pred_dir, pred_img)

#         gt = load_image(gt_path)
#         pred = load_image(pred_path)

#         if gt.shape != pred.shape:
#             raise ValueError(f"Shape mismatch: {gt_img} vs {pred_img}")

#         psnr_val = compare_psnr(gt, pred, data_range=1.0)
#         ssim_val = compare_ssim(gt, pred, data_range=1.0, channel_axis=2)

#         psnr_list.append(psnr_val)
#         ssim_list.append(ssim_val)

#     avg_psnr = np.mean(psnr_list)
#     avg_ssim = np.mean(ssim_list)
#     print(f'Average PSNR: {avg_psnr:.2f} dB')
#     print(f'Average SSIM: {avg_ssim:.4f}')
#     return avg_psnr, avg_ssim

# # 예시 실행
# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--gt_dir', type=str, required=True, help='Ground truth image folder')
#     parser.add_argument('--pred_dir', type=str, required=True, help='Predicted/rendered image folder')
#     args = parser.parse_args()

#     compute_psnr_ssim(args.gt_dir, args.pred_dir)

import os
import numpy as np
from PIL import Image
from tqdm import tqdm
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim

import torch
import lpips
from torchvision import transforms

def load_image(path, for_lpips=False):
    """이미지를 [0,1]로 정규화하거나, LPIPS용 텐서로 변환"""
    img = Image.open(path).convert('RGB')

    if for_lpips:
        transform = transforms.Compose([
            transforms.ToTensor(),  # [0,1]
            transforms.Normalize([0.5]*3, [0.5]*3)  # [-1,1] for LPIPS
        ])
        return transform(img).unsqueeze(0)  # (1, 3, H, W)
    else:
        return np.array(img).astype(np.float32) / 255.0

def compute_all_metrics(gt_dir, pred_dir, lpips_net='alex'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    loss_fn = lpips.LPIPS(net=lpips_net).to(device).eval()

    gt_images = sorted([f for f in os.listdir(gt_dir) if f.endswith(('png', 'jpg', 'jpeg'))])
    pred_images = sorted([f for f in os.listdir(pred_dir) if f.endswith(('png', 'jpg', 'jpeg'))])

    if len(gt_images) != len(pred_images):
        raise ValueError("GT and prediction folders must contain the same number of images.")

    psnr_list, ssim_list, lpips_list = [], [], []
    for gt_img, pred_img in tqdm(zip(gt_images, pred_images), total=len(gt_images), desc='Computing Metrics'):
        gt_path = os.path.join(gt_dir, gt_img)
        pred_path = os.path.join(pred_dir, pred_img)

        # Load for PSNR/SSIM
        gt_np = load_image(gt_path)
        pred_np = load_image(pred_path)

        if gt_np.shape != pred_np.shape:
            raise ValueError(f"Shape mismatch: {gt_img} vs {pred_img}")

        psnr_val = compare_psnr(gt_np, pred_np, data_range=1.0)
        ssim_val = compare_ssim(gt_np, pred_np, data_range=1.0, channel_axis=2)

        psnr_list.append(psnr_val)
        ssim_list.append(ssim_val)

        # Load for LPIPS
        gt_tensor = load_image(gt_path, for_lpips=True).to(device)
        pred_tensor = load_image(pred_path, for_lpips=True).to(device)

        with torch.no_grad():
            lpips_val = loss_fn(gt_tensor, pred_tensor).item()
        lpips_list.append(lpips_val)

    avg_psnr = np.mean(psnr_list)
    avg_ssim = np.mean(ssim_list)
    avg_lpips = np.mean(lpips_list)

    print(f'Average PSNR:  {avg_psnr:.2f} dB')
    print(f'Average SSIM:  {avg_ssim:.4f}')
    print(f'Average LPIPS: {avg_lpips:.4f} ({lpips_net})')

    return avg_psnr, avg_ssim, avg_lpips

# 예시 실행
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt_dir', type=str, required=True, help='Ground truth image folder')
    parser.add_argument('--pred_dir', type=str, required=True, help='Predicted/rendered image folder')
    parser.add_argument('--lpips_net', type=str, default='alex', choices=['alex', 'vgg', 'squeeze'], help='LPIPS network backbone')
    args = parser.parse_args()

    compute_all_metrics(args.gt_dir, args.pred_dir, args.lpips_net)

def demo_fn(args):
    # Print configuration
    print("Arguments:", vars(args))

    # Set seed for reproducibility
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    random.seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(args.seed)
        torch.cuda.manual_seed_all(args.seed)  # for multi-GPU
    print(f"Setting seed as: {args.seed}")

    # Set device and dtype
    dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    print(f"Using dtype: {dtype}")

    # Run VGGT for camera and depth estimation
    model = VGGT()
    #_URL = "https://huggingface.co/facebook/VGGT-1B/resolve/main/model.pt"
    #model.load_state_dict(torch.hub.load_state_dict_from_url(_URL))
    
    state_dict = torch.load("/home/knuvi/vggt/model.pt", map_location = "cuda") 
    model.load_state_dict(state_dict)
    model.eval()
    model = model.to(device)
    print(f"Model loaded")

    QP_values = [70, 50, 30, 20, 10]
    categories = ["backpack", "ball", "book", "bottle", "chair", "cup", "handbag", "laptop", "plant", "teddybear", "vase"]

    # 이미지 파일이 있는 디렉토리 및 복사 대상 디렉토리 설정
    source_dir_template = "/home/knuvi/OSEDiff/Results/jpeg/JpegOutput_{QP}/{category}/*/images"
    destination_dir = "/home/knuvi/vggt/temp/images"  # 이미지 복사 위치
    temp_dir = "/home/knuvi/vggt/temp"  # demo_colmap.py가 읽는 폴더 경로
    result_dir_template = "/home/knuvi/vggt/Result/OSEDiff/jpeg/JpegOutput_{QP}/{category}/{filename}/sparse"

    # destination_dir이 없으면 생성
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    else:
        # temp/images 디렉토리가 비어 있지 않으면 비워준다
        for filename in os.listdir(destination_dir):
            file_path = os.path.join(destination_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    # 이미지 복사 및 demo_colmap 실행
    for QP in QP_values:
        for category in categories:
            # 해당 카테고리 및 QP에 맞는 이미지 디렉토리 경로 패턴 설정
            source_dir_pattern = source_dir_template.format(QP=QP, category=category)

            # glob을 사용하여 해당 패턴에 맞는 폴더를 찾음
            folder_paths = glob.glob(source_dir_pattern)

            if not folder_paths:
                print(f"디렉토리 없음: {source_dir_pattern}")
                continue

            # 각 폴더에 대해 작업 수행
            for folder_path in folder_paths:
                print(f"폴더 경로: {folder_path}")
                # .jpg로 수정 및 이미지 파일 리스트 정렬
                image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(f"JPEG_{QP}.jpg")])

                # 이미지 파일을 하나씩 복사하여 처리
                for image_file in image_files:
                    source_file = os.path.join(folder_path, image_file)

                    if os.path.exists(source_file):
                        # 파일 이름을 폴더 이름으로 사용
                        filename = os.path.splitext(image_file)[0]  # 확장자 제거
                        result_folder = result_dir_template.format(QP=QP, category=category, filename=filename)

                        # 결과 저장 폴더가 없으면 생성
                        if not os.path.exists(result_folder):
                            os.makedirs(result_folder)

                        # temp/images 디렉토리에 한 장씩 복사
                        shutil.copy(source_file, destination_dir)

                        # 출력: 복사된 파일과 저장되는 폴더 경로
                        print(f"복사된 파일: {source_file} -> {destination_dir}")
                        print(f"저장되는 결과 폴더: {result_folder}")





                        # Get image paths and preprocess them
                        image_dir = os.path.join(temp_dir, "images")
                        image_path_list = glob.glob(os.path.join(image_dir, "*"))
                        if len(image_path_list) == 0:
                            raise ValueError(f"No images found in {image_dir}")
                        base_image_path_list = [os.path.basename(path) for path in image_path_list]

                        # Load images and original coordinates
                        # Load Image in 1024, while running VGGT with 518
                        vggt_fixed_resolution = 518
                        img_load_resolution = 1024

                        images, original_coords = load_and_preprocess_images_square(image_path_list, img_load_resolution)
                        images = images.to(device)
                        original_coords = original_coords.to(device)
                        print(f"Loaded {len(images)} images from {image_dir}")

                        # Run VGGT to estimate camera and depth
                        # Run with 518x518 images
                        extrinsic, intrinsic, depth_map, depth_conf = run_VGGT(model, images, dtype, vggt_fixed_resolution)
                        points_3d = unproject_depth_map_to_point_map(depth_map, extrinsic, intrinsic)

                        if args.use_ba:
                            image_size = np.array(images.shape[-2:])
                            scale = img_load_resolution / vggt_fixed_resolution
                            shared_camera = args.shared_camera

                            with torch.cuda.amp.autocast(dtype=dtype):
                                # Predicting Tracks
                                # Using VGGSfM tracker instead of VGGT tracker for efficiency
                                # VGGT tracker requires multiple backbone runs to query different frames (this is a problem caused by the training process)
                                # Will be fixed in VGGT v2

                                # You can also change the pred_tracks to tracks from any other methods
                                # e.g., from COLMAP, from CoTracker, or by chaining 2D matches from Lightglue/LoFTR.
                                pred_tracks, pred_vis_scores, pred_confs, points_3d, points_rgb = predict_tracks(
                                    images,
                                    conf=depth_conf,
                                    points_3d=points_3d,
                                    masks=None,
                                    max_query_pts=args.max_query_pts,
                                    query_frame_num=args.query_frame_num,
                                    keypoint_extractor="aliked+sp",
                                    fine_tracking=args.fine_tracking,
                                )

                                torch.cuda.empty_cache()

                            # rescale the intrinsic matrix from 518 to 1024
                            intrinsic[:, :2, :] *= scale
                            track_mask = pred_vis_scores > args.vis_thresh

                            # TODO: radial distortion, iterative BA, masks
                            reconstruction, valid_track_mask = batch_np_matrix_to_pycolmap(
                                points_3d,
                                extrinsic,
                                intrinsic,
                                pred_tracks,
                                image_size,
                                masks=track_mask,
                                max_reproj_error=args.max_reproj_error,
                                shared_camera=shared_camera,
                                camera_type=args.camera_type,
                                points_rgb=points_rgb,
                            )

                            if reconstruction is None:
                                raise ValueError("No reconstruction can be built with BA")

                            # Bundle Adjustment
                            ba_options = pycolmap.BundleAdjustmentOptions()
                            pycolmap.bundle_adjustment(reconstruction, ba_options)

                            reconstruction_resolution = img_load_resolution
                        else:
                            conf_thres_value = args.conf_thres_value
                            max_points_for_colmap = 100000  # randomly sample 3D points
                            shared_camera = False  # in the feedforward manner, we do not support shared camera
                            camera_type = "PINHOLE"  # in the feedforward manner, we only support PINHOLE camera

                            image_size = np.array([vggt_fixed_resolution, vggt_fixed_resolution])
                            num_frames, height, width, _ = points_3d.shape

                            points_rgb = F.interpolate(
                                images, size=(vggt_fixed_resolution, vggt_fixed_resolution), mode="bilinear", align_corners=False
                            )
                            points_rgb = (points_rgb.cpu().numpy() * 255).astype(np.uint8)
                            points_rgb = points_rgb.transpose(0, 2, 3, 1)

                            # (S, H, W, 3), with x, y coordinates and frame indices
                            points_xyf = create_pixel_coordinate_grid(num_frames, height, width)

                            conf_mask = depth_conf >= conf_thres_value
                            # at most writing 100000 3d points to colmap reconstruction object
                            conf_mask = randomly_limit_trues(conf_mask, max_points_for_colmap)

                            points_3d = points_3d[conf_mask]
                            points_xyf = points_xyf[conf_mask]
                            points_rgb = points_rgb[conf_mask]

                            print("Converting to COLMAP format")
                            reconstruction = batch_np_matrix_to_pycolmap_wo_track(
                                points_3d,
                                points_xyf,
                                points_rgb,
                                extrinsic,
                                intrinsic,
                                image_size,
                                shared_camera=shared_camera,
                                camera_type=camera_type,
                            )

                            reconstruction_resolution = vggt_fixed_resolution

                        reconstruction = rename_colmap_recons_and_rescale_camera(
                            reconstruction,
                            base_image_path_list,
                            original_coords.cpu().numpy(),
                            img_size=reconstruction_resolution,
                            shift_point2d_to_original_res=True,
                            shared_camera=shared_camera,
                        )

                        print(f"Saving reconstruction to {temp_dir}/sparse")
                        sparse_reconstruction_dir = os.path.join(temp_dir, "sparse")
                        os.makedirs(sparse_reconstruction_dir, exist_ok=True)
                        reconstruction.write(sparse_reconstruction_dir)

                        # Save point cloud for fast visualization
                        trimesh.PointCloud(points_3d, colors=points_rgb).export(os.path.join(temp_dir, "sparse/points.ply"))

                        # 처리된 후 temp/images 디렉토리 비우기
                        os.remove(os.path.join(destination_dir, image_file))

                        # sparse 폴더 내 파일을 result_folder로 복사
                        sparse_folder = os.path.join(temp_dir, "sparse")
                        if os.path.exists(sparse_folder):
                            for file_name in os.listdir(sparse_folder):
                                file_path = os.path.join(sparse_folder, file_name)
                                if os.path.isfile(file_path):
                                    shutil.copy(file_path, result_folder)
                                    # 출력: 복사된 결과 파일
                                    print(f"복사된 결과 파일: {file_path} -> {result_folder}")
                        else:
                            print(f"sparse 폴더가 존재하지 않음: {sparse_folder}")

                    else:
                        print(f"파일이 존재하지 않음: {source_file}")

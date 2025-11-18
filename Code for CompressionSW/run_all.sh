
# 0. 기본 경로 입력 받기
echo "데이터셋 경로를 입력하세요 (예: /mnt/c/Users/user/Desktop/dataset):"
read base_root
echo "사용할 데이터셋 경로: $base_root"

# 1. 코덱 선택
echo "사용할 코덱을 선택하세요 (hevc / jpeg): "
read codec

# 2. QP 또는 JPEG Quality 리스트 입력
echo "사용할 QP 또는 JPEG Quality 리스트 입력 (예: 10 30 50 70 90): "
read -a qps

echo "선택된 모드: $codec"
echo "사용된 값: ${qps[@]}"

##############################################
# 1. JPEG 압축 함수
##############################################
jpeg_compress() {
    echo "===== JPEG 압축 시작 ====="

    output_root="${base_root}/jpeg_output"

    scenes=(bicycle bonsai counter flowers garden kitchen room stump treehill)

    for scene in "${scenes[@]}"; do
        input_dir="${base_root}/frames/${scene}"
        if [ ! -d "$input_dir" ]; then
            echo "⚠️ $input_dir 없음. 건너뜀"
            continue
        fi

        for q in "${qps[@]}"; do
            outdir="${output_root}/${scene}/Q${q}"
            mkdir -p "$outdir"

            for img in "$input_dir"/*.{jpg,JPG,png}; do
                [ -f "$img" ] || continue
                fname=$(basename "$img")
                outfile="${outdir}/${fname%.jpg}_Q${q}.jpg"

                convert "$img" -quality "$q" "$outfile"
                echo "[${scene}] Q=${q} 저장 → $outfile"
            done
        done
    done

    echo "===== JPEG 압축 완료 ====="
}

##############################################
# 2. HEVC 인코딩 함수
##############################################
hevc_encode() {
	mkdir -p "${base_root}/yuv"
	mkdir -p "${base_root}/recon"
	mkdir -p "${base_root}/bitstream"
	mkdir -p "${base_root}/coding_log"

	echo "===== JPG 파일 이름 일괄 변경 시작 ====="
     	for scene in "${scenes[@]}"; do
         	frames_dir="${base_root}/frames/${scene}"
         	n=1
    	 	for file in "$frames_dir"/_DSC*.JPG "$frames_dir"/_DSC*.jpg "$frames_dir"/_DSC*.JPEG "$frames_dir"/_DSC*.jpeg \
                "$frames_dir"/DSC*.JPG "$frames_dir"/DSC*.jpg "$frames_dir"/DSC*.JPEG "$frames_dir"/DSC*.jpeg \
                "$frames_dir"/DSCF*.JPG "$frames_dir"/DSCF*.jpg "$frames_dir"/DSCF*.JPEG "$frames_dir"/DSCF*.jpeg; do
         	[ -f "$file" ] || continue
         	ext="${file##*.}"
         	new_name=$(printf "img_%06d.%s" "$n" "$ext")
         	mv "$file" "$frames_dir/$new_name"
         	((n++))
    	done
    	echo "===== [$scene] 완료: $((n-1)) 개 파일 이름 변경 ====="
	done

	echo "===== JPG → YUV 변환 시작 ====="

	scenes=(bicycle bonsai counter flowers garden kitchen room stump treehill)

	for scene in "${scenes[@]}"; do
	    frames_dir="${base_root}/frames/${scene}"
	    yuv_out="${base_root}/yuv/${scene}.yuv"

	    echo "[${scene}] JPG → YUV 변환 중..."
	    ffmpeg -y -framerate 30 \
	        -i ${frames_dir}/img_%06d.jpg\
	        -f rawvideo -pix_fmt yuv444p \
	        "$yuv_out"
	    echo "[${scene}] 완료: $yuv_out"
	done

	echo "===== JPG → YUV 변환 완료 ====="

	# ============================
	#  설정
	# ============================
	inputs=(
	"bicycle 195 618 410"
	"bonsai 292 390 260"
	"counter 240 388 260"
	"flowers 173 628 414"
	"garden 185 648 420"
	"kitchen 279 388 260"
	"room 311 388 258"
	"stump 126 622 412"
	"treehill 141 634 416"
	)

	encoder="$HOME/HM/bin/umake/gcc-13.3/x86_64/release/TAppEncoder"
  cfg="$HOME/HM/cfg/encoder_randomaccess_main.cfg"

	# ============================
	#  코어 자동 감지
	# ============================
	n_cores=$(nproc)
	core_list=($(seq 0 $((n_cores-1))))
	task_count=0

	# ============================
	#  HEVC Encoding
	# ============================
	echo "===== HEVC Encoding 시작 ====="

	for input_info in "${inputs[@]}"; do
	    name=$(echo "$input_info" | awk '{print $1}')
	    frames=$(echo "$input_info" | awk '{print $2}')
	    width=$(echo "$input_info" | awk '{print $3}')
	    height=$(echo "$input_info" | awk '{print $4}')

	    for qp in "${qps[@]}"; do

	        input="${base_root}/yuv/${name}.yuv"
					recon="${base_root}/recon/${name}_qp${qp}.yuv"
					bin="${base_root}/bitstream/${name}_qp${qp}.bin"
					log="${base_root}/coding_log/${name}_qp${qp}.log"

	        core_idx=$((task_count % n_cores))
	        core=${core_list[$core_idx]}

	        {
	            echo "=== $(date) START name=${name} qp=${qp} core=${core} frames=${frames} ==="
	            taskset -c "$core" "$encoder" \
	                -c "$cfg" \
	                -i "$input" -o "$recon" \
	                -wdt "$width" -hgt "$height" \
	                -b "$bin" -q "$qp" -fr 30 -f "$frames"
	            ret=$?
	            echo "=== $(date) END name=${name} qp=${qp} status=${ret} ==="
	        } > "$log" 2>&1 &

	        ((task_count++))

	        # 코어 수만큼만 병렬 실행
	        if (( $(jobs -r | wc -l) >= n_cores )); then
	            wait -n
	        fi
	    done
	done

	wait
	echo "===== HEVC Encoding 완료 ====="

	# ============================
	#  Decoding (이미지 PNG 출력)
	# ============================
	echo "===== PNG 추출 시작 ====="

	videos=(
	"1_bicycle bicycle 618 410"
	"2_bonsai bonsai 390 260"
	"3_counter counter 388 260"
	"4_flowers flowers 628 414"
	"5_garden garden 648 420"
	"6_kitchen kitchen 388 260"
	"7_room room 388 258"
	"8_stump stump 622 412"
	"9_treehill treehill 634 416"
	)

	for v in "${videos[@]}"; do
	    folder=$(echo $v | awk '{print $1}')
	    file=$(echo $v | awk '{print $2}')
	    width=$(echo $v | awk '{print $3}')
	    height=$(echo $v | awk '{print $4}')

	    for qp in "${qps[@]}"; do
	        outdir="${base_root}/${qp}/${folder}/images"
	        mkdir -p "$outdir"

	        ffmpeg -y -f rawvideo -pix_fmt yuv444p -s ${width}x${height} \
	            -i "${base_root}/recon/${file}_qp${qp}.yuv" \
	            "${outdir}/img_%06d.png"
	    done
	done

	echo "===== 모든 작업 완료 ====="


}

##############################################
# 3. 사용자 선택에 따라 실행
##############################################
case "$codec" in
    hevc)
        hevc_encode
        ;;
    jpeg)
        jpeg_compress
        ;;
    *)
        echo "❌ 잘못된 입력: $codec"
        exit 1
        ;;
esac

echo "===== 모든 작업 종료 ====="

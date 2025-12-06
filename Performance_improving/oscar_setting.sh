#local에서 oscar 사용을 위한 환경세팅
#pretrained model 및 SD-2.1 다운로드 필요

# test/
#  ├── gt                 ← jpeg50·70의 GT
#  ├── gt_for_jpeg10      ← jpeg10의 GT
#  ├── jpeg10
#  ├── jpeg50
#  └── jpeg70

sudo apt update
sudo apt install wget -y
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh


git clone https://github.com/jp-guo/OSCAR.git
cd OSCAR

conda env create -f environment.yml

conda activate oscar

cd ~/test/OSCAR
mkdir model_zoo

#https://huggingface.co/jinpeig/OSCAR/tree/main -> oscar.pkl 다운받아 model_zoo 안에 넣기
#SD-2.1 base 다운로드
sudo apt-get install git-lfs
git lfs install
git clone https://huggingface.co/Manojb/stable-diffusion-2-1-base
mv stable-diffusion-2-1-base OSCAR/model_zoo/stable-diffusion-2-1


#test.sh
                                
export CUDA_VISIBLE_DEVICES=0

dataset=""

accelerate launch --main_process_port main_test.py \
    -i "dataset/test/$dataset" \
    -o "results/${dataset}" \
    --pretrained_model_name_or_path="model_zoo/stable-diffusion-2-1" \
    --seed 123 \
    --oscar_path "model_zoo/oscar.pkl"


### If execute the following commands, uncomment them
CUDA_VISIBLE_DEVICES=1 python ./train.py \
 --source_path /workspace/ultrra_challenge/phase3/train \
 --evaluate_path /workspace/ultrra_challenge/phase3/test \
 --eval --scene_name ultrra_challenge_phase3 --model_path outputs/ultrra_challenge/phase3 --resolution 4 --iterations 1 \
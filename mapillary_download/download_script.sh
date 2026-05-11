#!/bin/bash


txt_file="/home/bliberat/workspace/dataset_download/STVchrono/stvchrono_v4_image_ids.txt"
image_ids=$(cat $txt_file)

for image_id in $image_ids; do
    python download_test.py "MLY|26090331160592224|8a683d8a5e743e11ac3e92e9b06820df" --image_id $image_id --destination /home/bliberat/iveco/datasets_iveco/STVchrono/$image_id
done
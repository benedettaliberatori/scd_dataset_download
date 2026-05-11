import os
import json
from datasets import Dataset, DatasetDict, Features, Image, Value

def get_dataset_for_folder(base_path, is_original=False):
    def gen():
        for city in sorted(os.listdir(base_path)):
            city_path = os.path.join(base_path, city)
            if not os.path.isdir(city_path): continue

            if is_original:
                for filename in sorted(os.listdir(city_path)):
                    if filename.lower().endswith(('.jpg', '.jpeg')):
                        img_path = os.path.join(city_path, filename)
                        image_id = os.path.splitext(filename)[0]
                        
                        yield {
                            "image": img_path,
                            "city": city,
                            "image_id": image_id,
                            "variation": "original",
                            "metadata": "{}"  
                        }

            else:
                for img_id in sorted(os.listdir(city_path)):
                    img_id_path = os.path.join(city_path, img_id)
                    if not os.path.isdir(img_id_path): continue
                    
                    for sub in sorted(os.listdir(img_id_path)):
                        sub_path = os.path.join(img_id_path, sub)
                        if not os.path.isdir(sub_path): continue

                        json_path = os.path.join(sub_path, "edit.json")
                        jpg_files = [f for f in os.listdir(sub_path) if f.lower().endswith(('.jpg', '.jpeg'))]

                        if os.path.exists(json_path) and jpg_files:
                            img_path = os.path.join(sub_path, jpg_files[0])
                            with open(json_path, 'r') as f:
                                try:
                                    metadata = json.load(f)
                                except:
                                    metadata = {"error": "json_corrupt"}
                            
                            yield {
                                "image": img_path,
                                "city": city,
                                "image_id": img_id,
                                "variation": sub,
                                "metadata": json.dumps(metadata)
                            }

    features = Features({
        "image": Image(),
        "city": Value("string"),
        "image_id": Value("string"),
        "variation": Value("string"),
        "metadata": Value("string"),
    })
    return Dataset.from_generator(gen, features=features)

original_folders = ["train"]
generated_folders = [
    "train_gen_v1", "train_gen_v1_seed0",
    "train_gen_v1_seed123", "train_gen_v1_seed456", "train_gen_v1_seed789",
    "train_gen_v2_seed42", "train_outpaint", "train_outpaint_homography",
    "train_overlap", "train_overlap_gen_v1", "train_overlap_gen_v1_seed123",
    "train_overlap_gen_v1_seed456", "train_overlap_gen_v1_seed789"
]

ds_dict = DatasetDict()

for folder in (original_folders + generated_folders):
    if os.path.exists(folder):
        print(f"--- Processing {folder} ---")
        is_orig = folder in original_folders
        ds_dict[folder] = get_dataset_for_folder(folder, is_original=is_orig)

print("\nPushing MapillaryPair to Hugging Face...")
ds_dict.push_to_hub("bliberatori/mapillary_generated", max_shard_size="500MB")
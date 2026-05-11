import os
import json
from datasets import Dataset, Features, Image, Value


def get_dataset_for_folder(base_path, mode="generated"):
    def gen():
        for city in sorted(os.listdir(base_path)):
            city_path = os.path.join(base_path, city)
            if not os.path.isdir(city_path): continue

            if mode == "original":
                for filename in sorted(os.listdir(city_path)):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        yield {
                            "image": os.path.join(city_path, filename),
                            "city": city,
                            "image_id": os.path.splitext(filename)[0],
                            "variation": "original",
                            "metadata": "{}"
                        }

            elif mode == "nested_no_json":
                for img_id in sorted(os.listdir(city_path)):
                    img_id_path = os.path.join(city_path, img_id)
                    if not os.path.isdir(img_id_path): continue

                    img_files = [f for f in os.listdir(img_id_path)
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    for img_name in img_files:
                        yield {
                            "image": os.path.join(img_id_path, img_name),
                            "city": city,
                            "image_id": img_id,
                            "variation": os.path.splitext(img_name)[0],
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
                            with open(json_path, 'r') as f:
                                metadata = json.load(f)
                            yield {
                                "image": os.path.join(sub_path, jpg_files[0]),
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



repo_id = "bliberatori/mapillary_pair_generated"

flat_folders = ["train", "train_overlap"]
nested_no_json_folders = ["train_outpaint_homography"]
generated_folders = [
    "train_gen_v1", "train_gen_v1_seed0", "train_gen_v1_seed123",
    "train_gen_v1_seed456", "train_gen_v1_seed789", "train_gen_v2_seed42",
    "train_overlap_gen_v1", "train_overlap_gen_v1_seed123",
    "train_overlap_gen_v1_seed456", "train_overlap_gen_v1_seed789"
]

all_tasks = [
    (flat_folders, "original"),
    (nested_no_json_folders, "nested_no_json"),
    (generated_folders, "generated")
]

for folder_list, run_mode in all_tasks:
    for folder in folder_list:
        if os.path.exists(folder):
            print(f"\n--- 🚀 Starting: {folder} (Mode: {run_mode}) ---")

            ds = get_dataset_for_folder(folder, mode=run_mode)

            if len(ds) > 0:
                print(f"Uploading {len(ds)} images...")
                ds.push_to_hub(repo_id, split=folder, max_shard_size="500MB")
                print(f"Success: {folder}")
            else:
                print(f"Skipping {folder}: No data found.")
        else:
            print(f"Missing: {folder}")

print("\n All Mapillary subsets have been processed!")
import os
import json
from datasets import Dataset, DatasetDict, Features, Image, Value

def get_dataset_for_folder(base_path):
    def gen():
        for city in sorted(os.listdir(base_path)):
            city_path = os.path.join(base_path, city)
            if not os.path.isdir(city_path): continue

            for img_dir in sorted(os.listdir(city_path)):
                img_dir_path = os.path.join(city_path, img_dir)
                if not os.path.isdir(img_dir_path): continue

               
                for sub in sorted(os.listdir(img_dir_path)):
                    sub_path = os.path.join(img_dir_path, sub)
                    if not os.path.isdir(sub_path): continue

                    json_path = os.path.join(sub_path, "edit.json")
                    jpg_files = [f for f in os.listdir(sub_path) if f.lower().endswith('.jpg')]

                    if os.path.exists(json_path) and jpg_files:
                        img_path = os.path.join(sub_path, jpg_files[0])
                        with open(json_path, 'r') as f:
                            metadata = json.load(f)

                        yield {
                            "image": img_path,
                            "city": city,
                            "folder_id": img_dir,
                            "variation": sub,
                            "metadata": json.dumps(metadata)
                        }

    features = Features({
        "image": Image(),
        "city": Value("string"),
        "folder_id": Value("string"),
        "variation": Value("string"),
        "metadata": Value("string"),
    })

    return Dataset.from_generator(gen, features=features)

target_folders = [
    "train_gen_v1",
    "train_gen_v1_seed123",
    "train_extra_gen_v1",
    "train_extra_gen_v1_seed123"
]

ds_dict = DatasetDict()

for folder in target_folders:
    if os.path.exists(folder):
        print(f"--- Processing {folder} ---")
        ds_dict[folder] = get_dataset_for_folder(folder)
    else:
        print(f"Warning: Folder {folder} not found. Skipping.")

print("\nPushing all splits to Hugging Face...")
ds_dict.push_to_hub("bliberatori/cityscapes_generated")
print("Upload Complete!")
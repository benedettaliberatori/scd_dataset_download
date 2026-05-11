import json 
import argparse
from urllib import response
import requests



def get_image_ids(annotations_list):
    """Get image ids from annotation files (PJ1_annotations, PJ2_annotations)."""

    annotations = []
    for ann_file in annotations_list:
        with open(ann_file, "r") as f:
            data = json.load(f)
            annotations.extend(data)

    all_image_ids = []
    for el in annotations:
        image_ids = [item["name"] for item in el["contents"]] 
        # NB: image ID from v3 may contain _ so we cannot use split("_")
        # but split removing the prefix date and suffix .jpg 
        image_ids = [i[11:-4] for i in image_ids]        
        assert all(len(i) == 22 for i in image_ids)
        all_image_ids.extend(image_ids)

    unique_image_ids = list(set(all_image_ids))
    print(f"Total image ids (with duplicates): {len(all_image_ids)}")
    print(f"Total unique image ids: {len(unique_image_ids)}")
    return unique_image_ids



def v3_to_v4_id_save(v3_ids_all, output_file, output_file_mapping):
    """Convert v3 image id to v4 image id and save to output file."""
    base_url = "https://www.mapillary.com/map/im/"
    with open(output_file, "w") as f, open(output_file_mapping, "w") as f_map:
        for v3_id in v3_ids_all:
            url = base_url + v3_id
            response = requests.get(url)
            final_url = response.url
            try:
              v4_id = final_url.split("pKey=")[1].split("&")[0]
              f.write(f"{v4_id}\n")
              f_map.write(f"{v3_id},{v4_id}\n")
            except:
              print(f"could not get {v3_id}")
    print(f"Converted IDs saved to {output_file}")


def v3_to_v4_id_retrieve(v3_id, mapping_file="stvchrono_v3_to_v4_image_ids.txt"):
    """Retrieve the v4 ID given the v3 ID by looking at precomputed ones (stvchrono_v3_to_v4_image_ids.txt)
    The txt contains lines with v3_id,v4_id
    """
    v3_to_v4_dict = {}
    with open(mapping_file, "r") as f:
        for line in f:
            v3, v4 = line.strip().split(",")
            v3_to_v4_dict[v3] = v4

    return v3_to_v4_dict.get(v3_id, None)


def organize_annotations_by_pair(annotations_list):
    """Organize annotations by image pairs.
    Retaining only unique captions for each pair."""
    organized_json = {}

    annotations = []
    for ann_file in annotations_list:
        with open(ann_file, "r") as f:
            data = json.load(f)
            annotations.extend(data)

    cnt = 0
    for el in annotations:
        if len(el["contents"]) != 2:
            continue # here I skip the continual change captioning setting (more than 2 images)

        image_A_id = el["contents"][0]["name"][11:-4]
        image_B_id = el["contents"][1]["name"][11:-4]

        image_A_id_v4 = v3_to_v4_id_retrieve(image_A_id)
        image_B_id_v4 = v3_to_v4_id_retrieve(image_B_id)

        if image_A_id_v4 is not None and image_B_id_v4 is not None:
            cnt += 1

        pair_key = f"{image_A_id}_{image_B_id}"
        captions_list = [item["value"] for item in el["attributes"]]
        if pair_key not in organized_json:
            organized_json[pair_key] = {"image_A": image_A_id, "image_B": image_B_id, "image_A_v4": image_A_id_v4, "image_B_v4": image_B_id_v4, "captions": captions_list}
        else: 
            existing_captions = organized_json[pair_key]["captions"]
            for caption in captions_list:
                if caption not in existing_captions:
                    existing_captions.append(caption)  
                     
    print(f"Total pairs with both v4 IDs found: {cnt}")
    return organized_json


def main(args):

    if args.get_image_ids:
        annotations_list = [args.annotations_dir1, args.annotations_dir2]
        image_ids = get_image_ids(annotations_list)

        with open("stvchrono_image_ids.txt", "w") as f:
            for img_id in image_ids:
                f.write(f"{img_id}\n")
        print("Image ids saved to stvchrono_image_ids.txt")
    
    if args.convert_v3_to_v4:
        with open("stvchrono_image_ids.txt", "r") as f:
            v3_ids_all = [line.strip() for line in f.readlines()]
        
        output_file = "stvchrono_v4_image_ids.txt"
        output_file_mapping = "stvchrono_v3_to_v4_mapping.txt"
        v3_to_v4_id_save(v3_ids_all, output_file, output_file_mapping)
    
    if args.organize_annotations:
        annotations_list = [args.annotations_dir1, args.annotations_dir2]
        organized_annotations = organize_annotations_by_pair(annotations_list)
        with open("stvchrono_organized_annotations.json", "w") as f:
            json.dump(organized_annotations, f, indent=4)
        print("Organized annotations saved to stvchrono_organized_annotations.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download STVChrono dataset.")
    parser.add_argument("--annotations_dir1", type=str, default="PJ1_annotations.json")
    parser.add_argument("--annotations_dir2", type=str, default="PJ2_annotations.json")
    parser.add_argument("--get_image_ids", action="store_true", help="Get image ids from annotation files.")
    parser.add_argument("--convert_v3_to_v4", action="store_true", help="Convert v3 image ids to v4 image ids.")
    parser.add_argument("--organize_annotations", action="store_true", help="Organize annotations by image pairs.")
    args = parser.parse_args()
    main(args)
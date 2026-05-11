import os
import requests
import argparse



def parse_args(argv =None):
    parser = argparse.ArgumentParser()
    parser.add_argument('access_token', type=str, help='Your mapillary access token')
    parser.add_argument('--sequence_ids', type=str, nargs='*', help='The mapillary sequence id(s) to download')
    parser.add_argument('--image_id', nargs='*', help='The mapillary image id(s) to get their sequence id(s)')
    parser.add_argument('--destination', type=str, default='data', help='Path destination for the images')
    parser.add_argument('--image_limit', type=int, default=None, help='How many images you want to download')
    parser.add_argument('--overwrite', default=False, action='store_true', help='overwrite existing images')
    parser.add_argument("-v", "--version", action="version", version="release 1.6")
    args = parser.parse_args(argv)
    if args.sequence_ids is None and args.image_id is None:
        parser.error("Please enter at least one sequence id or image id")
    return args


if __name__ == '__main__':
    
    args = parse_args()
    sequence_ids= args.sequence_ids if args.sequence_ids is not None else []
    image_id = args.image_id if args.image_id is not None else []
    access_token = args.access_token

    image_id = image_id[0]  # Assuming only one image ID is provided
    url = f"https://graph.mapillary.com/{image_id}?fields=thumb_original_url&access_token={access_token}"
    print(url)
    response = requests.get(url)
    data = response.json()

    if 'thumb_original_url' in data:
        image_url = data['thumb_original_url']

        img_data = requests.get(image_url).content

        output_directory = args.destination
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            
        with open(os.path.join(output_directory, f'{image_id}.jpg'), 'wb') as handler:
            handler.write(img_data)
        print(f"Successfully downloaded {image_id}.jpg")
    else:
        print("Error: Could not find image URL. Check your Token or ID.")
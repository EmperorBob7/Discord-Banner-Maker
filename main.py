import os
import random

from PIL import Image
import pprint
from typing import List, Dict, Tuple

# Configuration
IMAGE_FOLDER: str = "./images"
FRAME_DURATION: int = 2000  # milliseconds between frames
TARGET_SIZE: Tuple[int, int] = (1920, 1080)

# If True create a GIF such that one Artist appears at the start for each GIF
# IF False, only create 1 GIF
ONE_A_DAY = True

def get_images(folder: str) -> List[str]:
    """Get all image file paths in the folder."""
    exts: tuple = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def group_images(images: List[str]) -> Dict[str, List[str]]:
    """Group images by the first word before '#'."""
    groups: Dict[str, List[str]] = {}
    for img in images:
        filename_og: str = os.path.basename(img)
        filename: str = os.path.splitext(filename_og)[0]
        if '#' in filename:
            group_name: str = filename.split('#')[0].lower()
        else:
            group_name: str = filename.lower()  # single-image group if no '#'
        
        if group_name not in groups:
          groups[group_name] = []
        groups[group_name].append(img)
    pprint.pprint(groups)
    return groups

def main() -> None:
    os.makedirs("./outputGifs", exist_ok=True)

    images: List[str] = get_images(IMAGE_FOLDER)
    
    grouped_images_dict: Dict[str, List[str]] = group_images(images)
    grouped_images: List[List[str]] = list(grouped_images_dict.values())
    random.shuffle(grouped_images)

    # Shuffle images within each group
    for group in grouped_images:
        random.shuffle(group)

    # Load Images
    grouped_loaded_images: List[List[Image.Image]] = []
    for group in grouped_images:
        arr: List[Image.Image] = []
        for image in group:
            arr.append(Image.open(image).convert('RGBA').resize(TARGET_SIZE, Image.Resampling.LANCZOS))
        grouped_loaded_images.append(arr)

    num_gifs = len(grouped_loaded_images)
    for index in range(num_gifs):
        # Flatten List
        pil_images: List[Image.Image] = [img for group in grouped_loaded_images for img in group]
        
        # Save as GIF
        if pil_images:
            OUTPUT_GIF = f"./outputGifs/File{index}.gif"
            pil_images[0].save(
                OUTPUT_GIF,
                save_all=True,
                append_images=pil_images[1:],
                duration=FRAME_DURATION,
                loop=0  # loop forever
            )
            print(f"GIF saved as {OUTPUT_GIF} with {len(pil_images)} frames.")
        
        if not ONE_A_DAY:
            break

        # Cycle the Carousel
        group_pop = grouped_loaded_images.pop(0)
        grouped_loaded_images.append(group_pop)

if __name__ == "__main__":
    main()
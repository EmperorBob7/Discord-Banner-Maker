import math
import os
import random
from PIL import Image, ImageSequence
import pprint
from typing import List, Dict, Tuple

IMAGE_FOLDER: str = "./images"
FRAME_DURATION: int = 3000
WIDTH: int = 1920 # Minimum resolution is 960x540, Size Max is 10MB
TARGET_SIZE: Tuple[int, int] = (WIDTH, int(WIDTH * 9 / 16))

NUM_BANNERS = 3 # 0 for one for every artist, X otherwise
SEGREGATE_GIFS = True # False if you want all banners in every gif

def get_images(folder: str) -> List[str]:
    exts: tuple = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def get_group_name(filename: str):
    if '#' in filename:
        group_name = filename.split('#')[0].lower()
    else:
        group_name = filename.lower()
    return group_name

def group_images(images: List[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for img in images:
        filename_og = os.path.basename(img)
        filename = os.path.splitext(filename_og)[0]
        group_name = get_group_name(filename)
        groups.setdefault(group_name, []).append(img)
    pprint.pprint(groups)
    return groups

def load_image_preserving_gif(path: str) -> Tuple[List[Image.Image], List[int]]:
    """Load an image. If GIF, preserve all frames + durations."""
    img = Image.open(path)

    if img.format == "GIF":
        frames = []
        durations = []

        for frame in ImageSequence.Iterator(img):
            frames.append(
                frame.convert("RGBA").resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            )
            durations.append(frame.info.get("duration", FRAME_DURATION))

        return frames, durations

    # Non-gif -> single frame image
    frame = img.convert("RGBA").resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    return [frame], [FRAME_DURATION]

def main() -> None:
    os.makedirs("./outputGifs", exist_ok=True)

    images: List[str] = get_images(IMAGE_FOLDER)
    grouped: list[List[str]] = list(group_images(images).values())
    random.shuffle(grouped)

    for frames_group in grouped:
        random.shuffle(frames_group)

    # Load all images + durations
    grouped_frames: List[List[Image.Image]] = []
    grouped_durations: List[List[int]] = []
    grouped_names: List[str] = []

    for frames_group in grouped:
        frames: List[Image.Image] = []
        durations: List[int] = []
        sorted_group = sorted(frames_group)
        print(f"Sorted Group: {sorted_group}")
        for path in sorted_group:
            f, d = load_image_preserving_gif(path)
            frames.extend(f)
            durations.extend(d)
        grouped_frames.append(frames)
        grouped_durations.append(durations)
        grouped_names.append(get_group_name(frames_group[0]))

    num_artists = len(grouped_names)
    num_gifs = NUM_BANNERS
    if NUM_BANNERS == 0:
        num_gifs = num_artists

    artists_per_gif = num_artists
    if SEGREGATE_GIFS:
        artists_per_gif = math.ceil(num_artists / num_gifs) 

    seg_total_artists = 0
    for index in range(num_gifs):
        frames: List[Image.Image] = []
        durations: List[int] = []
        names: List[str] = []
        for artist_index in range(artists_per_gif):
            if SEGREGATE_GIFS and seg_total_artists >= num_artists:
                break
            seg_total_artists += 1
            # Rounding
            if artist_index >= num_artists:
                break
            # Accumulate Frames
            frames_group = grouped_frames[artist_index]
            for f in frames_group:
                frames.append(f)
            # Accumulate Durations
            durations_group = grouped_durations[artist_index]
            for d in durations_group:
                durations.append(d)
            names.append(grouped_names[artist_index])
        
        # Make the gif
        if frames:
            OUTPUT_GIF = f"./outputGifs/File{index}.gif"
            frames[0].save(
                OUTPUT_GIF,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0
            )
            print(f"Saved {OUTPUT_GIF} with {len(frames)} frames - {len(names)} artists - {names}")

        # rotate groups
        num_to_shift = 1
        if SEGREGATE_GIFS:
            num_to_shift = artists_per_gif
        for i in range(num_to_shift):
            grouped_frames.append(grouped_frames.pop(0))
            grouped_durations.append(grouped_durations.pop(0))
            grouped_names.append(grouped_names.pop(0))


if __name__ == "__main__":
    main()

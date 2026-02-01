import os
import random
from PIL import Image, ImageSequence
import pprint
from typing import List, Dict, Tuple

IMAGE_FOLDER: str = "./images"
FRAME_DURATION: int = 3000
WIDTH: int = 960 # Minimum resolution is 960x540, Size Max is 10MB
TARGET_SIZE: Tuple[int, int] = (WIDTH, int(WIDTH * 9 / 16))

ONE_A_DAY = True

def get_images(folder: str) -> List[str]:
    exts: tuple = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

def group_images(images: List[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for img in images:
        filename_og = os.path.basename(img)
        filename = os.path.splitext(filename_og)[0]
        if '#' in filename:
            group_name = filename.split('#')[0].lower()
        else:
            group_name = filename.lower()
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

    images = get_images(IMAGE_FOLDER)
    grouped = list(group_images(images).values())
    random.shuffle(grouped)

    for group in grouped:
        random.shuffle(group)

    # Load all images + durations
    grouped_frames = []
    grouped_durations = []

    for group in grouped:
        frames = []
        durations = []
        sorted_group = sorted(group)
        print(f"Sorted Group: {sorted_group}")
        for path in sorted_group:
            f, d = load_image_preserving_gif(path)
            frames.extend(f)
            durations.extend(d)
        grouped_frames.append(frames)
        grouped_durations.append(durations)

    num_gifs = len(grouped_frames)

    for index in range(num_gifs):
        frames = [f for group in grouped_frames for f in group]
        durations = [d for group in grouped_durations for d in group]

        if frames:
            OUTPUT_GIF = f"./outputGifs/File{index}.gif"
            frames[0].save(
                OUTPUT_GIF,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0
            )
            print(f"Saved {OUTPUT_GIF} with {len(frames)} frames.")

        if not ONE_A_DAY:
            break

        # rotate groups
        grouped_frames.append(grouped_frames.pop(0))
        grouped_durations.append(grouped_durations.pop(0))


if __name__ == "__main__":
    main()

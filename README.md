# Requirements
```
python3
pip
```

# How to Use
- Clone the repository (or download it)
- Inside the repository, create a directory `images`
- Label images in `GROUP_NAME#ImageNumber.('.png', '.jpg', '.jpeg', '.bmp', '.gif')` format. `#ImageNumber` isn't necessary if a GROUP has only 1 image.
  - Yes the `#` in the previous line means literally the hashtag character. Ex: `EmperorBob#0.png`, `EmperorBob#1.png`.
  - The numbers you choose don't actually matter.
- Run the commands below
- If you only want ONE final GIF, set `ONE_A_DAY` in `main.py` to `False`

```
python -m venv venv

# Windows
.\venv\Scripts\activate.bat

# macOS / Linux
source ./venv/bin/activate

# Everyone
pip install -r requirements.txt
python ./main.py
```
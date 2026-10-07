import glob
import os.path
import shutil
import string
import time

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")
INPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "input")
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "output")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")



# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------

if os.path.exists(INPUT_FOLDER):
    for file in glob.glob(f"{INPUT_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(INPUT_FOLDER)
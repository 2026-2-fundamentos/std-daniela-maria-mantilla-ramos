import glob
import os.path
import shutil
import string
import time
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_FOLDER = ACTIVITY_DIR / "data"
INPUT_FOLDER = ACTIVITY_DIR / "temp" / "input"
OUTPUT_FOLDER = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_FOLDER = ACTIVITY_DIR / "submission"

# FUNCIONES -----------------------------------------------------------------------------
def clear_folder(folder): #limpia el folder
    for file in glob.glob(f"{folder}/*"):
        os.remove(file)

def initialize_folder(folder): #inicia el folder
    if os.path.exists(folder):
        clear_folder(folder)
    else:
        os.makedirs(folder)

def delete_folder(folder): #borra el folder
    if os.path.exists(folder):
        shutil.rmtree(folder)

def generate_file_copies(n): # Genera copias de los archivos en raw/
    for file in glob.glob(f"{DATA_FOLDER}/*"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)

            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

            new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

            with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)

def mapper(sequence):# Mapper
    pairs_sequence = []
    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.replace("\n", "")
        words = line.split()
        pairs_sequence.extend([(word, 1) for word in words])
    return pairs_sequence

def reducer(pairs_sequence): # Reducer
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result

def hadoop(
        input_folder,
        output_folder,
        mapper,
        reducer,
):
    def read_records_from_input():# Lectura de los archivos
        sequence = [] 
        files = glob.glob(f"{input_folder}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence
    
    def shuffle_and_sort(pairs_sequence): # Shuffle and sort
        pairs_sequence = sorted(pairs_sequence)
        return pairs_sequence
    
    def save_results_to_output(result): # Archivo con el conteo
        with open(f"{output_folder}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")

    def create_success_file(): # Marcador de éxito
        with open(f"{output_folder}/_SUCCESS", "w", encoding="utf-8") as f:
            f.write("")
    
    def fail_if_output_exists():
        if os.path.exists(output_folder):
            raise Exception(
                f"Output folder '{output_folder}' already exists. Please delete it vefore running the job.")
        else:
            os.makedirs(output_folder)
    
    sequence = read_records_from_input()
    pairs_sequence = mapper(sequence)
    pairs_sequence = shuffle_and_sort(pairs_sequence)
    result = reducer(pairs_sequence)
    fail_if_output_exists()
    save_results_to_output(result)
    create_success_file()

def copy_hdfs_output_to_submission(output_folder, submission_folder):
    initialize_folder(submission_folder)
    for file in glob.glob(f"{output_folder}/*"):
        shutil.copy2(file, submission_folder)



    initialize_folder(INPUT_FOLDER)
    delete_folder(OUTPUT_FOLDER)
    generate_file_copies(1000)
    start_time = time.time()


# CÓDIGO PRINCIPAL -----------------------------------------------------------------------------
if __name__ == "__main__":
    n = 1000
    initialize_folder(INPUT_FOLDER)
    generate_file_copies(n)
    start_time = time.time()
    hadoop(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        mapper=mapper,
        reducer=reducer,)
    copy_hdfs_output_to_submission(OUTPUT_FOLDER, SUBMISSION_FOLDER)
    end_time = time.time() # Reporte de tiempo de ejecución
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
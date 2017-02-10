import vcf
import argparse

from keras.models import *

def main(paths):
    model = load_model(paths['input'])

def prep_input_samples(array_sizes, x_training_data):
    count = 0
    X_fb = np.array(map(lambda x: x[count:array_sizes[0]], x_training_data))
    count += array_sizes[0]
    X_hc = np.array(map(lambda x: x[count:count + array_sizes[1]], x_training_data))
    count += array_sizes[1]
    X_ug = np.array(map(lambda x: x[count:count + array_sizes[2]], x_training_data))
    count += array_sizes[2]
    X_pindel = np.array(map(lambda x: x[count:count + array_sizes[3]], x_training_data))
    count += array_sizes[3]
    X_st = np.array(map(lambda x: x[count:count + array_sizes[4]], x_training_data))
    count += array_sizes[4]
    return X_fb, X_hc, X_pindel, X_st, X_ug

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description="train neural net")
    parser.add_argument('-m', '--model', help="give directories with files")
    parser.add_argument('-i', '--input', help="give directories with files")
    input_path = parser.parse_args()
    input_path = vars(input_path)
    main_gather_input_execute_prep_output(input_path)
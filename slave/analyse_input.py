import vcf
import argparse

from keras.models import *


def execute_main(input, model, training):
    model = load_model(model)
    X_fb, X_hc, X_ug_ X = prep_input_samples()
    model.predict(input)


def main(paths):
    input, model, training = load_references(paths)
    execute_main(input,model,training)


def load_references(paths):
    paths = vars(paths)
    input = load_model(paths['input'])
    model = load_model(paths['model'])
    training = load_model(paths['training'])



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
    return X_fb, X_hc, X_ug, X_pindel, X_st

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description="train neural net")
        parser.add_argument('-t', '--training', help="give directories with files")
    parser.add_argument('-m', '--model', help="give directories with files")
    parser.add_argument('-i', '--input', help="give directories with files")
    input_path = parser.parse_args()
    input_path = vars(input_path)
    main_gather_input_execute_prep_output(input_path)
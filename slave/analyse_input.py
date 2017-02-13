from keras.models import *

from ANNgeneratematrixes import *


def main(paths):
    input, model, reference, output = load_references(paths)
    generate_matrixes(input, model, reference, output)


def predone_train_neural_net(length_of_caller_outputs, my_x_dataset, model):
    X_1, X_2, X_3, X_4, X_5 = prep_input_samples(length_of_caller_outputs, my_x_dataset)
    final_predictions = model.predict([X_1, X_2, X_3, X_4, X_5])


# INPUT MUST BE A DIRECTORY!

def generate_matrixes(input, model, reference, outputpath):
    length_of_caller_outputs, list_of_called_samples, vcf_list = generate_input(input, reference)
    my_x_dataset = check_predicted_with_truth(list_of_called_samples)
    calculated_prediction_actual = predone_train_neural_net(length_of_caller_outputs, my_x_dataset, model)
    list_of_records = create_list_of_records(calculated_prediction_actual, vcf_list)
    vcf_reader = vcf.Reader(filename=original_vcf_reader)
    vcf_writer = vcf.Writer(open(outputpath + "truevcf.vcf", 'w'), vcf_reader)
    for record in list_of_records:
        vcf_writer.write_record(record)


def create_list_of_records(calculated_prediction_actual, vcf_dictionary):
    list_of_records = []
    for i in range(len(list_of_samples_input)):
        if calculated_prediction_actual[i] == 1:
            item = list_of_samples_input[i]
            list_of_records.append(vcf_dictionary[item[0]])
    return list_of_records


def load_references(paths):
    paths = vars(paths)
    input = paths['input']
    model = load_model(paths['model'])
    reference = paths['reference']
    output = paths['output']
    return input, model, reference, output


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
    parser.add_argument('-r', '--reference', help="give directories with files")
    parser.add_argument('-m', '--model', help="give directories with files")
    parser.add_argument('-i', '--input', help="give directories with files")
    parser.add_argument('-o', '--output', help="give directories with files")
    input_path = parser.parse_args()
    input_path = vars(input_path)
    main_gather_input_execute_prep_output(input_path)

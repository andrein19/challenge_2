import argparse
import csv
import datetime
import os
import random


def data_points(file):
    """
    return list with 10 data points from random timestamp
    """
    items_list = []

    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csv_list = list(csv_reader)
        csv_size = len(csv_list)

        index_random_line = random.randint(0, csv_size - 9)

        for items in csv_list[index_random_line:index_random_line + 9]:
            items_list.append(items)

        return items_list


def predict(input_data: list):
    """
    return list with predicted values
    """
    computed_values = []
    print(input_data)

    # data points
    n_value = float('{:.2f}'.format(float(input_data[-1][2])))
    n1_value = float('{:.2f}'.format(sorted([float(row[2]) for row in input_data], reverse=True)[1]))
    n2_value = float('{:.2f}'.format(n1_value + (n_value - n1_value) / 2))
    n3_value = float('{:.2f}'.format(n2_value + (n_value - n1_value) / 4))

    computed_values.append(n1_value)
    computed_values.append(n2_value)
    computed_values.append(n3_value)

    timestamp = datetime.datetime.strptime(input_data[-1][1], '%d-%m-%Y')
    delta = datetime.timedelta(days=1)

    output_list = []
    i = 0

    for value in computed_values:
        i = i + 1
        timestamp_inc = timestamp + (i * delta)
        formatted_date = timestamp_inc.strftime('%d-%m-%Y')
        output = ([input_data[-1][0], formatted_date, value])
        output_list.append(output)

    return output_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help='input directory')
    args = parser.parse_args()
    input_dir = args.input

    file_path_list = []
    os.makedirs("output", exist_ok=True)

    if os.path.isdir(input_dir):
        print(f"Input directory is '{input_dir}'")

        for dirpath, dirnames, filenames in os.walk(input_dir):
            if not os.listdir(input_dir):
                print(f"Directory '{dirpath}' is empty. Nothing to process")
                pass
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                file_path_list.append(file_path)
    else:
        print(f"Directory '{input_dir}' is invalid. "
              f"\nYou need to provide a valid directory")

    for file_path in file_path_list:
        print(f"\n Processed file is {file_path}")
        predicted = predict(data_points(file_path))
        print(predicted)
        filename = file_path.rsplit('.')[0].split('/')[2]

        with open(f'output/{filename}.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in predicted:
                csv_writer.writerow(row)


if __name__ == "__main__":
    main()

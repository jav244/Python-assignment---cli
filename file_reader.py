import re
import csv
import pathlib


class FileReader:
    def __init__(self):
        # self.file_reader(file)
        self.full_data_dics = []

    def read_file(self, file):
        if pathlib.Path(file).suffix == ".txt":
            self.txt_reader(file)
        elif pathlib.Path(file).suffix == ".csv":
            self.csv_reader(file)
        else:
            raise Exception('Unknown file type')
        return self.full_data_dics

    def txt_reader(self, the_file):
        with open(the_file, 'r') as f:
            f = f.read()
            self.data_sets = f.split("\n")
            for x in self.data_sets:
                self.data_splitter(x)

    def data_splitter(self, data_set):
        lines = re.split(",|/|\s", data_set)
        data_dic = {'Empid': None, 'Gender': None, 'Age': None, 'Sales': None, 'BMI': None, 'Salary': None,
                    'Birthday': None}

        data_dic['Empid'] = lines[0]
        data_dic['Gender'] = lines[1]
        data_dic['Age'] = lines[2]
        data_dic['Sales'] = lines[3]
        data_dic['BMI'] = lines[4]
        data_dic['Salary'] = lines[5]
        data_dic['Birthday'] = lines[6]

        # self.data_validate(data_dic)
        self.full_data_dics.append(data_dic)

    def csv_reader(self, the_file):
        with open(the_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data_splitter_csv(row)

    def data_splitter_csv(self, row):
        data_dic = {'Empid': None, 'Gender': None, 'Age': None, 'Sales': None, 'BMI': None, 'Salary': None,
                    'Birthday': None}

        data_dic['Empid'] = row['Empid']
        data_dic['Gender'] = row['Gender']
        data_dic['Age'] = row['Age']
        data_dic['Sales'] = row['Sales']
        data_dic['BMI'] = row['BMI']
        data_dic['Salary'] = row['Salary']
        data_dic['Birthday'] = row['Birthday']

        # self.data_validate(data_dic)
        self.full_data_dics.append(data_dic)

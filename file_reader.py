import re
import csv
import pathlib
from abc import ABCMeta, abstractmethod

# client
class FileReader:
    def __init__(self, file):
        self.__file = file
        self.__full_data_dics = []

    def read_file(self):
        if pathlib.Path(self.__file).suffix == ".txt":
            txt_file = TxtRead(self.__file)
            txt_read = Reader(txt_file)
            self.__full_data_dics = txt_read.return_file_data()
        elif pathlib.Path(self.__file).suffix == ".csv":
            csv_file = CsvRead(self.__file)
            csv_read = Reader(csv_file)
            self.__full_data_dics = csv_read.return_file_data()
        else:
            raise Exception('Unknown file type')
        return self.__full_data_dics


# context
class Reader:
    def __init__(self, type):
        self.file_type = type

    def return_file_data(self):
        data = self.file_type.read()
        return data


# interface for strategy
class AbstractFileRead(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass


# concrete strategy 1
class TxtRead(AbstractFileRead):
    def __init__(self, the_file):
        self.__full_data_dics = []
        self.__file = the_file

    def read(self):
        with open(self.__file, 'r') as f:
            f = f.read()
            data_sets = f.split("\n")
            for x in data_sets:
                self.__data_splitter(x)
            return self.__full_data_dics

    def __data_splitter(self, data_set):
        lines = re.split(",|/|\s", data_set)
        data_dic = {'Empid': lines[0],
                    'Gender':lines[1],
                    'Age': lines[2],
                    'Sales': lines[3],
                    'BMI': lines[4],
                    'Salary': lines[5],
                    'Birthday': lines[6]}

        self.__full_data_dics.append(data_dic)


# concrete strategy 2
class CsvRead(AbstractFileRead):
    def __init__(self, the_file):
        self.__full_data_dics = []
        self.__file = the_file

    def read(self):
        with open(self.__file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.__data_splitter_csv(row)
            return self.__full_data_dics

    def __data_splitter_csv(self, row):
        data_dic = {'Empid': row['Empid'],
                    'Gender': row['Gender'],
                    'Age': row['Age'],
                    'Sales': row['Sales'],
                    'BMI': row['BMI'],
                    'Salary': row['Salary'],
                    'Birthday': row['Birthday']}

        self.__full_data_dics.append(data_dic)







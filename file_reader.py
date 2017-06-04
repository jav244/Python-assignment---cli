import re
import csv
import pathlib
from abc import ABCMeta, abstractmethod


class FileReader:
    def __init__(self, file):
        self.file = file
        self.full_data_dics = []

    def read_file(self):
        if pathlib.Path(self.file).suffix == ".txt":
            txt_file = TxtFactory()
            self.reader(txt_file, self.file)
        elif pathlib.Path(self.file).suffix == ".csv":
            csv_file = CsvFactory()
            self.reader(csv_file, self.file)
        else:
            raise Exception('Unknown file type')
        return self.full_data_dics

    def reader(self, factory, file):
        read = factory.read()
        data_set = read.read_file(file)

        catalogue = factory.organize()
        self.full_data_dics = catalogue.organize(data_set)


# abstract factory
class FileFactory(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def organize(self):
        pass


# concrete factory 1
class CsvFactory(FileFactory):
    def read(self):
        return CsvRead()

    def organize(self):
        return CsvCatalogue()


# concrete factory 2
class TxtFactory(FileFactory):
    def read(self):
        return TxtRead()

    def organize(self):
        return TxtCatalogue()


# abstract product A
class Read(metaclass=ABCMeta):
    @abstractmethod
    def read_file(self):
        pass


# concrete product A1
class CsvRead(Read):
    def read_file(self, the_file):
        data_set = csv.DictReader(open(the_file))
        return data_set



# concrete product A2
class TxtRead(Read):
    def read_file(self, the_file):
        with open(the_file, 'r') as f:
            file = f.read()
            data_sets = file.split("\n")
            return data_sets


# abstract product B
class Catalogue(metaclass=ABCMeta):
    @abstractmethod
    def organize(self):
        pass


# concrete product B1
class CsvCatalogue(Catalogue):
    def organize(self, data_set):
        full_data_dic = []
        for row in data_set:
            data_dic = {'Empid': row['Empid'],
                        'Gender': row['Gender'],
                        'Age': row['Age'],
                        'Sales': row['Sales'],
                        'BMI': row['BMI'],
                        'Salary': row['Salary'],
                        'Birthday': row['Birthday']}

            full_data_dic.append(data_dic)
        return full_data_dic


# concrete product B2
class TxtCatalogue(Catalogue):
    def organize(self, data_set):
        full_data_dic = []
        for row in data_set:
            lines = re.split(",|/|\s", row)
            data_dic = {'Empid': lines[0],
                        'Gender': lines[1],
                        'Age': lines[2],
                        'Sales': lines[3],
                        'BMI': lines[4],
                        'Salary': lines[5],
                        'Birthday': lines[6]}

            full_data_dic.append(data_dic)
        return full_data_dic





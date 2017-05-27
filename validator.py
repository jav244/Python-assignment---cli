import re
from datetime import date
from file_reader import FileReader


# large class -- bad smell 2
class Validator:
    def __init__(self):
        # self.file_reader(file)
        self.reg_dic = {"Empid": '[A-Z][0-9]{3}$',
                        "Gender": '^M$|^F$',
                        "Age": '^[0-9]{2,3}$',
                        "Sales": '^[0-9]{2,3}$',
                        "BMI": '(^Normal$|^Overweight$|^Obesity$|^Underweight$)',
                        "Salary": '^[0-9]{2,3}$',
                        "Birthday": '^(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4})$'}
        self.data_sets = []
        self.clean_data_sets = []
        self.unclean_data_sets = []
        self.invalid_data = []
        self.empids = []

    def find_age(self, key, value, data_dic):
        if key == "Age":
            age = data_dic[key]
            for xkey in data_dic:
                if xkey == "Birthday":
                    birthday = data_dic[xkey]
                    if self.validate_age(age, birthday):
                        return value
                    else:
                        return "invalid"
        else:
            return value

    # long method -- bad smell 1
    def data_validate(self, data_dic):
        valid_data_dic = {}
        valid = True

        for key, value in data_dic.items():
            try:
                match = re.search(self.reg_dic[key], value, re.I)
                if match:
                    valid_data_dic[key] = self.find_age(key, value, data_dic)
                else:
                    valid_data_dic[key] = "invalid"
                    self.invalid_data.append("invalid " + key + " " + value)
            except Exception as e:
                return e

        for key in valid_data_dic:
            if valid_data_dic[key] == "invalid":
                valid = False

        if valid:
            self.clean_data_sets.append(valid_data_dic)

    def validate_age(self, age, birthdate):
        """
        >>> Validator().validate_age(24, '08-05-1992')
        True

        >>> Validator().validate_age(24, '08/05/1992')
        True

        >>> Validator().validate_age(25, '08/05/1992')
        False
        """
        birthdate = re.split('-|/', birthdate)
        day = int(birthdate[0])
        month = int(birthdate[1])
        year = int(birthdate[2])

        valid_birth_age = False
        valid_age = False
        valid_year = False

        if year < date.today().year:
            valid_year = True

        dob = date(year, month, day)
        today = date.today()
        if today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) == int(age):
            valid_age = True

        if valid_age & valid_year:
            valid_birth_age = True

        assert type(valid_birth_age) is bool
        return valid_birth_age

    def validate(self, file, id):
        self.invalid_data = []
        self.clean_data_sets = []

        file_reader = FileReader()
        file_data = file_reader.read_file(file)
        for data_dic in file_data:
            self.data_validate(data_dic)

        if self.invalid_data:
            if id == "file":
                return self.invalid_data + self.clean_data_sets
            if id == "db":
                return self.clean_data_sets
        else:
            return self.clean_data_sets


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod(verbose=True)

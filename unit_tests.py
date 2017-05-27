import unittest
import io
import sys
from controller import Controller
from cmd_view import CmdView
from data_visualiser import DataVis
from validator import Validator
from format import Format
from database import Database
from serialize import Pickle


class MainTests(unittest.TestCase):
    def test_ageValidator(self):
        val = Validator()

        result = val.validate_age(25, '08-05-1992')

        self.assertTrue(result == True, "result should equal true")

    def test_badAgeValidator(self):
        val = Validator()

        result = val.validate_age(26, '08-05-1992')

        self.assertTrue(result == False, "result should equal false")

    def test_noData_Display(self):
        view = CmdView()
        data_vis = DataVis()
        validator = Validator()
        format = Format()
        pickle = Pickle()
        db = Database('company.db')

        con = Controller(view, data_vis, validator, format, pickle, db)
        view.controller_set(con)

        captured = io.StringIO()
        sys.stdout = captured

        con.display("bar")

        expected = "there is no data in database\n" \
                   "there is no data in database\n" \
                   "there is no data in database\n" \
                   "'NoneType' object is not iterable\n"

        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_fileDataValidator(self):
        val = Validator()

        data = val.validate("data/data.txt", "file")

        self.assertTrue(data[0] == 'invalid BMI norm', "result should equal the first invalid bit of data")

    def test_fileDataValidator_Clean(self):
        val = Validator()

        data = val.validate("data/data-clean.txt", "file")

        self.assertTrue(data[0] == {'Empid': 'E001', 'Gender': 'F', 'Age': '25', 'Sales': '123', 'BMI': 'overweight',
                                    'Salary': '350', 'Birthday': '08-05-1992'},
                        "result should equal the first line of good data")

    def test_fileDataValidator_Csv(self):
        val = Validator()

        data = val.validate("data/data.csv", "file")

        self.assertTrue(data[0] == 'invalid Empid X12', "result should equal the first invalid bit of data")

    def test_fileDataValidator_Csv_Clean(self):
        val = Validator()

        data = val.validate("data/data-clean.csv", "file")

        self.assertTrue(data[0] == {'Empid': 'A123', 'Gender': 'm', 'Age': '26', 'Sales': '987', 'BMI': 'overweight',
                                    'Salary': '192', 'Birthday': '14/10/1990'},
                        "result should equal the first line of good data")

    def test_fileDataValidator_InvalidFile(self):
        val = Validator()

        try:
            val.validate("data/data.pdf", "file")
        except Exception as e:
            error = str(e)

        self.assertTrue(error == 'Unknown file type')

    def test_dbDataValidator(self):
        val = Validator()

        data = val.validate("data/data.txt", "db")

        self.assertTrue(data[0] == {'Empid': 'E001', 'Gender': 'F', 'Age': '25', 'Sales': '123', 'BMI': 'overweight',
                                    'Salary': '350', 'Birthday': '08-05-1992'},
                        "result should equal the first line of good data")

    def test_cleaner(self):
        frm = Format()

        x = [(330,), (700,), (330,), (200,), (128,), (200,), (100,), (200,)]

        f = frm.clean(x)

        self.assertTrue(f == [330, 700, 330, 200, 128, 200, 100, 200],
                        "result should be [330, 700, 330, 200, 128, 200, 100, 200]")

    def test_db_gooddata_txtFile(self):
        val = Validator()
        db = Database('company.db')

        data = val.validate("data/data.txt", "db")

        errors = []
        for x in data:
            try:
                db.insert(x)
            except Exception as e:
                errors.append((str(e) + " --- " + str(x.get("Empid"))))

        result = db.query("*")

        row = result[1]

        self.assertTrue(row == ('E002', 'M', 27, 145, 'obesity', 330, '08-05-1990'),
                        "the result should be ('E002', 'M', 27, 145, 'obesity', 330, '08-05-1990')")

    def test_db_gooddata_csvFile(self):
        val = Validator()
        db = Database('company.db')

        data = val.validate("data/data.csv", "db")

        errors = []
        for x in data:
            try:
                db.insert(x)
            except Exception as e:
                errors.append((str(e) + " --- " + str(x.get("Empid"))))

        result = db.query("*")

        row = result[0]

        self.assertTrue(row == ('A123', 'm', 26, 987, 'overweight', 192, '14/10/1990'),
                        "the result should be ('A123', 'm', 26, 987, 'overweight', 192, '14/10/1990')")

    def test_db_UniqueIDBad(self):
        val = Validator()
        db = Database('company.db')

        data = val.validate("data/data.txt", "db")

        errors = []
        for x in data:
            try:
                db.insert(x)
            except Exception as e:
                errors.append((str(e) + " --- " + str(x.get("Empid"))))

        result = db.query("*")

        row = result[1]

        error = errors[0]

        self.assertTrue(error == ('UNIQUE constraint failed: Employee.EMPID --- Q258'),
                        "the result should be ('UNIQUE constraint failed: Employee.EMPID --- Q258')")


if __name__ == '__main__':  # pragma: no cover
    # unittest.main(verbosity=2)  # with more details
    unittest.main()

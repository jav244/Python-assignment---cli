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


class ConTests(unittest.TestCase):
    def setUp(self):
        view = CmdView()
        data_vis = DataVis()
        validator = Validator()
        format = Format()
        pickle = Pickle()
        db = Database('company.db')

        self.con = Controller(view, data_vis, validator, format, pickle, db)
        view.controller_set(self.con)

    def test_pieChart(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.con.database_insert("data.txt")
        self.con.display("pie")

        regex = '^file://C:/Users/Jacob/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_barChart(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.con.database_insert("data.txt")
        self.con.display("bar")

        regex = '^file://C:/Users/Jacob/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_queryDatabase_exception(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.con.database_insert("data.txt")
        self.con.database_query("date_of_birth")

        expected = "no such column: date_of_birth\n"

        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_fileReader_txtFile(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.con.file_reader("data/data1.txt")

        expected = "{'Empid': 'E001', 'Gender': 'F', 'Age': '25', 'Sales': '123', 'BMI': 'overweight', " \
                   "'Salary': '350', 'Birthday': '08-05-1992'}\n"
        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_fileReader_csvFile(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.con.file_reader("data/data1.csv")

        expected = "{'Empid': 'A123', 'Gender': 'm', 'Age': '26', 'Sales': '987', 'BMI': 'overweight', " \
                   "'Salary': '192', 'Birthday': '14/10/1990'}\n"
        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_fileReader_invalidFile(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.con.file_reader("data/data1.pdf")

        expected = "Unknown file type\n"
        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_invalidChart(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.con.display("pineapple")

        expected = "not a valid flag\n"
        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_pickleCreate(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.con.database_insert("data/data1.txt")
        self.con.serialize("create", "pikdata")

        expected = "success: pickle saved as pikdata\n"
        actual = captured.getvalue()

        self.assertEqual(expected, actual)

    def test_pickleOpen(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.con.serialize("open", "pikdata")

        expected = "('E003', 'F', 25, 134, 'normal', 700, '10-07-1991')"
        actual = captured.getvalue().split("\n")[0]

        self.assertEqual(actual, expected)


if __name__ == '__main__':  # pragma: no cover
    # unittest.main(verbosity=2)  # with more details
    unittest.main()

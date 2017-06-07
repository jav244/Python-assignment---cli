from cmd_view import CmdView
from controller import Controller
from data_visualiser import DataVis
from validator import Validator
from format import Format
from database import Database
from serialize import Pickle

if __name__ == '__main__':
    view = CmdView()
    validator = Validator()
    format = Format()
    pickle = Pickle()
    db = Database('company.db')

    con = Controller(view, validator, format, pickle, db)

    view.controller_set(con)

    view.cmdloop()

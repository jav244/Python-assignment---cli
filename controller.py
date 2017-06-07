from data_visualiser import *

# large class -- bad smell 3
class Controller:
    database_got_data = False

    def __init__(self, view, validator, format, pickle, db):
        self.view = view
        self.validator = validator
        self.format = format
        self.pickle = pickle
        self.db = db
        # self.db = db

    def file_reader(self, the_file):
        try:
            data = self.validator.validate(the_file, "file")
            for row in data:
                self.view.show_data(row)
        # not throwing any assertions yet, was going to add this functionality, didn't have time
        except AssertionError as e:  # pragma: no cover
            self.view.say(e)
        except Exception as e:
            self.view.say(e)

    # bad smell switch statement
    def display(self, flag):
        try:
            #self.data_vis.run_this(flag, self.db)

            if flag == "pie":
                DataVisualiser(BuildPieChart(self.db)).construct()
            elif flag == "bar":
                DataVisualiser(BuildBarChart(self.db)).construct()
            else:
                print("not a valid flag")
        except Exception as e:
            self.view.say(e)

    # unused function that i never took out, used to use it
    def database(self):  # pragma: no cover
        try:
            # if not self.database_set:
            self.db.create_table()
            # self.database_set = True
            # self.db.insert()
        except Exception as e:
            self.view.say(e)

    def database_insert(self, the_file):
        errors = []
        data = self.validator.validate(the_file, "db")
        for x in data:
            try:
                self.database_got_data = True
                self.db.insert(x)

            except Exception as e:
                errors.append((str(e) + " --- " + str(x.get("Empid"))))
                continue
        return errors

    # extract this serialization to another class
    def serialize(self, id, file):
        if id == "create":
            self.pickle.create_pickle(file, self)
        if id == "open":
            self.pickle.read_pickle(file)

    def database_query(self, input):
        try:
            if not self.database_got_data:
                self.view.say("there is no data in database")
            else:
                result = self.db.query(input)
                return result
        except Exception as e:
            print(e)

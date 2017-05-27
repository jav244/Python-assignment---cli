from cmd import Cmd


class CmdView(Cmd):
    """
    single command processor example
    """

    def __init__(self):
        Cmd.__init__(self)
        self.intro = "Type 'help' for available commands"
        self.prompt = ">>> "

    def controller_set(self, con):
        self.con = con

    def do_display(self, flag):
        """
        display either a piechart showing the 'gender ratio', or barchart showing the 'salary vs sales' of each employee

        :param flag: pie: shows piechart
                     bar: shows barchart
        """
        if flag:
            self.con.display(flag)

    def do_file(self, file):
        """
        input a file to display data in the file, and see what data is valid and invalid

        any invalid data drops the whole line

        can take input from txt or csv file

        :param file: input the file name following the command
                        e.g file data.txt
                        e.g file data.csv
        """
        if file:
            self.con.file_reader(file)
        else:
            self.say("please input a file name or type help for help")

    # def do_insert(self, input):
    #     self.con.insert(input)

    def say(self, input):
        print(input)

    def show_data(self, data):
        self.say(data)

    def do_quit(self, line):
        print("Quitting ......")
        return True

    def do_db(self, flag):
        """
        database interaction
        can insert from txt or csv files
        any rows with invalid data will drop the whole row
        use file command to find invalid data

        db[-flag]

        :param flag: -i: select a txt or csv file to insert into the database
                     -d: select fields to display from the database, seperate fields with a comma
                            e.g empid, age, gender

                            available fields to view are:
                            empid, gender, age, sales, bmi, salary, birthday
                            or type 'all' to view all fields
        """

        # self.con.database()

        if flag == "-d":
            query = input("Input field to display: ")
            if query == "all":
                query = "*"
            result = self.con.database_query(query)
            if result:
                for r in result:
                    self.say(r)
            return

        if flag == "-i":
            query = input("Input name of file to insert: ")
            f = self.con.database_insert(query)
            if f:
                for x in f:
                    self.say(x)
            return
        else:
            self.say("not a valid flag")

    def do_pickle(self, flag):
        """
        pickle[-flag]

        :param flag: -c: create a new pickle dataset
                     -o: open and view an existing pickle dataset
        """
        try:
            if flag == "-c":
                fname = input("Input a name to save dataset as: ")
                self.con.serialize("create", fname)
                return
            if flag == "-o":
                fname = input("input the dataset to open: ")
                self.con.serialize("open", fname)
                return
            else:
                self.say("not a valid flag")
        except Exception as e:
            self.say(e)

    def help_quit(self):
        print("\n".join(['Quit from my CMD', ':return: True']))

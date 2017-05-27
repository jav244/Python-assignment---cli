import pickle


class Pickle:
    def create_pickle(self, file, con):
        data = con.database_query("*")
        with open(file, 'wb') as f:
            pickle.dump(data, f)
        print("success: pickle saved as " + file)

    def read_pickle(self, file):
        with open(file, 'rb') as f:
            d = pickle.load(f)
        for row in d:
            print(row)

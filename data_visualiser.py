import pygal
from format import Format
from abc import ABCMeta, abstractmethod

# director
class DataVisualiser:

    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.get_data()
        self.builder.label_title()
        self.builder.label_axis()
        self.builder.input_data()
        self.builder.render()


class AbstractChartBuilder(metaclass=ABCMeta):
    def __init__(self):
        self.chart = None

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def label_title(self):
        pass

    @abstractmethod
    def label_axis(self):
        pass

    @abstractmethod
    def input_data(self):
        pass

    def render(self):
        self.chart.render_in_browser()


class BuildBarChart(AbstractChartBuilder):
    def __init__(self, database):
        self.chart = pygal.Bar()
        self.db = database

    def get_data(self):
        form = Format()

        salary = self.db.query("salary")
        sales = self.db.query("sales")
        empid = self.db.query("empid")

        self.salary = form.clean(salary)
        self.sales = form.clean(sales)
        self.empid = form.clean(empid)

    def label_title(self):
        self.chart.title = 'Sales vs Salary'
        self.chart.x_title = 'Employee ID\'s'
        self.chart.y_title = 'the Dollars'

    def label_axis(self):
        self.chart.x_labels = map(str, self.empid)

    def input_data(self):
        self.chart.add("salary", self.salary)
        self.chart.add("sales", self.sales)



class BuildPieChart(AbstractChartBuilder):
    def __init__(self, database):
        self.chart = pygal.Pie(inner_radius=.2)
        self.db = database

    def get_data(self):
        form = Format()

        male = self.db.count_query("gender", "M")
        female = self.db.count_query("gender", "F")

        self.male = form.clean(male)
        self.female = form.clean(female)

    def label_title(self):
        self.chart.title = 'Gender ratio'

    def label_axis(self):
        pass

    def input_data(self):
        self.chart.add('female', self.female)
        self.chart.add('male', self.male)




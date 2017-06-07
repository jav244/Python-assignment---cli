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

    @abstractmethod
    def render(self):
        pass


class BuildBarChart(AbstractChartBuilder):
    def __init__(self, database):
        self.bar_chart = pygal.Bar(x_title='Employee ID\'s', y_title='the Dollars')
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
        self.bar_chart.title='Sales vs Salary'

    def label_axis(self):
        self.bar_chart.x_labels = map(str, self.empid)

    def input_data(self):
        self.bar_chart.add("salary", self.salary)
        self.bar_chart.add("sales", self.sales)

    def render(self):
        self.bar_chart.render_in_browser()


class BuildPieChart(AbstractChartBuilder):
    def __init__(self, database):
        self.pie_chart = pygal.Pie(inner_radius=.2)
        self.db = database

    def get_data(self):
        form = Format()

        male = self.db.count_query("gender", "M")
        female = self.db.count_query("gender", "F")

        self.male = form.clean(male)
        self.female = form.clean(female)

    def label_title(self):
        self.pie_chart.title = 'Gender ratio'

    def label_axis(self):
        pass

    def input_data(self):
        self.pie_chart.add('female', self.female)
        self.pie_chart.add('male', self.male)

    def render(self):
        self.pie_chart.render_in_browser()



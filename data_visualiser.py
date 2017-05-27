import pygal


class DataVis:
    def __init__(self):
        pass

    # not a used function, left over for testing purposes
    def bar_chart(self, input, line_names):  # pragma: no cover
        self.bar_chart = pygal.Bar()
        self.bar_chart.x_labels = line_names[0]

        for i, line in enumerate(line_names):
            print(i)
            print(line)
            print(input)
            # self.bar_chart.add(line, [input[i], input[i]])
            # self.bar_chart.render_in_browser()

    def pie_gender(self, female, male):
        pie_chart = pygal.Pie(inner_radius=.2)
        pie_chart.title = 'Gender ratio'
        pie_chart.add('female', female)
        pie_chart.add('male', male)
        pie_chart.render_in_browser()

    def bar_salary(self, salary, sales, empid):
        bar_chart = pygal.Bar(title='Sales vs Salary', x_title='Employee ID\'s', y_title='the Dollars')
        bar_chart.x_labels = map(str, empid)
        bar_chart.add("salary", salary)
        bar_chart.add("sales", sales)
        bar_chart.render_in_browser()

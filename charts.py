from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class Chart(object):

    def __init__(self, data, frame, row, column, title, rotation=0):
        self.data = data
        self.frame = frame
        self.title = title
        self.row = row
        self.column = column
        self.rotation = rotation

    def plot_chart(self, x_label, y_label):
        # Style of chart
        plt.style.use('fivethirtyeight')

        # Set dimensions for graph
        fig = plt.figure(figsize=(12, 8), dpi=30)

        # plots the graph
        ax = fig.add_subplot(111)
        ax.plot(self.data)
        ax.set_title(self.title, color='red',  fontsize=22)
        ax.set_xlabel(x_label, color='red', fontsize=18)
        ax.set_ylabel(y_label, color='red', fontsize=18)
        plt.xticks(rotation=self.rotation)
        canvasbar = FigureCanvasTkAgg(fig, master=self.frame)
        fig.tight_layout()
        canvasbar.draw()
        canvasbar.get_tk_widget().grid(row=self.row, column=self.column)
        plt.draw()

    def pie_chart(self, legend_title):
        # Plots a pie Chart
        plt.style.use('fivethirtyeight')
        fig, ax = plt.subplots(figsize=(12, 8), dpi=30, subplot_kw=dict(aspect="equal"))

        data = self.data
        # chart_data = data.values
        # chart_names = data.index

        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return "{:.1f}%\n({:d} cases)".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))
        ax.legend(wedges, data.index, title=legend_title, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(self.title, color='red', fontsize=24)
        canvasbar = FigureCanvasTkAgg(fig, master=self.frame)
        plt.xticks(rotation=self.rotation)
        fig.tight_layout()
        canvasbar.draw()
        canvasbar.get_tk_widget().grid(row=self.row, column=self.column)
        plt.draw()

    def multi_plot(self,  x_label, y_label, legend):
        # Plots multi line chart

        # Plot Style
        plt.style.use('fivethirtyeight')
        fig = plt.figure(figsize=(12, 8), dpi=30)
        ax = fig.add_subplot(111)

        # takes data as a list format
        list_of_plots = self.data
        # Plots for number of data entered
        for i in list_of_plots:
            ax.plot(i)

        # Plot the data
        ax.set_xlabel(x_label, color='green', fontsize=18)
        ax.set_ylabel(y_label, color='green', fontsize=18)
        ax.set_title(self.title, color='red', fontsize=22)
        fig.tight_layout()
        ax.legend(legend)
        canvasbar = FigureCanvasTkAgg(fig, master=self.frame)
        canvasbar.draw()
        canvasbar.get_tk_widget().grid(row=self.row, column=self.column, pady=(0, 400))
        plt.draw()

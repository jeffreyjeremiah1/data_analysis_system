import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from police_data_module.stop_and_search import get_police_data
from covid_19_module.covid19_data_ica import get_covid_data
from charts import Chart

# Gets data from the police data file
police_data = get_police_data()

# Gets data from the covid data file
covid_data = get_covid_data()

LARGE_FONT = ("verdana", 12)


# Responsible for the homepage layout and navigation between pages


class HomePage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Analysis System")
        container = tk.Frame(self, bg="black")
        self.geometry("1400x950")
        # self.geometry("%dx%d" % (HomePage.winfo_screenwidth(self), HomePage.winfo_screenheight(self)))
        self.resizable(False, False)
        container.pack(side="top", fill="both", expand=False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super(StartPage, self).__init__()
        tk.Frame.__init__(self, parent, width=1080, height=750, bg="black")
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid_rowconfigure(0, weight=1)
        label.grid_columnconfigure(0, weight=1)

        self.backGroundImage = PhotoImage(file="images/background1.png")
        self.backGroundImageLabel = Label(self, image=self.backGroundImage)
        self.backGroundImageLabel.pack()

        self.canvas = Canvas(self, width=1080, height=700, bg="#181C4E")
        self.canvas.place(x=150, y=60)

        title = tk.Label(self, text="Welcome to the Homepage", font=("Bold", 40), bg="#181C4E", foreground='white')
        title.place(x=450, y=100)

        note1 = tk.Label(self, text="Click button for COVID-19 Confirmed Cases Module: ", font=("Arial", 18),
                         bg="#181C4E", foreground='white')
        note1.place(x=200, y=250)

        note2 = tk.Label(self, text="Click button for Stop and Search Module: ", font=("Arial", 18),
                         bg="#181C4E", foreground='white')
        note2.place(x=200, y=300)

        button1 = tk.Button(self, text="Covid-19 Cases", padx=2, pady=2, fg="#181C4E",
                            bg="white", font=("Arial", 14), command=lambda: controller.show_frame(PageOne))
        button1.place(x=650, y=250)

        button2 = tk.Button(self, text="Stop and Search", highlightbackground="white", padx=2, pady=2, fg="#181C4E",
                            bg="white", font=("Arial", 14), command=lambda: controller.show_frame(PageTwo))
        button2.place(x=650, y=300)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        main_container = tk.Canvas(self)
        frame = tk.Frame(main_container)
        vertical_scroll_bar = tk.Scrollbar(self)

        # frame for header
        header_frame = tk.Canvas(self, background='#051a1f')
        header_frame.pack(pady=5, padx=0)

        header = tk.Label(header_frame, background="#051a1f", fg='white', font=("Bold", 36), text="COVID-19 Confirmed "
                                                                                                  "Cases")
        header.grid(row=0, column=3, padx=(400, 470), pady=20)

        # Question 1  ##################################################################

        # Filters df by total number of cases each month
        total_monthly_cases = covid_data.Total_case.groupby(covid_data.Month, sort=False).sum()

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="1.  What are the total number of cases reported each month over from the start of reporting to "
                      "end ?").grid(row=0,
                                    column=0,
                                    sticky='W',
                                    padx=50,
                                    pady=(50, 10))

        # Plots chart for question 1
        chart_1 = Chart(row=1, column=0, data=total_monthly_cases, frame=frame,
                        title='Total Number of Cases Reported vs Month')
        chart_1.plot_chart(x_label='Month', y_label='Total Cases')

        # Question 2  ###################################################################

        # Select first and last day of september as a date range
        start_date = '2020-09-01'
        end_date = '2020-09-30'

        # Filter the DataFrame for the month of september
        df_september = covid_data[(covid_data['date'] >= start_date) & (covid_data['date'] <= end_date)]
        total_daily_cases_september = df_september.Total_case.groupby(df_september['date'], sort=False).sum()

        tk.Label(frame, font=("Bold", 22), wraplength='1000', justify=LEFT,
                 text="2. What are Total number of cases reported each day over a given date range ? ").grid(row=2,
                                                                                                             column=0,
                                                                                                             sticky='W',
                                                                                                             padx=50,
                                                                                                             pady=(
                                                                                                                 50,
                                                                                                                 10))
        # Plots chart for question 1
        chart_2 = Chart(row=3, column=0, data=total_daily_cases_september, frame=frame,
                        title='Daily cases for the month of september', rotation=90)
        chart_2.plot_chart(x_label='Date', y_label='Total Cases')

        # Question 3  #######################################################################

        # Chosen date
        date = '2020-04-01'

        # Filters the DataFrame to include only the rows that correspond to the given day.
        df_by_date = covid_data.query(f'date == "{date}"')

        # Groups the DataFrame by the area column and makes 'areaName' index.
        df_by_area = df_by_date.groupby(df_by_date['areaName']).count()

        # finds the top n areas with the highest number of cases
        top_areas = df_by_area.nlargest(5, 'Total_case')

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="3. What are the areas with the highest number of cases on a given day ?") \
            .grid(row=4, column=0, sticky='W', padx=50, pady=(50, 10))

        chart_3 = Chart(row=5, column=0, data=top_areas, frame=frame,
                        title=f"Top 5 Areas with the highest number of cases on {date}")
        chart_3.pie_chart(legend_title='Area Names')

        # Question 4  #####################################################################

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="4. Are there any comparison between two or more areas concerning their cumulative cases total "
                      "over a given date range ?").grid(row=6,
                                                        column=0,
                                                        sticky='W',
                                                        padx=50,
                                                        pady=(50, 10))

        def chart_4():
            # Select first and last day of september as a date range
            start_date = '2020-08-01'
            end_date = '2020-10-01'

            # Chosen areas to explore
            areas = ['North West', 'London', 'Yorkshire and The Humber']

            # Filter the DataFrame based on the date range
            df_date_range = covid_data[(covid_data['date'] >= start_date) & (covid_data['date'] <= end_date)]

            # Get the data for three different areas
            area1 = df_date_range[df_date_range['areaName'] == areas[0]]
            area2 = df_date_range[df_date_range['areaName'] == areas[1]]
            area3 = df_date_range[df_date_range['areaName'] == areas[2]]

            # Group each area by date and get the cumulative sum of total cases
            area1_cases = area1.groupby('date')['Total_case'].sum()
            area2_cases = area2.groupby('date')['Total_case'].sum()
            area3_cases = area3.groupby('date')['Total_case'].sum()

            # Plot Style
            plt.style.use('fivethirtyeight')

            fig = plt.figure(figsize=(11, 8), dpi=30)
            ax = fig.add_subplot(111)

            # Plot the data
            ax.plot(area1_cases, label=areas[0])
            ax.plot(area2_cases, label=areas[1])
            ax.plot(area3_cases, label=areas[2])
            ax.set_xlabel('Date', color='green', fontsize=18)
            ax.set_ylabel('Cumulative Cases Total', color='green', fontsize=18)
            ax.set_title(f'Cumulative Cases Total by Area from {start_date} to {end_date}', color='red', fontsize=22)
            # plt.xticks(rotation=45)
            # Add padding to the x-tick labels
            ax.xaxis.set_tick_params(pad=30)
            fig.tight_layout()
            ax.legend(areas)
            canvasbar = FigureCanvasTkAgg(fig, master=frame)
            canvasbar.draw()
            canvasbar.get_tk_widget().grid(row=7, column=0, padx=0, pady=(0, 400))
            plt.draw()

        # Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
        def update_scrolling_region():
            main_container.update_idletasks()
            main_container.config(scrollregion=frame.bbox())

        # Sets up the Canvas, Frame, and scrollbars for scrolling
        def create_scroll_bar_container():
            main_container.config(yscrollcommand=vertical_scroll_bar.set,
                                  highlightthickness=0)

            vertical_scroll_bar.config(orient=tk.VERTICAL, command=main_container.yview)
            vertical_scroll_bar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
            main_container.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
            main_container.create_window(0, 0, window=frame, anchor=tk.NW)

        chart_4()

        create_scroll_bar_container()
        update_scrolling_region()

        # Button takes user to home screen
        button1 = tk.Button(header_frame, text="Back to home", highlightbackground="white",
                            command=lambda: controller.show_frame(StartPage))

        # button takes user to first page
        button2 = tk.Button(header_frame, text="Page Two", background="#051a1f", highlightbackground="white",
                            justify="center", command=lambda: controller.show_frame(PageTwo))

        button1.grid(row=0, column=1, padx=6)
        button2.grid(row=0, column=2, padx=6)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        main_container = tk.Canvas(self)
        frame = tk.Frame(main_container)
        vertical_scroll_bar = tk.Scrollbar(self)

        # frame for header
        header_frame = tk.Canvas(self, background='#051a1f')
        header_frame.pack(pady=5, padx=0)

        # Navigates to the homepage
        button1 = tk.Button(header_frame, text="Back to home", bg="blue", highlightbackground="white",
                            command=lambda: controller.show_frame(StartPage))

        # Navigates to Page One
        button2 = tk.Button(header_frame, text="Page One", background="#051a1f", highlightbackground="white",
                            justify="center",
                            command=lambda: controller.show_frame(PageOne))

        button1.grid(row=0, column=1, padx=6)
        button2.grid(row=0, column=2, padx=6)

        header = tk.Label(header_frame, background="#051a1f", fg='white', font=("Bold", 36),
                          text="Police Stop and Search")
        header.grid(row=0, column=3, padx=(400, 470), pady=20)

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="1.  What are the top 5 age range with the most arrests ?").grid(row=0,
                                                                                       column=0,
                                                                                       sticky='W',
                                                                                       padx=50,
                                                                                       pady=(50, 10))

        def chart_1():
            # Group the data by age range and count the number of arrests
            age_arrests = police_data.groupby('age_range')['outcome'].agg(lambda x: x[x == 'Arrest'].count())

            # Sort the data in descending order by the count of arrests
            age_arrests = age_arrests.sort_values(ascending=False)

            # Select the top 5 age ranges
            top_5_age_ranges = age_arrests.head(5)

            #  Plots a pie Chart
            plt.style.use('fivethirtyeight')

            fig, ax = plt.subplots(figsize=(8, 6), dpi=30, subplot_kw=dict(aspect="equal"))

            age_range_values = top_5_age_ranges.values
            age_ranges = top_5_age_ranges.index

            def func(pct, allvals):
                absolute = int(np.round(pct / 100. * np.sum(allvals)))
                return "{:.1f}%\n({:d} Arrests)".format(pct, absolute)

            wedges, texts, autotexts = ax.pie(age_range_values, autopct=lambda pct: func(pct, age_range_values),
                                              textprops=dict(color="w"))
            ax.legend(wedges, age_ranges,
                      title="Age Ranges",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))

            plt.setp(autotexts, size=8, weight="bold")
            ax.set_title(f"Top 5 Age Ranges with highest Arrests", color='red', fontsize=24)
            canvasbar = FigureCanvasTkAgg(fig, master=frame)
            canvasbar.draw()
            fig.tight_layout()
            canvasbar.get_tk_widget().grid(row=1, column=0, padx=0)
            plt.draw()

        tk.Label(frame, font=("Bold", 22), wraplength='1000', justify=LEFT,
                 text="2. What are the top locations where interactions takes place ?").grid(row=2,
                                                                                             column=0,
                                                                                             sticky='W',
                                                                                             padx=50,
                                                                                             pady=(50, 10))

        def chart_2():
            # Group the data by location and count the number of interactions
            location_count = police_data.groupby('name').size().sort_values(ascending=False)
            top_10_locations = location_count.head(10)

            plt.style.use('fivethirtyeight')

            # Set dimensions for graph
            fig = plt.figure(figsize=(10, 8), dpi=30)

            # Create a bar chart to show the location count
            ax = fig.add_subplot(111)
            top_10_locations.plot(kind='bar', color='lightblue', edgecolor='black')

            # Add a title and labels to the chart
            ax.set_title('Top 10 Location names of interactions ', fontsize=22, color='red')
            ax.set_xlabel('Location ', color='red', fontsize=18)
            ax.set_ylabel('Interaction Count', color='red', fontsize=18)
            plt.xticks(rotation=90)
            # ax.xaxis.set_tick_params(pad=20)
            fig.tight_layout()
            canvasbar = FigureCanvasTkAgg(fig, master=frame)
            canvasbar.draw()
            canvasbar.get_tk_widget().grid(row=3, column=0, padx=0)
            plt.draw()

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="3. What are the top locations where interactions takes place ?").grid(row=4,
                                                                                             column=0,
                                                                                             sticky='W',
                                                                                             padx=50,
                                                                                             pady=(50, 10))

        def chart_3():
            # Group the data by ethnicity and outcome and count the number of interactions
            ethnicity_count = police_data.groupby(
                ['self_defined_ethnicity', 'officer_defined_ethnicity', 'outcome']).size().unstack()

            plt.style.use('fivethirtyeight')

            # set dimensions for figure
            fig = plt.figure(figsize=(10, 8), dpi=30)
            ax = fig.add_subplot(111)

            # Create a stacked bar chart to show the ethnicity count by outcome
            ethnicity_count.plot(kind='bar', ax=ax, stacked=False,
                                 color=['lightblue', 'crimson', 'lightgreen', 'darkorange', 'teal', 'indigo'],
                                 edgecolor='black')

            # Add a title and labels to the chart
            ax.set_title('Ethnicity Count by Outcome', color='red', fontsize=24)
            ax.set_xlabel('Ethnicity (self_defined_ethnicity, officer_defined_ethnicity)', color='red', fontsize=18)
            ax.set_ylabel('Count', color='red', fontsize=18)
            # Add a legend to the chart
            plt.legend(ethnicity_count, title='Outcome')
            plt.xticks(rotation=0)
            canvasbar = FigureCanvasTkAgg(fig, master=frame)
            canvasbar.draw()
            fig.tight_layout()
            canvasbar.get_tk_widget().grid(row=5, column=0, padx=0, pady=(0, 100))
            plt.draw()

        tk.Label(frame, font=("Bold", 22), wraplength='1300', justify=LEFT,
                 text="4. Are there any patterns in the legislation based on gender ?").grid(row=6,
                                                                                             column=0,
                                                                                             sticky='W',
                                                                                             padx=50,
                                                                                             pady=(50, 10))

        def chart_4():
            # filters data data based on legislation and gender
            legislation_count = police_data.groupby(['legislation', 'gender']).size().unstack()

            plt.style.use('fivethirtyeight')

            # set dimensions for figure
            fig = plt.figure(figsize=(10, 8), dpi=30)
            ax = fig.add_subplot(111)

            # Create a stacked bar chart to show the ethnicity count by outcome
            legislation_count.plot(kind='bar', figsize=(14, 8), ax=ax, stacked=False, color=['teal', 'crimson'],
                                   edgecolor='black')

            # Add a title and labels to the chart
            ax.set_title('Legislation Count Based on Gender', color='red', fontsize=24)
            ax.set_xlabel('Legislation ', color='red', fontsize=18)
            ax.set_ylabel('Count', color='red', fontsize=18)
            plt.xticks(rotation=0)

            # Add a legend to the chart
            plt.legend(legislation_count, title='Gender')
            canvasbar = FigureCanvasTkAgg(fig, master=frame)
            canvasbar.draw()
            fig.tight_layout()
            canvasbar.get_tk_widget().grid(row=7, column=0, padx=0, pady=(0, 400))
            plt.draw()

        # Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
        def update_scrolling_region():
            main_container.update_idletasks()
            main_container.config(scrollregion=frame.bbox())

        # Sets up the Canvas, Frame, and scrollbars for scrolling
        def create_scroll_bar_container():
            main_container.config(yscrollcommand=vertical_scroll_bar.set,
                                  highlightthickness=0)

            vertical_scroll_bar.config(orient=tk.VERTICAL, command=main_container.yview)
            vertical_scroll_bar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
            main_container.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
            main_container.create_window(0, 0, window=frame, anchor=tk.NW)

        chart_1()
        chart_2()
        chart_3()
        chart_4()
        create_scroll_bar_container()
        update_scrolling_region()


app = HomePage()
app.mainloop()

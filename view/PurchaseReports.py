from tkinter import *
from tkinter import messagebox
from controller import control


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.date_frame().grid(row=5, column=5, )
        self.button_frame().grid(row=10, column=5)


        self.pack(expand=False)

    def button_frame(self):
        frame = Frame(self)
        Button(frame, text="Run Report", command=self.run_report).pack(side=LEFT)
        Button(frame, text="Open Report", command=self.open_file).pack(side=LEFT)
        Button(frame, text="Delete Report", command=self.delete_report).pack(side=LEFT)
        return frame

    def delete_report(self):
        week = int(self.entry_week.get())
        year = int(self.entry_year.get())
        if not control.delete_report(year,week):
            messagebox.showinfo("Open File",
                                f"The Report is open!\nPlease Close Week {14} and click delete again")
        self.updateDateRange()

    def run_report(self):
        week = int(self.entry_week.get())
        year = int(self.entry_year.get())
        if not control.run_report(year, week):
            messagebox.showinfo("Open File", f"The Report is already open!\nPlease Close Week {14} and click run report again")
        self.updateDateRange()

    def open_file(self):
        week = int(self.entry_week.get())
        year = int(self.entry_year.get())
        control.open_file(year, week)

    def date_frame(self):
        frame = Frame(self, width=500)
        '''
        self.cur_year = StringVar()
        self.cur_year.set(control.get_current_year_week()['year'])
        self.cur_week = StringVar()
        self.cur_week.set(control.get_current_year_week()['week'])
        '''

        Label(frame, text="Year:").grid(row=1, column=1)
        Label(frame, text="Week:").grid(row=2, column=1)
        self.var_year = StringVar()
        self.var_week = StringVar()
        self.var_year.set(control.get_current_year_week()['year'])
        self.var_week.set(control.get_current_year_week()['week'] + 1)


        self.entry_week = Entry(frame, textvariable=self.var_week)
        self.entry_year = Entry(frame, textvariable=self.var_year)
        self.var_year.trace_add('write', self.updateDateRange)
        self.var_week.trace_add('write', self.updateDateRange)

        self.entry_year.grid(row=1, column=2, sticky="EW")
        self.entry_week.grid(row=2, column=2, sticky="EW")
        self.from_date = StringVar()
        self.to_date = StringVar()
        self.report_exists = StringVar()
        Label(frame, anchor="e", textvariable=self.from_date).grid(row=1, column=3)
        Label(frame, anchor="e", textvariable=self.to_date).grid(row=2, column=3)

        Label(frame, anchor="w", textvariable=self.report_exists, width=35).grid(row=4, column=2)

        self.updateDateRange()

        return frame

    def updateDateRange(self, *args):


        try:
            year = int(self.entry_year.get())
            week = int(self.entry_week.get())
            dates = control.get_week_dates(year, week)
            self.from_date.set(f"From: {dates['sunday']}")
            self.to_date.set(f"To:   {dates['saturday']}")
            self.report_exists.set(control.last_modified(year,week))

        except:
            self.report_exists.set("Dates are invalid")

    def callback(self):
        print("called")
root = Tk()
app = Window(root)
app.master.title("Run Reports")
root.mainloop()

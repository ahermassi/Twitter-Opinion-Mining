from tkinter.constants import CENTER, DISABLED, NORMAL
import tkinter as tk
import glob
import os
from tkinter.font import Font
from scraping import getTweets
from clean import pre_process
from analyse import classify, result_plot

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (CollectionPage, AnalysisPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(CollectionPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class CollectionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        L1 = tk.Label(self, text="Trends Discovery in Twitter", fg="#0080ff")
        L1.config(font=Font(family="Helvetica", size=22, weight="bold"))
        L1.place(x=160, y=55)

        L2 = tk.Label(self, text="Enter hashtags below:", fg="#000")
        L2.config(font=Font(family="Arial", size=16))
        L2.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.h1 = tk.Entry(self)
        self.h2 = tk.Entry(self)
        self.h3 = tk.Entry(self)
        self.h4 = tk.Entry(self)
        self.info = tk.Label(width=30, height=2)

        self.extractButton = tk.Button(self, text="Collect", width=5, command=self.extract)
        self.cleanButton = tk.Button(self, text="Clean", state=DISABLED, command=self.clean)
        self.nextButton = tk.Button(self, text="Next", width=5, state=DISABLED,
                                    command=lambda: controller.show_frame(AnalysisPage))

        self.h1.place(relx=0.2, rely=0.45, relwidth=0.2, anchor=CENTER)
        self.h2.place(relx=0.4, rely=0.45, relwidth=0.2, anchor=CENTER)
        self.h3.place(relx=0.6, rely=0.45, relwidth=0.2, anchor=CENTER)
        self.h4.place(relx=0.8, rely=0.45, relwidth=0.2, anchor=CENTER)
        self.info.place(x=170, y=400)
        self.extractButton.place(x=220, y=300)
        self.cleanButton.place(x=320, y=300)
        self.nextButton.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.info.place(x=150, y=350)
        self.info.config(text="Test")

    def extract(self):
        if not self.h1.get() and not self.h2.get() and not self.h3.get() and not self.h4.get():
            self.info.config(text="Hashtags list is empty!")
        else:
            hashtags = [eval("self.h" + str(i)).get() for i in range(1, 5)]
            hashtags = [s for s in hashtags if s]
            print(hashtags)
            getTweets(hashtags, self.info)
            self.extractButton.config(state=DISABLED)
            self.cleanButton.config(state=NORMAL)

    def clean(self):
        hashtags = [eval("self.h" + str(i)).get() for i in range(1, 5)]
        hashtags = [s for s in hashtags if s]
        file_list = ['../gen/' + filename + '.csv' for filename in hashtags]
        # print file_list
        pre_process(file_list, self.info)
        self.cleanButton.config(state=DISABLED)
        self.nextButton.config(state=NORMAL)


class AnalysisPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        L1 = tk.Label(self, text="Trends Discovery in Twitter", fg="#0080ff")
        L1.config(font=Font(family="Helvetica", size=22, weight="bold"))
        L1.place(x=160, y=55)
        L3 = tk.Label(self, text="Choose the classification algorithm:", fg="#000")
        L3.config(font=Font(family="Arial", size=16))
        L3.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.CheckVar = tk.IntVar()
        self.C1 = tk.Radiobutton(self, text="Naive Bayes", variable=self.CheckVar, value=0)
        self.C2 = tk.Radiobutton(self, text="SVM", variable=self.CheckVar, value=1)

        back = tk.Button(self, text="Back", width=5, command=lambda: controller.show_frame(CollectionPage))
        analyse = tk.Button(self, text="Analyse", command=self.analyse)

        self.C1.place(x=170, rely=0.5, anchor=CENTER)
        self.C2.place(x=440, rely=0.5, anchor=CENTER)

        back.place(x=220, y=300)
        analyse.place(x=320, y=300)

    def analyse(self):
        val = self.CheckVar.get()
        os.chdir("../gen")
        for f in glob.glob("*.csv"):
            classify(f, val)
        result_plot()


class MainButtonFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Pages = [CollectionPage, AnalysisPage]
        for button in Pages:
            NewButton = tk.Button(self, text=str(button), command=lambda: controller.show_frame(button))
            NewButton.pack()


if __name__ == '__main__':
    app = SeaofBTCapp()
    app.geometry("600x488")
    app.resizable(width=False, height=False)
    app.mainloop()

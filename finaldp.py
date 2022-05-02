import time
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


global le

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

le = LabelEncoder()
root = tk.Tk()
root.attributes('-fullscreen', True)

root.title("data preprocessing")
root.config(bg="LIGHT BLUE")

style = ttk.Style()
style.theme_use('clam')

# Create a Frame
frame = Frame(root)
frame.pack(pady=20, side=BOTTOM)


# Define a function for opening the file
def open_file():
    filename = sg.popup_get_file('Dataset to read', title="Open a File",
                                 file_types=(("CSV Files", "*.csv"), ("Text Files", "*.txt")))


# Clear the Treeview Widget
def clear_treeview():
    tree.delete(*tree.get_children())


# Create a Treeview widget
tree = ttk.Treeview(frame)

# Add a Menu
m = Menu(root)
root.config(menu=m)

# Add a Label widget to display the file content
label = Label(root, text='')
label.pack(pady=20)
canvas = Canvas(width=1000, height=800, bg='light green')
canvas.pack(fill=BOTH)
image = ImageTk.PhotoImage(file=r"C:\Users\sanka\Desktop\projects\old\dp\10962973.jpg")
canvas.create_image(0, 0, image=image, anchor=NW)
canvas.create_image(987, 0, image=image, anchor=NW)


def print_answers():
    global sel_optx
    global sel_opty
    sel_optx = clickedx.get()
    sel_opty = clickedy.get()


def read():
    global df
    sg.set_options(auto_size_buttons=True)
    filename = sg.popup_get_file(
        'Dataset to read',
        title='Dataset to read',
        no_window=True,
        file_types=(("CSV Files", "*.csv"), ("Text Files", "*.txt")))

    l5 = ttk.Label(root, text=filename)
    l5.place(x=620, y=130)
    # --- populate table with file contents --- #
    if filename == '':
        return
    df = pd.read_csv(filename, sep=',', engine='python')
    list_of_column_names = list(df.columns)

    options = list(df.columns)
    global clickedx
    global clickedy
    clickedx = tk.StringVar(root)
    clickedy = tk.StringVar(root)
    drop = tk.OptionMenu(root, clickedx, *options)
    drop1 = tk.OptionMenu(root, clickedy, *options)
    drop.pack()
    drop1.pack()
    drop.place(x=220, y=200)
    drop1.place(x=220, y=230)
    drop.config(bg="ORANGE", fg="BLACK")
    drop1.config(bg="ORANGE", fg="BLACK")
    drop["menu"].config(bg="yellow")
    drop1["menu"].config(bg="yellow")

    l8 = ttk.Label(root, text='select the attribute for x axis')
    l8.place(x=50, y=200)
    l7 = ttk.Label(root, text='select the attribute for y axis')
    l7.place(x=50, y=230)

    print(clickedx.get())
    print(clickedy.get())
    submit_button = tk.Button(root, text='Submit', command=print_answers)
    submit_button.pack()
    submit_button.place(x=300, y=280)

    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_csv(filename)
        except ValueError:
            label.config(text="File could not be opened")
        except FileNotFoundError:
            label.config(text="File Not Found")

    # Clear all the previous data in tree
    clear_treeview()

    # Add new data in Treeview widget
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)
        tree.column(col, minwidth=0, width=110, stretch=NO)

    # Put Data in Rows
    df_rows = df.to_numpy().tolist()

    for row in df_rows:
        tree.insert("", "end", values=row)
        tree.pack()


# Add Menu Dropdown
file_menu = Menu(m, tearoff=False)
m.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Open Spreadsheet", command=read)


def show_stats():
    stats = df.describe().T
    header_list = list(stats.columns)
    data = stats.values.tolist()
    for i, d in enumerate(data):
        d.insert(0, list(stats.index)[i])
    header_list = ['Feature'] + header_list
    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  font='Helvetica',
                  pad=(10, 10),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))]
    ]

    window = sg.Window("Statistics", layout, grab_anywhere=False)
    event, values = window.read()
    window.close()


def bar():
    plt.bar(x=df[sel_optx], height=df[sel_opty])
    plt.show()


def histo(sel_optx):
    histo_data = df[sel_optx]
    plt.hist(histo_data, 50)
    plt.show()


def scatter():
    scatter_data = df[[sel_optx, sel_opty]]
    df.plot.scatter(x=sel_optx, y=sel_opty, s=100);
    plt.show()


def missing():
    self = tk.Tk()
    self.geometry("250x350")
    main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
    # pack_propagate prevents the window resizing to match the widgets
    main_frame.pack_propagate(0)
    main_frame.pack(fill="both", expand="true")
    self.title("missing value percentage")

    global null
    null = df.isnull().mean()

    global l5
    l5 = ttk.Label(main_frame, text=null)
    l5.place(x=10, y=10)


def label_encoding():
    root1 = tk.Tk()
    root1.geometry("900x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=BOTTOM)
    tree1 = ttk.Treeview(frame1)

    df1 = df
    le.fit(df1['Country'])
    df['Country'] = le.transform(df1['Country'])

    # Add new data in Treeview widget
    tree1["column"] = list(df1.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=60, stretch=NO)

    # Put Data in Rows
    df1_rows = df1.to_numpy().tolist()

    for row in df1_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


# frequency encoding
def frequency_enconding():
    root1 = tk.Tk()
    root1.geometry("900x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=BOTTOM)
    tree1 = ttk.Treeview(frame1)

    df2 = df
    df2.dropna(inplace=True)
    value_counts = df2['Status'].value_counts().to_dict()
    df2['Status_fd'] = df2['Status'].map(value_counts)

    tree1["column"] = list(df2.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=60, stretch=NO)

    # Put Data in Rows
    df2_rows = df2.to_numpy().tolist()

    for row in df2_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


def one_hot_encoding():
    root1 = tk.Tk()
    root1.geometry("900x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=BOTTOM)
    tree1 = ttk.Treeview(frame1)

    df2 = pd.concat([df["Status"], pd.get_dummies(df["Status"])], axis=1)
    # print(pd.concat([df["Status"], pd.get_dummies(df["Status"])], axis=1))

    tree1["column"] = list(df2.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=60, stretch=NO)

    # Put Data in Rows
    df2_rows = df2.to_numpy().tolist()

    for row in df2_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


# ordinal enconding
def ordinal_encoding():
    root1 = tk.Tk()
    root1.geometry("900x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=BOTTOM)
    tree1 = ttk.Treeview(frame1)

    df3 = df[['Status', 'Country']]
    ordered_cats = df3.groupby(['Status'])['thinness_1-19_years'].mean().sort_values().index
    cat_map = {k: i for i, k in enumerate(ordered_cats, 0)}  # Dictionary creation:
    df3['Country_ordered'] = df3['Country'].map(cat_map)

    tree1["column"] = list(df3.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=60, stretch=NO)

    # Put Data in Rows
    df3_rows = df3.to_numpy().tolist()

    for row in df3_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


def mean_encoding():
    root1 = tk.Tk()
    root1.geometry("1300x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=BOTTOM)
    tree1 = ttk.Treeview(frame1)

    df4 = df
    mean_labels = df.groupby(['Country'])['thinness_1-19_years'].mean().to_dict()
    df['Country_mean'] = df['Country'].map(mean_labels)

    tree1["column"] = list(df4.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=90, stretch=NO)

    # Put Data in Rows
    df4_rows = df4.to_numpy().tolist()

    for row in df4_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


def discretization():
    root1 = tk.Tk()
    root1.geometry("1390x200")
    root1.title("missing value percentage")
    side_frame = tk.Frame(root1, bg="#3F6BAA")
    side_frame.pack_propagate(0)
    side_frame.pack(fill="both", expand="true")

    frame1 = Frame(root1)
    frame1.pack(pady=2, side=TOP)
    tree1 = ttk.Treeview(frame1)

    df5 = df
    GDP_range = df5['GDP'].max() - df5['GDP'].min()
    GDP_range / 10
    lower_interval = int(np.floor(df5['GDP'].min()))
    upper_interval = int(np.ceil(df5['GDP'].max()))
    interval_length = int(np.round(GDP_range / 10))
    total_bins = [i for i in range(lower_interval, upper_interval + interval_length, interval_length)]
    bin_labels = ['Bin_no _' + str(i) for i in range(1, len(total_bins))]
    df5['GDP_bins'] = pd.cut(x=df5['GDP'], bins=total_bins, labels=bin_labels, include_lowest=True)

    tree1["column"] = list(df5.columns)
    tree1["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree1["column"]:
        tree1.heading(col, text=col)
        tree1.column(col, minwidth=0, width=90, stretch=NO)

    # Put Data in Rows
    df_rows = df.to_numpy().tolist()

    for row in df_rows:
        tree1.insert("", "end", values=row)
        tree1.pack()


def feat():
    sns.set(style="white")

    # Generate a large random dataset

    d = df

    # Compute the correlation matrix
    corr = d.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    return f


def new():
    root = tk.Tk()
    root.wm_title("Embedding in Tk")

    label = tk.Label(root, text="Matplotlib with Seaborn in Tkinter")
    label.pack()

    fig = feat()

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()

    button = tk.Button(root, text="Quit", command=root.destroy)

    button.pack()


def replace():
    opt = ["replace by mean", "replace by median", "replace by mode "]
    global r
    r = tk.StringVar(root)
    drop = tk.OptionMenu(root, r, *opt)
    drop.pack()
    drop.place(x=1150, y=180)
    drop.config(bg="ORANGE", fg="BLACK")
    drop["menu"].config(bg="yellow")

    l9 = ttk.Label(root, text='select the type of replacing')
    l9.place(x=1280, y=150)
    print(r.get())
    submit_button4 = tk.Button(root, text='Submit')
    submit_button4.pack()
    submit_button4.place(x=1240, y=180)


def drop():
    global df1
    df1 = df.dropna()
    x= df1.info()
    clear_treeview()

    self = tk.Tk()
    self.geometry("250x350")

    main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
    # pack_propagate prevents the window resizing to match the widgets
    main_frame.pack_propagate(0)
    main_frame.pack(fill="both", expand="true")
    self.title("missing value percentage")

    asa = df1.isnull().mean()
    global l15
    l15 = ttk.Label(main_frame, text=asa)
    l15.place(x=10, y=10)
    l16 = ttk.Label(main_frame, text=x)
    l16.place(x=20, y=0)

    # Add new data in Treeview widget
    tree["column"] = list(df1.columns)
    tree["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)
        tree.column(col, minwidth=0, width=60, stretch=NO)

    # Put Data in Rows
    df1_rows = df1.to_numpy().tolist()

    for row in df1_rows:
        tree.insert("", "end", values=row)
        tree.pack()


## button for making histogram
histo_button = Button(root, text="histogram", command=lambda: histo(sel_optx))
histo_button.pack()
scatter_button = Button(root, text="scatter plot", command=scatter)
scatter_button.pack()
bar_btn = Button(root, text='bar graph', command=bar)
bar_btn.pack()

ONE_HOT_ENCODING = Button(root, text="one hot encoding", command=one_hot_encoding)
ONE_HOT_ENCODING.pack()
LABEL_ENCODING = Button(root, text="label encoding", command=label_encoding)
LABEL_ENCODING.pack()
FREQUENCY_ENCODING = Button(root, text="frequency encoding", command=frequency_enconding)
FREQUENCY_ENCODING.pack()
ORDINAL_ENCODING = Button(root, text="ordinal encoding", command=ordinal_encoding)
ORDINAL_ENCODING.pack()
MEAN_ENCODING = Button(root, text="mean encoding", command=mean_encoding)
MEAN_ENCODING.pack()

discretization = Button(root, text="DISCRETIZATION", command=discretization)
discretization.pack()
feature = Button(root, text="FEATURE SELECTION", command=new)
feature.pack()

l1 = tk.Label(root, text='DATA PRE-PROCESSING PROJECT', font=("Arial", 25), bg="skyblue")
l8 = tk.Label(root, text='MADE BY - SANKALP VARMA & SANDESH KR. CHANDRAKAR', font=("Arial", 10), bg="skyblue")

l2 = tk.Label(root, text='enter address of data ', font=("Arial", 12))


# b2 = ttk.Button(root, text='show', width=20, command=display())
b1 = tk.Button(root, text='browse and show', width=20, command=read)
b4 = tk.Button(root, text='%age of missing attribues ', width=20, command=missing)
b5 = tk.Button(root, text='drop ', width=20, command=drop)
b6 = tk.Button(root, text='replace ', width=20, command=replace)

b7 = tk.Button(root, text='statistics', width=20, command=show_stats)

close_btn = tk.Button(root, text="Close", command=root.destroy, bg="red")
close_btn.pack()
close_btn.place(x=1480, y=0)
l2.place(x=720, y=70)
b1.place(x=718, y=100)

histo_button.place(x=100, y=350, height=50, width=110)
scatter_button.place(x=220, y=350, height=50, width=110)
bar_btn.place(x=165, y=420, height=50, width=110)

ONE_HOT_ENCODING.place(x=600, y=270, height=50, width=130)
LABEL_ENCODING.place(x=800, y=270, height=50, width=130)
FREQUENCY_ENCODING.place(x=600, y=330, height=50, width=130)
ORDINAL_ENCODING.place(x=800, y=330, height=50, width=130)
MEAN_ENCODING.place(x=700, y=390, height=50, width=130)

discretization.place(x=1170, y=270, height=40, width=130)
feature.place(x=1170, y=320, height=40, width=130)


# color on the btn's
def on_enter(e):
    ONE_HOT_ENCODING['background'] = 'orange'


def on_leave(e):
    ONE_HOT_ENCODING['background'] = 'SystemButtonFace'


ONE_HOT_ENCODING.bind("<Enter>", on_enter)
ONE_HOT_ENCODING.bind("<Leave>", on_leave)


def on_enter(e):
    discretization['background'] = 'orange'


def on_leave(e):
    discretization['background'] = 'SystemButtonFace'


discretization.bind("<Enter>", on_enter)
discretization.bind("<Leave>", on_leave)


def on_enter(e):
    feature['background'] = 'orange'


def on_leave(e):
    feature['background'] = 'SystemButtonFace'


feature.bind("<Enter>", on_enter)
feature.bind("<Leave>", on_leave)


def on_enter(e):
    FREQUENCY_ENCODING['background'] = 'orange'


def on_leave(e):
    FREQUENCY_ENCODING['background'] = 'SystemButtonFace'


FREQUENCY_ENCODING.bind("<Enter>", on_enter)
FREQUENCY_ENCODING.bind("<Leave>", on_leave)


def on_enter(e):
    MEAN_ENCODING['background'] = 'orange'


def on_leave(e):
    MEAN_ENCODING['background'] = 'SystemButtonFace'


MEAN_ENCODING.bind("<Enter>", on_enter)
MEAN_ENCODING.bind("<Leave>", on_leave)


def on_enter(e):
    LABEL_ENCODING['background'] = 'orange'


def on_leave(e):
    LABEL_ENCODING['background'] = 'SystemButtonFace'


LABEL_ENCODING.bind("<Enter>", on_enter)
LABEL_ENCODING.bind("<Leave>", on_leave)


def on_enter(e):
    ORDINAL_ENCODING['background'] = 'orange'


def on_leave(e):
    ORDINAL_ENCODING['background'] = 'SystemButtonFace'


ORDINAL_ENCODING.bind("<Enter>", on_enter)
ORDINAL_ENCODING.bind("<Leave>", on_leave)


def on_enter(e):
    histo_button['background'] = 'orange'


def on_leave(e):
    histo_button['background'] = 'SystemButtonFace'


histo_button.bind("<Enter>", on_enter)
histo_button.bind("<Leave>", on_leave)


def on_enter(e):
    bar_btn['background'] = 'orange'


def on_leave(e):
    bar_btn['background'] = 'SystemButtonFace'


bar_btn.bind("<Enter>", on_enter)
bar_btn.bind("<Leave>", on_leave)


def on_enter(e):
    scatter_button['background'] = 'orange'


def on_leave(e):
    scatter_button['background'] = 'SystemButtonFace'


scatter_button.bind("<Enter>", on_enter)
scatter_button.bind("<Leave>", on_leave)


# show stats coloring buton b7
def on_enter(e):
    b7['background'] = 'blue'


def on_leave(e):
    b7['background'] = 'SystemButtonFace'


b7.bind("<Enter>", on_enter)
b7.bind("<Leave>", on_leave)


###coloring replace btn b6
def on_enter(e):
    b6['background'] = 'blue'


def on_leave(e):
    b6['background'] = 'SystemButtonFace'


b6.bind("<Enter>", on_enter)
b6.bind("<Leave>", on_leave)


# b4,b5
def on_enter(e):
    b4['background'] = 'blue'


def on_leave(e):
    b4['background'] = 'SystemButtonFace'


b4.bind("<Enter>", on_enter)
b4.bind("<Leave>", on_leave)


def on_enter(e):
    b5['background'] = 'blue'


def on_leave(e):
    b5['background'] = 'SystemButtonFace'


b5.bind("<Enter>", on_enter)
b5.bind("<Leave>", on_leave)

l1.place(x=470, y=10)
l8.place(x=10, y=10)
b4.place(x=180, y=150)

b5.place(x=690, y=150)
b6.place(x=1100, y=150)
b7.place(x=700, y=220)

root.mainloop()
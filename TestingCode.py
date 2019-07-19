import tkinter as tk


def dosomething():
    print(e1.get())

root = tk.Tk()

tk.Label(root, text="filename").grid(row=0)

e1 = tk.Entry(root)
e1.grid(row=0, column=1)

tk.Button(root, text="okay", command=dosomething()).grid(row=3,
                                                         column=1,
                                                         sticky=tk.W,
                                                         pady=4)


tk.mainloop()
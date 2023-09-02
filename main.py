import tkinter as tk
import pandas
import random


MAIN_DICT = "turkish_english_300.csv"
LANGUAGE_1 = 'Turkish'
LANGUAGE_2 = 'English'
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"


try:
    with open("data/to_learn.csv") as to_learn_file:
        data = pandas.read_csv(to_learn_file)
except FileNotFoundError:
    original_data = pandas.read_csv(f"data/{MAIN_DICT}")
    to_learn_list = original_data.to_dict(orient="records")
else:
    to_learn_list = data.to_dict(orient="records")

try:
    with open("data/learnt.csv") as learnt_file:
        data = pandas.read_csv(learnt_file)
except FileNotFoundError:
    learnt_list = []
    print(learnt_list)
else:
    learnt_list = data.to_dict(orient="records")
    print(len(learnt_list))


"""Functions--------------------------------------------------------------------------------------------------------"""


def wrong():
    show_new_word()


def right():
    global learnt_list
    global to_learn_list
    learnt_list.append(to_learn_list.pop(current_word_num))
    my_to_learn_data = pandas.DataFrame(to_learn_list)
    my_to_learn_data.to_csv("data/to_learn.csv", index=False)
    my_learnt_data = pandas.DataFrame(learnt_list)
    my_learnt_data.to_csv("data/learnt.csv", index=False)
    show_new_word()


def show_new_word():
    global current_word_num, flip_timer
    win.after_cancel(flip_timer)

    current_word_num = random.randint(0, len(to_learn_list) - 1)

    c1.itemconfig(card_image, image=card_front_img)
    c1.itemconfig(card_title, text=LANGUAGE_1, fill="black")
    c1.itemconfig(card_word, text=f"{to_learn_list[current_word_num][LANGUAGE_1]}", fill="black")
    flip_timer = win.after(3000, func=show_meaning)


def show_meaning():
    c1.itemconfig(card_image, image=card_back_img)
    c1.itemconfig(card_title, text=LANGUAGE_2, fill="white")
    c1.itemconfig(card_word, text=f"{to_learn_list[current_word_num][LANGUAGE_2]}", fill="white")


def start():
    show_new_word()
    b1.config(command=wrong)
    b2.config(command=right)
    b3.config(text="", command=stop)


def stop():
    pass


"""main-------------------------------------------------------------------------------------------------------------"""


current_word_num = 0


"""UI---------------------------------------------------------------------------------------------------------------"""


win = tk.Tk()
win.title("Flashy")
win.config(bg=BACKGROUND_COLOR, padx=40, pady=30)
flip_timer = win.after(3000, func=show_meaning)
win.after_cancel(flip_timer)

c1 = tk.Canvas(win, width=500, height=329, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back_img = tk.PhotoImage(file="images/card_back.png")
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_image = c1.create_image(250, 165, image=card_front_img)
card_title = c1.create_text(240, 80, text="Language", fill="black", font=(FONT_NAME, 18, "italic"), tags="text")
card_word = c1.create_text(240, 160, text="Word", fill="black", font=(FONT_NAME, 42, "bold"), tags="text")
c1.grid(column=1, row=1, columnspan=5)

wrong_img = tk.PhotoImage(file="images/wrong.png")
b1 = tk.Button(win, image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, command=stop)
b1.grid(column=2, row=2, pady=10)

right_img = tk.PhotoImage(file="images/right.png")
b2 = tk.Button(win, image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, command=stop)
b2.grid(column=4, row=2, pady=10)

b3 = tk.Button(win, text="Start", bg=BACKGROUND_COLOR, font=("ariel", 10, "bold"), highlightthickness=0, activebackground=BACKGROUND_COLOR, activeforeground="white", borderwidth=0, command=start)
b3.grid(column=3, row=3)


win.mainloop()

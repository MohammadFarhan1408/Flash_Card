from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
TIME_DELAY = 3000
current_word = {}
words_df = {}


# Change Word
def next_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(words_df)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_word["French"], fill="black")
    flip_timer = window.after(TIME_DELAY, flip_card)


# Remove Word
def remove_word():
    words_df.remove(current_word)
    data = pd.DataFrame(words_df)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def flip_card():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill='white')
    canvas.itemconfig(word_text, text=current_word["English"], fill="white")


# Window
window = Tk()
window.title("Flash Card")
window.config(pady=15, padx=35, bg=BACKGROUND_COLOR)

# Data
try:
    words_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    main_data = pd.read_csv("data/french_words.csv")
    words_df = main_data.to_dict(orient="records")
else:
    words_df = words_data.to_dict(orient="records")

flip_timer = window.after(TIME_DELAY, flip_card)

# Card Image Canvas
canvas = Canvas(width=800, height=526)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

# Right Button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0, command=next_word)
wrong_button.grid(column=0, row=1)

# Right Button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, border=0, command=remove_word)
right_button.grid(column=1, row=1)

next_word()

window.mainloop()

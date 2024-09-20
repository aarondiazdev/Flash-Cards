from tkinter import Tk, Button,PhotoImage, Canvas, Label
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
data = pd.read_csv("data/English_words.csv")
to_learn = data.to_dict(orient="records")
current_card = []

def next_card(status_="n"):   
  global current_card, flip_timer, learned, data, to_learn
  window.after_cancel(flip_timer)
  try:
    if status_ == "y" and len(to_learn) > 0:
      df = pd.read_csv("data/English_words.csv")
      df = df[(df["English"] != current_card["English"]) & (df["Spanish"] != current_card["Spanish"])]
      df.to_csv("data/English_words.csv", index=False)
      data = pd.read_csv("data/English_words.csv")
      to_learn = data.to_dict(orient="records")
    current_card = choice(to_learn)
    card_font.itemconfig(languaje, text="English", fill="black")
    card_font.itemconfig(word, text=current_card["English"], fill="black")  
    card_font.itemconfig(card_img, image=card_img_old) 
    flip_timer = window.after(3000, func=flip_card)
  except IndexError:
    card_font.itemconfig(card_img, image=card_img_old)
    card_font.itemconfig(languaje, text="English", fill="black")
    card_font.itemconfig(word, text="You have learned all cards", fill="black", font=("Ariel", 40, "bold"))
    warning_no_cards()

def flip_card():
  global current_card
  card_font.itemconfig(languaje, text="Spanish", fill="white")
  card_font.itemconfig(word, text=current_card["Spanish"], fill="white")
  card_font.itemconfig(card_img, image=card_img_new)
  
def warning_no_cards():
  if len(to_learn) == 0:
    warning_label = Label(text="No more cards", font=("Ariel", 20, "bold"), bg=BACKGROUND_COLOR, fg="red")
    warning_label.grid(row=2, column=0, columnspan=2)

window = Tk()
window.title("Flash Cards By Aaron Diaz")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
if len(to_learn) <= 0:
  warning_no_cards()
flip_timer = window.after(3000, func=flip_card) 
card_font = Canvas(width=800, height=527)
card_img_new = PhotoImage(file="images/card_back.png")
card_img_old = PhotoImage(file="images/card_front.png")
card_img = card_font.create_image(400, 263, image=card_img_old)
languaje = card_font.create_text(400, 150, text="Languaje", font=("Ariel", 40, "italic"))
word = card_font.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
card_font.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_font.grid(row=0, column=0, columnspan=2)

x = PhotoImage(file="images/wrong.png")
x_button = Button(image=x, borderwidth=0, highlightthickness=0, relief="flat", highlightbackground=BACKGROUND_COLOR, command=next_card)
x_button.grid(row=1, column=0)

y = PhotoImage(file="images/right.png")
y_button = Button(image=y, borderwidth=0, highlightthickness=0, relief="flat", highlightbackground=BACKGROUND_COLOR, command=lambda:next_card("y"))
y_button.grid(row=1, column=1)

next_card()

window.mainloop()
  

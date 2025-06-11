import os
import random
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import pandas
from tkinter import messagebox
import pyperclip
from numpy import delete

passwords = pandas.DataFrame(columns= ["Website", "Email/Username", "Password"])
passwords_file = open("passwords_file_ex.txt", mode= "a")
flash = None

#returns a randomly generated password
def generate_password():
    global flash

    #keeps the 'copied to clipboard' message working correctly if the user spams it
    if flash is not None:
        window.after_cancel(flash)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, tkinter.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    flash_copy_message()

def flash_copy_message():
    copied_label.grid(row=6, column= 2, sticky= "s", pady= 5)
    global flash
    flash = copied_label.after(2000, func= copied_label.grid_forget)

#Saves passwords to a pandas dataframe which will be printed to a file later
def save(event=None):
    website = website_entry.get()
    password = password_entry.get()
    username = email_entry.get()

    if website.strip() == "" or password.strip() == "" or username.strip() == "":
        messagebox.showwarning(title= "Error", message= "Please do not leave any fields blank.")
        return

    can_save = messagebox.askokcancel(title= website, message= f"Are these details correct?:\nEmail/Username: {username}"
                                                                                          f"\nPassword: {password}")

    if can_save:
        passwords.loc[len(passwords)] = [website, username, password]

        website_entry.delete(0, tkinter.END)
        email_entry.delete(0, tkinter.END)
        password_entry.delete(0, tkinter.END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx= 50, pady= 50)
window.title("Password Manager")

canvas = Canvas(width= 200, height= 200)
img = Image.open("logo.png")
img.save("clean_logo.png")  #to strip metadata so Tkinter will accept it
clean_img = Image.open("clean_logo.png")
logo_img = ImageTk.PhotoImage(clean_img)
canvas.create_image(100, 100, image= logo_img)
canvas.grid(row= 1, column= 2)

#Website URL Section
website_label = Label(text= "Website:")
website_label.grid(row= 2, column= 1, sticky= "w", pady= 2)
website_entry = Entry(width= 51)
website_entry.focus()
website_entry.grid(row= 2, column= 2, columnspan= 2, sticky= "w", pady= 2)

#Email/Username Section
email_label = Label(text= "Email/Username:")
email_label.grid(row= 3, column= 1, sticky= "w", pady= 2)
email_entry = Entry(width= 51)
email_entry.grid(row= 3, column= 2, columnspan= 2, sticky= "w", pady= 2)

#Password Section
password_label = Label(text= "Password:")
password_label.grid(row= 4, column= 1, sticky= "w", pady= 2)
password_entry = Entry(width= 30)
password_entry.grid(row= 4, column= 2, sticky= "w", pady= 2)
password_button = Button(text= "Generate Password", width= 14, command= generate_password)
password_button.grid(row= 4, column= 3, sticky= "w", pady= 2)

#Add button
add_button = Button(text= "Add", width= 36, command= save)
add_button.grid(row= 5, column= 2, columnspan= 2, pady= 2)
window.bind(sequence= '<Return>',func= save)

#password copied to clipboard message
copied_label = Label(text= "Password copied to clipboard", font= ("roboto", 8, "italic"))



window.mainloop()

#conditional only prints header if the file is empty or doesn't exist yet
if not os.path.exists("passwords_file_ex.txt") or os.stat("passwords_file_ex.txt").st_size == 0:
    passwords.to_csv(passwords_file, sep='|', index=False)
else:
    passwords.to_csv(passwords_file, sep='|', index=False, header= False)

passwords_file.close()
import json
import os
import random
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import pandas
from tkinter import messagebox
import pyperclip

try:
    passwords_file = open("passwords_file_ex.json", mode="r")
    if not os.path.getsize("passwords_file_ex.json") > 0:
        raise FileNotFoundError
    # Read JSON content into DataFrame
    data = json.load(passwords_file)
    passwords = pandas.DataFrame(data)
except FileNotFoundError:
    # File doesn't exist or has nothing in it; create empty DataFrame
    passwords = pandas.DataFrame(columns=["Website", "Email/Username", "Password"])

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

#Return credentials for website in website_entry if website has credentials stored in passwords
def search():
    website = website_entry.get().strip()

    #controls for user trying to search with empty website field
    if website.strip() == "":
        messagebox.showwarning(title= "Error", message= "Please enter the name of the website with the credentials you're searching for.")
        return

    try:
        result = passwords[passwords["Website"].str.lower() == website.lower()]

        email = result.iloc[0]["Email/Username"]
        password = result.iloc[0]["Password"]

        messagebox.showwarning(title= website, message= f"Email/Username: {email}"
                                                         f"\nPassword: {password}")
    except KeyError:
        messagebox.showwarning(title= "Error", message= f"No details for {website} found.")
    finally:
        return

#flashes a 'copied to clipboard' message on screen
def flash_copy_message():
    copied_label.grid(row=6, column= 2, sticky= "s", pady= 5)
    global flash
    flash = copied_label.after(2000, func= copied_label.grid_forget)

#Saves passwords to a pandas dataframe which will be printed to a file later
def save(event=None):
    website = website_entry.get().strip()
    password = password_entry.get().strip()
    username = email_entry.get().strip()

    if website == "" or password == "" or username == "":
        messagebox.showwarning(title= "Error", message= "Please do not leave any fields blank.")
        return

    #check if credentials have already been entered for the website
    try:
        website_index = passwords[passwords["Website"] == website]
        if website_index.empty:
            raise KeyError
    except KeyError:
        pass
    else:
        #if they have, then ask if the user wants to change the current credentials

        old_email = website_index.iloc[0]["Email/Username"]
        old_password = website_index.iloc[0]["Password"]

        change_credentials = messagebox.askokcancel(title= f"Credentials already exist for \"{website}\"", message= f"You already have credentials saved for \"{website}\" saved:"
                                                                                                            f"\nEmail/Username: {old_email}"
                                                                                                            f"\nPassword: {old_password}"
                                                                                                             "\n\n Do you wish to change them?")
        if not change_credentials:
            website_entry.delete(0, tkinter.END)
            email_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)
            return
        else:
            can_save = messagebox.askokcancel(title= website, message= f"Are these details correct?:\nEmail/Username: {username}"
                                                                       f"\nPassword: {password}")

            if can_save:
                passwords.drop(website_index.index[0], inplace= True)
                passwords.loc[len(passwords)] = [website, username, password]

                website_entry.delete(0, tkinter.END)
                email_entry.delete(0, tkinter.END)
                password_entry.delete(0, tkinter.END)
                website_entry.focus()
                return
            return

    can_save = messagebox.askokcancel(title= website, message= f"Are these details correct?:\nEmail/Username: {username}"
                                                                                          f"\nPassword: {password}")

    if can_save:
        passwords.loc[len(passwords)] = [website, username, password]

        website_entry.delete(0, tkinter.END)
        email_entry.delete(0, tkinter.END)
        password_entry.delete(0, tkinter.END)
        website_entry.focus()

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
website_entry = Entry(width= 30)
website_entry.focus()
website_entry.grid(row= 2, column= 2, sticky= "w", pady= 2)

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

#Search button
search_button = Button(text= "Search", width= 14, command= search)
search_button.grid(row= 2, column= 3, sticky= "w", pady= 2)

#password copied to clipboard message
copied_label = Label(text= "Password copied to clipboard", font= ("roboto", 8, "italic"))



window.mainloop()

with open("passwords_file_ex.json", mode="w") as passwords_file:
    json.dump(passwords.to_dict(orient="records"), passwords_file, indent=4)
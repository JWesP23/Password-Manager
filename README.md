# Password Manager
A simple, interactive password manager built using Python and Tkinter. This application allows users to generate strong passwords, copy them to the clipboard, and save login credentials (website, email/username, password) to a text file using a clean graphical interface.

## Features

- Password Generation: Creates complex passwords with letters, numbers, and symbols.
- Clipboard Support: Copies generated passwords to the clipboard automatically.
- Data Storage: Saves website, email/username, and password entries to a local text file (`passwords_file_ex.txt`) in a structured format using `pandas`.
- User Interface: Built with `Tkinter`, includes clean layout, logo display, and helpful UI feedback (e.g., “Password copied to clipboard”).

## Tech Stack

- Python 3.x
- Tkinter (`tkinter`)
- Pillow (`PIL.Image`, `ImageTk`)
- Pandas (`pandas`)
- Pyperclip (`pyperclip`)

## How to Run

   ```bash
   pip install pandas pillow pyperclip
   python password_manager.py

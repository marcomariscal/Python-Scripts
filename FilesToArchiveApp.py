import datetime
import os
import string
from shutil import copyfile

import tkinter as tk
from tkinter import ttk

### duplicates all files in a folder and appends the current date at the time of
### copy to the end of the file, archiving it into an "archive" folder

# the directory of where the script lives
current_directory = os.path.dirname(os.path.abspath(__file__)) or 'SPECIFY_YOUR_LOCAL_DIRECTORY'

# any files to omit from sending to the archive folder
files_to_omit = ['Archive', 'files_to_archive_app.py', 'files_to_archive_app.exe', 'Script', 'files_to_archive.py', 'files_to_archive.exe']

# filter the file to omit from the overall files list
filtered_file_list = [file for file in os.listdir(current_directory) if file not in files_to_omit]

def make_archive(current_directory):

    archive_directory = current_directory + '\\Archive\\'

    if not os.path.exists(archive_directory):
        try:
            os.makedirs(archive_directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return archive_directory

def generate_today_string():

    return datetime.date.today()

def append_id(filename):

    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=generate_today_string(), ext=ext)

# gather the list of files that the user wants to archive
def select_files(checked_bools, all_items):

    checked_list = []
    for i in range(len(checked_bools)):
        if checked_bools[i] == True:
            checked_list.append(all_items[i])

    return checked_list

def make_file_dict(selected_files, current_directory, archive_directory):

    file_dict = dict()
    
    for file in selected_files:
        full_file_name = current_directory + '\\' + file
        new_file_name = archive_directory + '\\' + file
        new_file = append_id(new_file_name)
        file_dict[full_file_name] = new_file
    
    return file_dict

# "make" a new file with the created at datetime
def copy_files(file_dict):

    for source, dest in file_dict.items():
        copyfile(source, dest)

# small gui so the user can mark which files to archive
class CheckBoxes(tk.Tk):

    def __init__(self, rows=10, columns=10, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.btns = []
        self.selected = [False] * (rows * columns)
        for i in range(len(filtered_file_list)):
            cbtn = ttk.Checkbutton(self, text=filtered_file_list[i], command=self.update)
            cbtn.state(('!alternate',)) # unchecked by default
            cbtn.pack(anchor = 'w')
            self.btns.append(cbtn)

        btn = ttk.Button(self, text="Submit", command=self.destroy) # closes the window - same effect as clicking the 'X'
        btn.pack()

    def update(self):
        self.selected = [btn.instate(('selected',)) for btn in self.btns]

# run gui
btn_box = CheckBoxes()
btn_box.mainloop()
selected_files = btn_box.selected # get the resulting list of selected checkboxes
checked_list = select_files(selected_files, filtered_file_list)
archive_directory = make_archive(current_directory)
file_dict = make_file_dict(checked_list, current_directory, archive_directory)
copy_files(file_dict)
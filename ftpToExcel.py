# log into an ftp, download the file to a specified location, and write that file into an excel spreadsheet
import ftplib
import pandas as pd

# specify ftp credentials
domain = 'YOUR_FTP_DOMAIN'
user = 'USERNAME'
pwd = 'PASSWORD'

# specify ftp folder name that the file lives in, and the file name itself
folder = 'FOLDER'
filename = 'FILENAME'  # file name within the ftp folder

# specify where to put downloaded data, and where to write the data to
local_path = r"LOCAL_PATH"    # where to place the data on your local drive from the ftp folder
dest = r"EXCEL_SHEET_FILE_PATH" # where to write the data to (the excel workbook and sheet)

# open ftp connection
ftp = ftplib.FTP(domain, user, pwd)
ftp.cwd(folder)

def grab_file():

    localfile = open(local_path, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    localfile.close()

# read data into a pandas dataframe, specify file type
def read_file():

    df = pd.read_csv(local_path, delimiter='\t')
    return df

# write the data from the file to an excel sheet
def write_file():

    writer = pd.ExcelWriter(dest, engine='xlsxwriter')
    rdf = read_file()
    rdf.to_excel(writer, sheet_name='Sheet1')
    writer.save()

grab = grab_file()
wfile = write_file()

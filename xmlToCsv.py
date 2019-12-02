import csv
import requests
from collections import OrderedDict
import ftplib
import os
import pandas as pd

# imports for transforming xml to dictionary
from xml.etree.ElementTree import fromstring, ElementTree
import xmltodict

dest = r"LOCAL_FILE_PATH"
url = "URL_TO_CHANGE_TO_CSV"

# ftp credentials
domain = 'FTP_DOMAIN'
user = 'FTP_USERNAME'
pwd = 'FTP_PASSWORD'

def getUrlContent(url):

    # use a header if you get an error trying to fetch the URL    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
  
    response = requests.get(url, headers=headers) 
    content = response.content

    return content
    
def parseXMLToDict(content):
    
    xmldict = xmltodict.parse(content)

    return xmldict

def dictToDf(d):
   
    df = pd.DataFrame.from_dict(dict(d), orient='index')

    # extract the specific data we need to make the dataframe (all other items
    # are superflous)
    # the below is specific to the XML that is being used
    df = df["url"]["urlset"]
    df = pd.DataFrame.from_dict(df)
    df = df.reset_index(drop=True)

    return df

def dfToCSV(df):
    
    df.to_csv(dest, index=False)

def writeToFTP(file):
  
    session = ftplib.FTP(domain, user, pwd)
    file = open(file,'rb')               
    session.storbinary('STOR %s' % os.path.basename(dest), file)
    file.close()
    session.quit()

def main():

    content = getUrlContent(url)
    parsed = parseXMLToDict(content)
    df = dictToDf(parsed)
    dfToCSV(df)
    writeToFTP(dest)
    
    return df



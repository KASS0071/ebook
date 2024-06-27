import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the HTML from the URL and pass on to BeautifulSoup
top100url = 'https://www.gutenberg.org/browse/scores/top'
url = top100url
print(f"Opening the file connection to {url}")
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
print("Connection established and HTML parsed...")

# Empty list to hold all the http links in the HTML page
lst_links=[]

# Find all the href tags and store them in the list of links
for link in soup.find_all('a'):
    print(link.get('href'))
    lst_links.append(link.get('href'))

# Use regular expression to find the numeric digits in these links. These are the file number for the Top 100 books. 
# Initialize empty list to hold the file numbers
booknum=[]

# Number 19 to 119 in the original list of links have the Top 100 books' number.
# now is 33-133
for i in range(33,133):
	link=lst_links[i]
	link=link.strip()
	print('link='+link)
	# Regular expression to find the numeric digits in the link (href) string
	n=re.findall('[0-9]+',link)
	if len(n)==1:
		# Append the filenumber casted as integer
		booknum.append(int(n[0]))

print ("\nThe file numbers for the top 100 ebooks on Gutenberg are shown below\n"+"-"*70)
print(booknum)

start_idx=soup.text.splitlines().index('Top 100 EBooks yesterday')
lst_titles_temp=[] # Empty list of Ebook names
# skip the TOP to real titles
for i in range(8, 108):
    lst_titles_temp.append(soup.text.splitlines()[start_idx+2+i])

# Use regular expression to extract only text from the name strings and append to an empty list
lst_titles=[]

for i in range(100):
    origtxt = lst_titles_temp[i]
    #id1,id2=re.match('^[a-zA-Z ]*',origtxt).span()
    #tx=lst_titles_temp[i][id1:id2]
    #print(i, tx)
    left_text = origtxt.partition("(")[0]
    title=left_text.replace(":", "~")
    print('title='+title)
    lst_titles.append(title)

for l in lst_titles:
    print(l)
    
    
def download_top_books(type='txt', num_download=10,verbosity=0):
    """
    Function: Download top N books from Gutenberg.org where N is specified by user
    Verbosity: If verbosity is turned on (set to 1) then prints the downloading status for every book
    Returns: Returns a dictionary where keys are the names of the books and values are the raw text.
    Exception Handling: If a book is not found on the server (due to broken link or whatever reason), inserts "NOT FOUND" as the text.
    """
    topEBooks = {}
    
    if num_download<=0:
        print("I guess no download is necessary")
        return topEBooks
    
    if num_download>100:
        print("You asked for more than 100 downloads.\nUnfortunately, Gutenberg ranks only top 100 books.\nProceeding to download top 100 books.")
        num_download=100
    
    # Base URL for files repository
    baseurl= 'http://www.gutenberg.org/files/'
    
    if verbosity==1:
        count_done=0
        for i in range(num_download):
            print ("Working on book:", lst_titles[i])
            
            # Create the proper download link (url) from the book id
            # You have to examine the Gutenberg.org file structure carefully to come up with the proper url
            bookid=booknum[i]
            bookurl= baseurl+str(bookid)+'/'+str(bookid)+'-0.'+type
            print('bookurl='+bookurl)
            # Create a file handler object
            try:
                fhand = urllib.request.urlopen(bookurl)
                txt_dump = ''
                # Iterate over the lines in the file handler object and dump the data into the text string
                for line in fhand:
                    # Use decode method to convert the UTF-8 to Unicode string
                    txt_dump+=line.decode()
                # Add downloaded text to the dictionary with keys matching the list of book titles.
                # This puts the raw text as the value of the key of the dictionary bearing the name of the Ebook 
                topEBooks[lst_titles[i]]=txt_dump
                count_done+=1
                print (f"Finished downloading {round(100*count_done/num_download,2)}%")
            except urllib.error.URLError as e:
                topEBooks[lst_titles[i]]="NOT FOUND"
                count_done+=1
                print(f"**ERROR: {lst_titles[i]} {e.reason}**")
    else:
        count_done=0
        from tqdm import tqdm, tqdm_notebook
        for i in tqdm(range(num_download),desc='Download % completed',dynamic_ncols=True):
            # Create the proper download link (url) from the book id
            # You have to examine the Gutenberg.org file structure carefully to come up with the proper url
            bookid=booknum[i]
            bookurl= baseurl+str(bookid)+'/'+str(bookid)+'-0.'+type
            print('bookurl='+bookurl)
            # Create a file handler object
            try:
                fhand = urllib.request.urlopen(bookurl)
                txt_dump = ''
                # Iterate over the lines in the file handler object and dump the data into the text string
                for line in fhand:
                    # Use decode method to convert the UTF-8 to Unicode string
                    txt_dump+=line.decode()
                # Add downloaded text to the dictionary with keys matching the list of book titles.
                # This puts the raw text as the value of the key of the dictionary bearing the name of the Ebook 
                topEBooks[lst_titles[i]]=txt_dump
                count_done+=1
            except urllib.error.URLError as e:
                topEBooks[lst_titles[i]]="NOT FOUND"
                count_done+=1
                print(f"**ERROR: {lst_titles[i]} {e.reason}**")
        
    print ("-"*40+"\nFinished downloading all books!\n"+"-"*40)
       
    return (topEBooks)

def save_text_files(type='txt',num_download=10,verbosity=1):
    """
    Downloads top N books from Gutenberg.org where N is specified by user.
    If verbosity is turned on (set to 1) then prints the downloading status for every book.
    Asks user for a location on computer where to save the downloaded Ebooks and process accordingly.
    Returns status message indicating how many ebooks could be successfully downloaded and saved
    """
    
    import os
    
    # Download the Ebooks and save in a dictionary object (in-memory)
    dict_books=download_top_books(type, num_download=num_download,verbosity=verbosity)
    download_epub_books
    if dict_books=={}:
        return None
    
    # Ask use for a save location (directory path)
    # savelocation=input("Please enter a folder location to save the Ebooks in:")
    savelocation="/home/ted/src/g-download/ebook/2024-0522"
    
    count_successful_download=0
    
    # Create a default folder/directory in the current working directory if the input is blank
    if (len(savelocation)<1):
        savelocation=os.getcwd()+os.path.sep+'Ebooks'+os.path.sep
        # Creates new directory if the directory does not exist. Otherwise, just use the existing path.
        if not os.path.isdir(savelocation):
            os.mkdir(savelocation)
    else:
        if savelocation[-1]==os.path.sep:
            os.mkdir(savelocation)
        else:
            os.mkdir(savelocation+os.path.sep)
    print("Saving files at:",savelocation)
    for k,v in dict_books.items():
        if (v!="NOT FOUND"):
            filename=savelocation+str(k)+'.txt'
            print('filename='+filename)
            file=open(filename,'wb')
            file.write(v.encode("UTF-8",'ignore'))
            file.close()
            count_successful_download+=1
    
    # Status message
    print (f"{count_successful_download} book(s) was/were successfully downloaded and saved to the location {savelocation}")
    if (num_download!=count_successful_download):
        print(f"{num_download-count_successful_download} books were not found on the server!")

def download_epub_books(type='epub', num_download=10,verbosity=0):
    """
    Function: Download top N books from Gutenberg.org where N is specified by user
    Verbosity: If verbosity is turned on (set to 1) then prints the downloading status for every book
    Returns: Returns a dictionary where keys are the names of the books and values are the raw text.
    Exception Handling: If a book is not found on the server (due to broken link or whatever reason), inserts "NOT FOUND" as the text.
    """
    import os
    topEBooks = {}
    
    if num_download<=0:
        print("I guess no download is necessary")
        return topEBooks
    
    if num_download>100:
        print("You asked for more than 100 downloads.\nUnfortunately, Gutenberg ranks only top 100 books.\nProceeding to download top 100 books.")
        num_download=100
    
    # Base URL for files repository
    #baseurl= 'http://www.gutenberg.org/files/'
    # reference url
    baseurl ='https://www.gutenberg.org/ebooks/'
    refurlext ='.images'
    if verbosity==1:
        count_done=0
        for i in range(num_download):
            print ("Working on book:", lst_titles[i])
            
            # Create the proper download link (url) from the book id
            # You have to examine the Gutenberg.org file structure carefully to come up with the proper url
            bookid=booknum[i]
            bookurl= baseurl+str(bookid)+'.'+type+refurlext
            print('bookurl='+bookurl)
            # Create a file handler object
            try:
                title = lst_titles[i]
                filename = str(bookid)+'-'+lst_titles[i]+'.'+type
                urllib.request.urlretrieve(bookurl, filename)
                topEBooks[lst_titles[i]]=title
                count_done+=1
                print (f"Finished downloading {round(100*count_done/num_download,2)}%")
            except urllib.error.URLError as e:
                topEBooks[lst_titles[i]]="NOT FOUND"
                count_done+=1
                print(f"**ERROR: {lst_titles[i]} {e.reason}**")
    else:
        count_done=0
        from tqdm import tqdm, tqdm_notebook
        for i in tqdm(range(num_download),desc='Download % completed',dynamic_ncols=True):
            # Create the proper download link (url) from the book id
            # You have to examine the Gutenberg.org file structure carefully to come up with the proper url
            bookid=booknum[i]
            bookurl= baseurl+str(bookid)+'.'+type+refurlext
            print('bookurl='+bookurl)
            # Create a file handler object
            try:
                fhand = urllib.request.urlopen(bookurl)
                txt_dump = ''
                # Iterate over the lines in the file handler object and dump the data into the text string
                for line in fhand:
                    # Use decode method to convert the UTF-8 to Unicode string
                    txt_dump+=line.decode()
                # Add downloaded text to the dictionary with keys matching the list of book titles.
                # This puts the raw text as the value of the key of the dictionary bearing the name of the Ebook 
                topEBooks[lst_titles[i]]=txt_dump
                count_done+=1
            except urllib.error.URLError as e:
                topEBooks[lst_titles[i]]="NOT FOUND"
                count_done+=1
                print(f"**ERROR: {lst_titles[i]} {e.reason}**")
        
    print ("-"*40+"\nFinished downloading all books!\n"+"-"*40)
       
    return (topEBooks)

def download_zh_epub_books(zh_data):
    """
    Function: Download top N books from Gutenberg.org where N is specified by user
    Verbosity: If verbosity is turned on (set to 1) then prints the downloading status for every book
    Returns: Returns a dictionary where keys are the names of the books and values are the raw text.
    Exception Handling: If a book is not found on the server (due to broken link or whatever reason), inserts "NOT FOUND" as the text.
    """
    import os
    topEBooks = {}
    
    num_download = len(zh_data)
    print('num_download=', num_download)
    type='epub'
    # Base URL for files repository
    #baseurl= 'http://www.gutenberg.org/files/'
    # reference url
    baseurl ='https://www.gutenberg.org/ebooks/'
    refurlext ='.images'
    count_done=0
    for i in range(num_download):       
        # Create the proper download link (url) from the book id
        # You have to examine the Gutenberg.org file structure carefully to come up with the proper url
        bookid=zh_data[i]
        bookurl= baseurl+str(bookid)+'.'+type+refurlext
        print('bookurl='+bookurl)
        # Create a file handler object
        try:
            filename = str(bookid)+'.'+type
            urllib.request.urlretrieve(bookurl, filename)
            topEBooks[i]=filename
            count_done+=1
            print (f"Finished downloading {round(100*count_done/num_download,2)}%")
        except urllib.error.URLError as e:
            topEBooks[lst_titles[i]]="NOT FOUND"
            count_done+=1
            print(f"**ERROR: {lst_titles[i]} {e.reason}**")
    
        
    print ("-"*40+"\nFinished downloading all books!\n"+"-"*40)
       
    return (topEBooks)

if __name__ == '__main__':
	# save_text_files(type='epub', num_download=10,verbosity=1)
	# save_text_files(type='txt', num_download=5,verbosity=1)
	download_epub_books(type='epub', num_download=100,verbosity=1)
	# file = open('/home/ted/src/g-download/zh-zip-list.txt','r') lines = list(file) for line in lines:

	#zh_data = [line.strip().split(',') for line in open("/home/ted/src/g-download/zh-zip-list.txt", 'r')]
	# download_zh_epub_books(zh_data)

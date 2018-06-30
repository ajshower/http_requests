# File: http_requests.py
# Description: Example on how to create and use http-requests in Python
# Environment: PyCharm and Anaconda environment
#
# MIT License
# Copyright (c) 2018 Valentyn N Sichkar
# github.com/sichkar-valentyn
#
# Reference to:
# [1] Valentyn N Sichkar. Example on how to create and use http-requests in Python // GitHub platform [Electronic resource]. URL: https://github.com/sichkar-valentyn/http_requests (date of access: XX.XX.XXXX)


# Working with http-requests with the help of library 'requests'

import requests
import re

# Creating a request
respond = requests.get('https://docs.python.org/3.5/')

# Asking for the status code
print(respond.status_code)  # 200

# Asking for the content type
print(respond.headers['Content-Type'])  # text/html

# Showing all content of the page in a binary type
print(respond.content)  # b'< .....'

# If we're sure that the content is in test format we can use different request
print(respond.text)


# Another example of creating the request for image
respond = requests.get('https://docs.python.org/3.5/_static/py.png')
print(respond.status_code)  # 200
print(respond.headers['Content-Type'])  # image/png
print(respond.content)  # b'\x89PNG\r\n....

# Saving the got binary code for the image in the file in binary mode
with open('py.png', 'wb') as f:
    f.write(respond.content)


# Another example of creating request with parameters
respond = requests.get('https://yandex.ru/search/',
                       params={
                           'text': 'Stepic',
                           'test': 'test1',
                           'name': 'Name With Spaces',
                           'list': {'test1', 'test2'}
                       })
print(respond.status_code)  # 200
print(respond.headers['Content-Type'])  # text/html; charset=utf-8
print(respond.url)  # https://yandex.ru/search/?test=test1&list=test1&list=test2&text=Stepic&name=Name+With+Spaces
print(respond.text)  # <!DOCTYPE html><html ...


# Implementing the task
# We have as input two links
# We need to check if it is possible to go through first link to the second in two steps
link1 = input()
link2 = input()

# Creating a request for the first link
respond1 = requests.get(link1)

# Getting the content of the first link in form of text - content of document A
content1 = respond1.text

# Finding all links inside the content1
# We create pattern for regular expression
pattern = r'href="(\w.*)"'

# Getting a list with all urls inside document A
inclusions1 = re.findall(pattern, content1)

inclusions2 = []

# Going through all elements of the list
for i in range(len(inclusions1)):
    # Creating second request for the links from document A
    respond2 = requests.get(inclusions1[i])

    # Checking if the status code is equal to 200
    if respond2.status_code == 200:
        # Getting the content of the document C
        content2 = respond2.text

        # Getting a list with all urls inside document C
        inclusions2 += re.findall(pattern, content2)


# Checking if the link inside document C consists of searching link for document B
if link2 in inclusions2:
    print('Yes')
else:
    print('No')


# Implementing the task 2
# As an input there is a link where we need to find all links
# Then to extract domains from that links and sort them by alphabetical order
# link = input()
#
# # Creating a request for the link
# respond = requests.get(link)
#
# # Getting the content of the link in form of text
# content = respond.text

# Finding all links inside the content
# We create pattern for regular expression
# Option 1 (Go further to have a look on the Option 2)
pattern = r'href=("|\')(http://)?(https://)?(ftp://)?(\w.*)("|\')'

test = '''<a href="http://stepic.org/courses">
<a href='https://stepic.org'>
<a href='http://neerc.ifmo.ru:1345'>
<a href="ftp://mail.ru/distib" >
<a href="ya.ru">
<a href="www.ya.ru">
<a href="../skip_relative_links">'''

# Getting a list with all urls inside document
inclusions = re.findall(pattern, test)

domains = []
s = {}

for i in range(len(inclusions)):
    if '/' in inclusions[i][4]:
        x = inclusions[i][4].split('/')
        domains += [x[0]]
    elif ':' in inclusions[i][4]:
        x = inclusions[i][4].split(':')
        domains += [x[0]]
    else:
        domains += [inclusions[i][4]]

s = set(domains)

domains = sorted(list(s))

print(domains)


# Option 2
# Another way - to use more complex regular expression
pattern = r"<a(.*?)href(.*?)=(.*?)(\"|')(((.*?):\/\/)|(\.\.)|)(.*?)(\/|:|\"|')(.*)"

# Getting a list with all urls inside document
inclusions = re.findall(pattern, test)
                                                                    
domains = []
                                                                    
for link in inclusions:
    x = link[8]
    if x not in domains:
        domains.append(x)

domains.sort()

for x in domains:
    print(x)


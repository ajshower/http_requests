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
#link1 = input()
#link2 = input()
link1 = 'https://stepic.org/media/attachments/lesson/24472/sample1.html'
link2 = 'https://stepic.org/media/attachments/lesson/24472/sample2.html'

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


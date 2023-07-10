import shutil

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


docnamearr = []
streetnamearr = []
citynamearr = []
docspec = ["stomatolog", "ginekolog", "ortopeda", "psycholog", "chirurg", "dermatolog", "fizjoterapeuta"]

hold_url = "https://www.znanylekarz.pl/%s" % docspec[0]
url = hold_url

for i in range(0, 5): #The range can go up to 500. There is no url code after that
    if i > 0:
        url = hold_url + "/" + str(i)

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    for doc in soup.find_all("div", class_='card card-shadow-1 mb-1'):
        try:
            # Get the doctor's name
            name = doc.find("div", class_='media-body')
            docnamearr.append(name.h3.text.strip())

            # Get the text from span containing address
            hold_address = doc.find("span", class_="text-truncate").get_text()
            address_split = hold_address.split(", ") #Split address to the street and city name

            if len(address_split) == 2:
                streetnamearr.append(address_split[0])
                citynamearr.append(address_split[1])

            # Works for single image extraction
            # image = doc.find("span", class_="mb-1 avatar avatar-circle no-background")
            image_span = doc.find("span", class_="mb-1 avatar avatar-circle no-background")
            image = image_span.find("img")
            try:
                image_url = "https:" + image['data-src'] #We need additional "https:" to complete the URL code
            except Exception as e1:
                image_url = "https:" + image['src']  # We need additional "https:" to complete the URL code

            img_data = requests.get(image_url, stream=True)

            # hdocimgname = docnamearr[-1] + ".jpg"
            if img_data.status_code == 200:  # 200 status code = OK
                with open("netflix.jpg", 'wb') as f:
                    img_data.raw.decode_content = True
                    shutil.copyfileobj(img_data.raw, f)

            # # If you want to see the saved photo during the debugging
            # img = mpimg.imread('netflix.jpg')
            # imgplot = plt.imshow(img)
            # plt.show()

        except Exception as e:
            pass


print(docnamearr)
print(citynamearr)
print(streetnamearr)
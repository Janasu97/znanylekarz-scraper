import shutil

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


docnamearr = []
streetnamearr = []
citynamearr = []
docspec = ["stomatolog"]

hold_url = "https://www.znanylekarz.pl/%s" % docspec[0]
url = hold_url

for i in range(0, 21): #The range can go up to 500. There is no url code after that
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

            # Get the avatar of the doctor
            # image = doc.find("a", class_="img")
            # hold_image = image.src
            image = doc.select('div img')
            image_url = image[0]['src']
            img_data = requests.get("https://www.znanylekarz.pl/karolina-szydlo-slabicka/stomatolog/gdynia#address-id=%5B966566%5D&filters%5Bspecializations%5D%5B%5D=103/" + image_url, stream=True)
            # with open('netflix.jpg', 'wb') as handler:
            #     handler.write(img_data)

            if img_data.status_code == 200:  # 200 status code = OK
                with open("netflix.jpg", 'wb') as f:
                    img_data.raw.decode_content = True
                    shutil.copyfileobj(img_data.raw, f)

            img = mpimg.imread('netflix.jpg')
            imgplot = plt.imshow(img)
            plt.show()

            if len(address_split) == 2:
                streetnamearr.append(address_split[0])
                citynamearr.append(address_split[1])

        except Exception as e:
            pass


print(docnamearr)
print(citynamearr)
print(streetnamearr)
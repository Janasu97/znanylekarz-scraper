import shutil
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


docnamearr = []
streetnamearr = []
citynamearr = []
companynamearr = []
doctitle = []
docpricearr = []
docspec = ["stomatolog", "ginekolog", "ortopeda", "psycholog", "chirurg", "dermatolog", "fizjoterapeuta"]

hold_url = "https://www.znanylekarz.pl/%s" % docspec[0]
url = hold_url

for i in range(0, 5): #The range can go up to 500. There is no url code after that, at least for the stomatologist
    if i > 0:
        url = hold_url + "/" + str(i)

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    for doc in soup.find_all("div", class_='card card-shadow-1 mb-1'):
        try:
            # Get the doctor's name
            main_name = doc.find("div", class_='media-body').h3.text.strip()
            hdocname = main_name.split(".")[-1]
            doctitle.append(main_name.replace(hdocname, ""))
            docnamearr.append(hdocname)

            # Get the service price
            price_all = doc.find("p", class_="m-0 text-nowrap font-weight-bold").text.strip()
            price = int(re.search(r'\d+', price_all).group())
            docpricearr.append(price)

            # Get the text from span containing address and company name
            hold_address = doc.find("span", class_="text-truncate").get_text()
            address_split = hold_address.split(", ") #Split address to the street and city name
            if len(address_split) == 2:
                streetnamearr.append(address_split[0])
                citynamearr.append(address_split[1])
            holdcompname = doc.find("p", class_="m-0 text-truncate text-muted font-weight-bold address-details").get_text().strip()
            companynamearr.append(holdcompname)

            # Scratch the avatar image of the doctor / clinic
            try:
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

            except Exception as e2:
                pass



            # Scratch the data of the specialists if the main name is the clinic instead of doctor
            # sub_spec_div = doc.findall("div", class_="card card-border card-shadow-1 m-0 mr-0-5 h-100")
            sub_spec_div = doc.find_all("div", class_="card card-border card-shadow-1 m-0 mr-0-5 h-100")
            for spec in sub_spec_div:

                # Append specialist name and title
                spec_main_name = spec.find("p", class_="text-body small mb-0").get_text().strip()
                hspecdocname = spec_main_name.split(".")[-1]
                doctitle.append(spec_main_name.replace(hspecdocname, ""))
                docnamearr.append(hspecdocname)

                #Append price
                docpricearr.append(price)

                #Append addres
                if len(address_split) == 2:
                    streetnamearr.append(address_split[0])
                    citynamearr.append(address_split[1])
                companynamearr.append(holdcompname)

                #Append avatar image
                try:
                    spec_div = spec.find("div", class_="card-header card-header-no-border m-auto pt-1")
                    spec_image_span = spec.find("span", class_="avatar avatar-sm avatar-circle no-background")
                    spec_image = spec_image_span.find("img")

                    try:
                        spec_image_url = "https:" + spec_image['data-src']  # We need additional "https:" to complete the URL code
                    except Exception as e1:
                        spec_image_url = "https:" + spec_image['src']  # We need additional "https:" to complete the URL code

                    spec_img_data = requests.get(spec_image_url, stream=True)

                    # hdocimgname = docnamearr[-1] + ".jpg"
                    if spec_img_data.status_code == 200:  # 200 status code = OK
                        with open("netflix.jpg", 'wb') as f:
                            spec_img_data.raw.decode_content = True
                            shutil.copyfileobj(spec_img_data.raw, f)
                except Exception as e3:
                    pass

        except Exception as e:
            pass


# Just to see what data we are scrapping for now
print(docnamearr)
print(doctitle)
print(docpricearr)
print(citynamearr)
print(streetnamearr)
print(companynamearr)

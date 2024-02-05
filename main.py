import shutil
import re
import requests
from bs4 import BeautifulSoup
import sqlite3


#Functions to check if the record already exists in the database
def check_if_medic_in_db(cursor, medic_name):
    cursor.execute("SELECT COUNT(name) FROM Medics WHERE name = ?", (medic_name,))
    count = cursor.fetchone()[0]
    return count > 0

def check_if_spec_in_db(cursor, specialistname):
    cursor.execute("SELECT COUNT(specname) FROM Specializations WHERE specname = ?", (specialistname,))
    count = cursor.fetchone()[0]
    return count > 0

conn = sqlite3.connect("ZNANYLEKARZ.db")
c = conn.cursor()

#Try to create the Specializations table
c.execute('''
    CREATE TABLE IF NOT EXISTS Specializations(
    ID INTEGER PRIMARY KEY,
    specname TEXT, 
    description TEXT
    )
''')

#Try to create Medics table containing webscrapper data
c.execute('''
    CREATE TABLE IF NOT EXISTS Medics(
    ID INTEGER PRIMARY KEY,
    name TEXT,
    title TEXT,
    specID INTEGER, 
    locationID INTEGER,
    companyID INTEGER,
    price REAL,
    avatar BLOB,
    FOREIGN KEY (specID) REFERENCES Specializations(ID),
    FOREIGN KEY (locationID) REFERENCES Locations(ID),
    FOREIGN KEY (companyID) REFERENCES Companies(ID)
    )
''')

#Try to create the Locations table
c.execute('''
    CREATE TABLE IF NOT EXISTS Locations(
    ID INTEGER PRIMARY KEY,
    street TEXT,
    city TEXT
    )
''')

#Try to create the Companies table
c.execute('''
    CREATE TABLE IF NOT EXISTS Companies(
    ID INTEGER PRIMARY KEY,
    name TEXT,
    locationID INTEGER,
    FOREIGN KEY (locationID) REFERENCES Locations(ID)
    )
''')



specializations_data = [
    ("stomatolog", "A dentist specializing in oral health."),
    ("ginekolog", "A medical professional specializing in women's health."),
    ("ortopeda", "A doctor specializing in the musculoskeletal system."),
    ("psycholog", "A professional focusing on mental and emotional well-being."),
    ("chirurg", "A surgeon specializing in surgical procedures."),
    ("dermatolog", "A medical practitioner dealing with skin-related issues."),
    ("fizjoterapeuta", "A physiotherapist specializing in physical therapy.")
]
specializations_data_ID = []
specializations_data_names = []

for spec in specializations_data:
    if not check_if_spec_in_db(c, spec[0]):
        c.execute("INSERT INTO Specializations (specname, description) VALUES (?,?)",spec)

c.execute("SELECT ID, specname FROM Specializations")
specresults = c.fetchall()


#Select the specialization of the medics you want to scrap the data for
print(specresults)
medicspecID = int(input("Enter the index of the specialisation type you want to scrap:"))
specresultsdict = dict(specresults)
holdspecname = specresultsdict[medicspecID]
print("You selected %s" % holdspecname)

hold_url = "https://www.znanylekarz.pl/%s" % holdspecname
url = hold_url

recscrapcount = 0
pagescount = int(input("Enter the number of pages to browse through for data scrapping: "))
for i in range(0, pagescount): #The range can go up to 500. There is no url code after that, at least for the stomatologist
    if i > 0:
        url = hold_url + "/" + str(i)

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    for doc in soup.find_all("div", class_='card card-shadow-1 mb-1'):
        try:
            #Flag to determine if the scratched main profile is company or singular doctor
            profileiscompany = False

            # Get the doctor's name
            main_name = doc.find("div", class_='media-body').h3.text.strip()
            hdocname = main_name.split(".")[-1]
            hdoctitle = main_name.replace(hdocname, "")


            # Get the service price
            price_all = doc.find("p", class_="m-0 text-nowrap font-weight-bold").text.strip()
            price = int(re.search(r'\d+', price_all).group())

            # Get the text from span containing address and company name
            hold_address = doc.find("span", class_="text-truncate").get_text()
            address_split = hold_address.split(", ") #Split address to the street and city name

            #Sometimes the number of the street is by accident put after , and as the continuity of the street name
            if len(address_split)>2:
                address_split[0] = address_split[0] + " " + address_split[1]
                address_split[1] = address_split[2]
                address_split.pop()

            holdcompname = doc.find("p", class_="m-0 text-truncate text-muted font-weight-bold address-details").get_text().strip()


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
                    with open("storeavatar.jpg", 'wb') as f:
                        img_data.raw.decode_content = True
                        shutil.copyfileobj(img_data.raw, f)

                    with open("storeavatar.jpg", 'rb') as avatar_img:
                        avatar_data = avatar_img.read()

            except Exception as e2:
                pass



            # Scratch the data of the specialists if the main name is the clinic instead of doctor
            sub_spec_div = doc.find_all("div", class_="card card-border card-shadow-1 m-0 mr-0-5 h-100")
            compinserted = False
            holdcompID = 0
            holdlocationID = 0
            for spec in sub_spec_div:
                #If there are positions here then the profile is company and have multiple doctors assigned
                profileiscompany = True

                # Get specialist name and title
                spec_main_name = spec.find("p", class_="text-body small mb-0").get_text().strip()
                hspecdocname = spec_main_name.split(".")[-1]
                hspecdoctitle = spec_main_name.replace(hspecdocname, "")



                #Get avatar image
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
                        with open("storeavatar.jpg", 'wb') as f:
                            spec_img_data.raw.decode_content = True
                            shutil.copyfileobj(spec_img_data.raw, f)

                        with open("storeavatar.jpg", 'rb') as avatar_img:
                            avatar_data = avatar_img.read()


                except Exception as e3:
                    pass

                #First check if record is not already in the db
                if not check_if_medic_in_db(c, hdocname):

                    #Add to db if the main profile is company
                    #Insert the company into the Companies table and lovation into Locations table
                    if compinserted==False:
                        #Insert the scratche data into the Locations table of db
                        c.execute("INSERT INTO Locations (street, city) VALUES (?,?)",address_split)
                        holdlocationID = c.lastrowid

                        c.execute("INSERT INTO Companies (name, locationID) VALUES (?, ?)",(holdcompname,holdlocationID))
                        holdcompID = c.lastrowid

                    #Insert the scratched data into the Medics table of db
                    c.execute("INSERT INTO Medics (name, title, specID, locationID, companyID, price, avatar) VALUES (?,?,?,?,?,?,?)",
                              (hspecdocname,hspecdoctitle,medicspecID,holdlocationID,holdcompID,price,avatar_data))

                    recscrapcount += 1


            #Add new record only if the main profile is not a company
            if profileiscompany == False:

                #First check if record is not already in the db
                if not check_if_medic_in_db(c, hdocname):

                    #Insert the scratche data into the Locations table of db
                    c.execute("INSERT INTO Locations (street, city) VALUES (?,?)",address_split)
                    holdlocationID = c.lastrowid

                    #Insert the company record
                    c.execute("INSERT INTO Companies (name, locationID) VALUES (?, ?)",(holdcompname,holdlocationID))
                    holdcompID = c.lastrowid

                    #Insert the scratched data into the Medics table of db
                    c.execute("INSERT INTO Medics (name, title, specID, locationID, companyID, price, avatar) VALUES (?,?,?,?,?,?,?)",
                              (hdocname,hdoctitle,medicspecID,holdlocationID,holdcompID,price,avatar_data))

                    recscrapcount += 1

        except Exception as e:
            pass

conn.commit()
conn.close()

print("Operation completed. %s records scraped." % recscrapcount)

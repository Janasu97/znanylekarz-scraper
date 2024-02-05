import sqlite3
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#In this script I simply want to check if the data has been imported correctly

conn = sqlite3.connect("ZNANYLEKARZ.db")
c = conn.cursor()

c.execute('''SELECT ID, name, title, specID, locationID, companyID, price FROM Medics''')
results = c.fetchall()
for profile in results:
    print(profile)

c.execute("SELECT avatar from Medics WHERE ID = '1'")
av_data = c.fetchone()

# Check if avatar_data is not None
if av_data:
    # Convert the image data to a BytesIO object
    image_stream = BytesIO(av_data[0])

    # Display the image using matplotlib.pyplot
    img = mpimg.imread(image_stream, format='jpg')
    plt.imshow(img)
    plt.axis('off')  # Hide axis
    plt.show()

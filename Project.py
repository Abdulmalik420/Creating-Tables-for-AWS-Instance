import mysql.connector
from faker import Faker
import numpy as np
import random

# these are all the faker providers that I used to generate the data.
# The IDE I use is IntelliJ and for this Faker is package like pandas and mysql.connector

from faker.providers import barcode
from faker.providers import person
from faker.providers import date_time
from faker.providers import lorem
from faker.providers import currency
from faker.providers import address
from faker.providers import internet

# In order to do a lot of tests I had to keep dropping the database in MySQL and I used this code to make a new database
# every time I dropped it. There is probably an easier to do this with DELETE probably but this was much easier and
# faster to do. I had this code in another tab so I could run it with out worrying about the other code that need
# a database.

# mydbase = mysql.connector.connect(host="[AWS Host Name]",
#                                   user="[Username]",
#                                   password="[Password]"
#                                   )
#
# mycursor = mydbase.cursor()
# mycursor.execute("CREATE DATABASE [Database]")
#

mydbase = mysql.connector.connect(host="[AWS Host Name]",
                                  user="[Username]",
                                  password="[Password]",
                                  database="[Database]"
                                  )
mycursor = mydbase.cursor()

# This amountdata is the amount of data that will be input. So by changing this you can change the amount of data
# that you want to input.
amountdata = 20

# This is just a simple random gender picker.
genderList = ['F', 'M']

# These for loops are the Primary Key generators. The Faker.seed() is there to make sure that the numbers generated
# are the same. If I do it without the seed then when I call it the generator might give me a different number that is
# that would cause the primary key to be different. This way all of the keys can be linked. The way I made sure that
# the primary key of one table would not be the same as others is by using prefixes in the faker.ean8() method to make
# sure that they will always be different.

fake = Faker()
Faker.seed(1222)
UserIDS = np.empty(amountdata, dtype=int)
for i in range(amountdata):
    UserIDS[i] = fake.ean8(prefixes=('10', ))
    print(UserIDS[i])

Faker.seed(1223)
FriendIDS = np.empty(amountdata, dtype=int)
for i in range(amountdata):
    FriendIDS[i] = fake.ean8(prefixes=('20', ))
    print(FriendIDS[i])

Faker.seed(1224)
ProductIDS = np.empty(amountdata, dtype=int)
for i in range(amountdata):
    ProductIDS[i] = fake.ean8(prefixes=('30', ))
    print(ProductIDS[i])

Faker.seed(1225)
AddressIDS = np.empty(amountdata, dtype=int)
for i in range(amountdata):
    AddressIDS[i] = fake.ean8(prefixes=('40', ))
    print(AddressIDS[i])

Faker.seed(1226)
PostIDS = np.empty(amountdata, dtype=int)
for i in range(amountdata):
    PostIDS[i] = fake.ean8(prefixes=('50', ))
    print(PostIDS[i])

# This is all the code to INPUT the tables into the database with its attributes.

mycursor.execute("CREATE TABLE users (UserID INT PRIMARY KEY, UserName VARCHAR(255), Fname VARCHAR(255), "
                 "Lname VARCHAR(255), Age INT(255), Gender VARCHAR(255), DateCreated INT(255),"
                 "LastAccessed INT(255))")

mycursor.execute("CREATE TABLE friend (FUserID INT, FOREIGN KEY (FUserID) REFERENCES users(UserID) on delete cascade, "
                 "UserName VARCHAR(255), "
                 " FriendSince INT(255), FriendID INT PRIMARY KEY )")

mycursor.execute("CREATE TABLE address (AUserID INT, FOREIGN KEY (AUserID) REFERENCES users(UserID) on delete "
                 "cascade, AddressID INT PRIMARY KEY, "
                 "Street VARCHAR(255), City VARCHAR(255), ZipCode INT)")

mycursor.execute("CREATE TABLE product (OUserID INT, FOREIGN KEY (OUserID) REFERENCES users(UserID) on delete cascade, "
                 "ProductID INT PRIMARY KEY, "
                 "ProductName VARCHAR(255), ProductPrice VARCHAR(255),OAddressID INT, FOREIGN KEY (OAddressID) "
                 "REFERENCES "
                 "address(AddressID) on delete cascade)")

mycursor.execute("CREATE TABLE post (PUserID INT, FOREIGN KEY (PUserID) REFERENCES users(UserID) on delete cascade, "
                 "PostID INT PRIMARY KEY, "
                 "PostedDate INT)")

mycursor.execute("CREATE TABLE messages (MUserID INT, FOREIGN KEY (MUserID) REFERENCES users(UserID) on delete "
                 "cascade, LastMessaged INT, MFriendID INT, "
                 "FOREIGN KEY (MFriendID) REFERENCES friend(FriendID) on delete cascade)")

# The for loop was used here to make this repeat what ever the amountdata is. With this for loop I can use it to go
# through the primary key arrays as well

for i in range(amountdata):
    sql = "INSERT INTO users (UserID, UserName, Fname, Lname, Age, Gender, DateCreated, LastAccessed) VALUES " \
          "(%s,%s,%s,%s,%s,%s,%s,%s)"
    val = [(UserIDS.item(i),
            fake.user_name(),
            fake.first_name(),
            fake.last_name(),
            fake.random_int(15, 40),
            random.choice(genderList),
            fake.date_time_between(start_date="-10y", end_date="-5y"),
            fake.date_time_between(start_date="-5y", end_date="now"))
           ]

    sql2 = "INSERT INTO friend (FUserID, UserName, FriendSince, FriendID) VALUES " \
           "(%s,%s,%s,%s)"
    val2 = [(UserIDS.item(i),
             fake.word(),
             fake.date_time_between(start_date="-10y", end_date="-5y"),
             FriendIDS.item(i))
            ]

    sql3 = "INSERT INTO product (OUserID, ProductID, ProductName, ProductPrice, OAddressID) VALUES " \
           "(%s, %s, %s, %s, %s)"
    val3 = [(UserIDS.item(i),
             ProductIDS.item(i),
             fake.word(),
             fake.pricetag(),
             AddressIDS.item(i))
            ]

    sql4 = "INSERT INTO post (PUserID, PostID, PostedDate) VALUES " \
           "(%s, %s, %s)"
    val4 = [(UserIDS.item(i),
             PostIDS.item(i),
             fake.date_time_between(start_date="-2y", end_date="now"))
            ]

    sql5 = "INSERT INTO messages (MUserID, LastMessaged, MFriendID) VALUES " \
           "(%s, %s, %s)"
    val5 = [(UserIDS.item(i),
             fake.date_time_between(start_date="-2y", end_date="now"),
             FriendIDS.item(i))
            ]

    sql6 = "INSERT INTO address (AUserID, AddressID, Street, City, ZipCode) VALUES " \
           "(%s, %s, %s, %s, %s)"
    val6 = [(UserIDS.item(i),
             AddressIDS.item(i),
             fake.street_address(),
             fake.city(),
             fake.postcode())
            ]

    mycursor.executemany(sql, val)
    mydbase.commit()
    mycursor.executemany(sql2, val2)
    mydbase.commit()
    mycursor.executemany(sql6, val6)
    mydbase.commit()
    mycursor.executemany(sql3, val3)
    mydbase.commit()
    mycursor.executemany(sql4, val4)
    mydbase.commit()
    mycursor.executemany(sql5, val5)
    mydbase.commit()

print(mycursor.rowcount, "was inserted.")

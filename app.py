import sys
import os
import csv
from jina import Document, DocumentArray, DocumentArrayMemmap


# da = DocumentArray.load_csv("./movies_metadata.csv")
#UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 455: character maps to <undefined>


# da = DocumentArray.load_csv("./movies_metadata.csv", encoding="utf8")
#gives error with encoding .  No attribute named 'encoding' either to specify encoding or to use utf8

docs = DocumentArray()

with open("movies_metadata.csv", encoding="utf-8") as file:
    #setup csv reader
    reader = csv.DictReader(file)
    #setup list to hold dictionaries
    movies = []
    #loop through each row in the csv
    for row in reader:
        # print(row.keys())
        #append each row to the list
        movies.append(row['title'])
    # print(movies)

    da = DocumentArray.from_csv(file)

da.plot()

# print(da[])
print(da[2].tags)


print(da[1].text)
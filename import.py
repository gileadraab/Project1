import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://localhost:5432")
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open("books.csv")
	reader = csv.reader(f)
	header = reader.next()
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
			{"isbn": isbn, "title": title, "author": author, "year": year})	
		print books.isbn, books.title, books.author, books.year
	db.commit()

if __name__ == "__main__":
	main()


# flipkart-reviews
A python program to fetch reviews from flipkart.com
- Written in Python 3
#####  Built for flipkart.com

#### Usage

- python flipkart-reviews.py filename.txt

Where filename.txt is the file containg urls to fetch the reviews from. 

#### If program outputs no reviews

Probably due to change of class in the flipkart page. The classes should be updated to match the ones in Review page.

##### To try out example

Example file provided "urls.txt"

- python flipkart-reviews.py urls.txt

Creates reviews.csv, with data fetched

### Implemented Analyzer
To analyze the reviews and create a word map

#### Usage

- python analyzer.py
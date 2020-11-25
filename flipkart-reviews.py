"""Finds reviews from Flipkart URL of a product, and saves in a reviews.csv

@author : Sreedev S

Parameters
----------
filename : str
    The file name of the file containing urls

Returns
-------
file : reviews.csv
    A file containing Name of the item, price, rating, and review
"""


import sys
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

#From given parsed HTML, returns title, price, ratings, review_title, review, as dictionary and next_path-for next page as string 
def get_details(soup):
    reviews = {}
    #Checking whether Title is given for the product
    try:
        title = soup.find(class_="_2s4DIt _1CDdy2").get_text().strip()
        title = title[:-8]
        title = remove_comma(title)
    except:
        title = "Not Found"
    #Checking whether price detail is given for the product
    try:
        price = soup.find(class_="_30jeq3").get_text().strip()
        price = price[1:]
        price = remove_comma(price, replace='')
    except:
        price = "Not Found"
    
    #checking for reviews, reviews are arranged as columns, which has bundle of information like rating, review and name of person
    try:
        re_cols = soup.find_all('div', class_='col _2wzgFH K0kLPL')
        for i, col in enumerate(re_cols):
            reviews[i] = {}
            reviews[i]['title'] = title
            reviews[i]['price'] = price

            try:
                reviews[i]['rating'] = col.find(class_='_3LWZlK _1BLPMq').get_text().strip()
                reviews[i]['review_title'] = col.find(class_='_2-N8zT').get_text().strip()
                review = col.find(class_='t-ZTKy')
                review = review.div.div.get_text().strip()
                review = review[:-9] #removing 'READ MORE
                reviews[i]['review'] = review

                reviews[i]['review_title'] = remove_comma(reviews[i]['review_title']) #removing comma to be saved as csv
                reviews[i]['review'] = remove_comma(reviews[i]['review'])
            except:
                reviews[i]['rating'] = -1
                reviews[i]['review_title'] = "Review Not Found"
                reviews[i]['review'] = ""
    except:
        i = 0
        reviews[i] = {}
        reviews[i]['title'] = title
        reviews[i]['price'] = price
        reviews[i]['rating'] = -1
        reviews[i]['review_title'] = "Review Not Found"
        reviews[i]['review'] = ""
    next_path = ''
    #checking whether a Next page of review is there and getting the link
    try:
        # next_link = soup.find('div', class_='_2zg3yZ _3KSYCY')
        next_link = soup.find_all(class_='_1LKTO3')
        
        for x in next_link:
            if x.get_text() == 'Next':
                next_path =  x['href']
    except:
        pass

    return reviews, next_path

# For converting Product url into review page url
def convert_url_review(URL):

    o = urlparse(URL)
    scheme = o.scheme
    netloc = o.netloc
    path = o.path.split('/')

    path[2] = 'product-reviews'

    path = '/'.join(path)
    query = o.query
    query = parse_qs(query)
    selected = ['pid','lid','marketplace']
    new_query = {}
    if 'marketplace' not in query:
        query['marketplace'] = 'FLIPKART'
    for sel in selected:
        new_query[sel] = query[sel]

    new_query = urlencode(new_query, doseq=True)
    url_tuple =(scheme, netloc, path, '', new_query, '')
    URL = urlunparse(url_tuple)

    return URL

# For getting next page of review
def get_next_url(URL, next_path):

    o = urlparse(URL)
    scheme = o.scheme
    netloc = o.netloc
    path = next_path
    url_tuple =(scheme, netloc, path, '', '', '')
    URL = urlunparse(url_tuple)

    return URL

# removes comma from the text so that there is no error while saving or reading CSV
def remove_comma(ori_text, replace=" "):
    text = ori_text.split(',')
    new_text = replace.join(text)

    return new_text

def main(filename):

    import requests
    from bs4 import BeautifulSoup

    #use your user-agent . If you don't know search in Google "My user agent"
    header =  {"User-Agent":'fill in your user agent'}

    #file1 -> url list
    #file2 -> reviews.txt
    #file1 -> reviews.csv

    file1 = open(filename, 'r') 
    urls = file1.readlines() 
    file1.close()
    # file2 = open('reviews.txt','w')
    file3 = open('reviews.csv','w')

    file3.writelines('Item,Price,Rating,Review\n')
    #iterating through the urls provided in the file
    for URL in urls:
        #checking whether URL is valid or not
        if URL == '\n':
            continue
        try:
            page = requests.get(URL, headers=header)
        except:
            # print("Unreachable or Invalid URL")
            continue
        URL = convert_url_review(URL)
        #for checking whether next page exists
        isnext = True
        #Tracking the run, run+1 at any stage is equal to number of pages it has been through
        run = 0
        #going through the next links
        while(isnext):
            try:
                page = requests.get(URL, headers=header)
            except:
                print("Unreachable or Invalid URL")
                continue

            soup = BeautifulSoup(page.content, 'html.parser')
            reviews, next_path = get_details(soup)
            for review in reviews.values():
                if review['rating'] != -1 :
                    # if run == 0:
                        # file2.writelines(review['title']+ '\n')
                        # file2.writelines('Price : ' +review['price'] + '\n') 
                    # file2.writelines( "'" + review['review_title'] +"' " + review['rating'] + " " + review['review'] + "\n")
                    file3.writelines(review['title']+','+review['price']+','+  review['rating']+",'" + review['review_title'] +"' " + review['review'] + "\n")
            #if needed to limit number of runs uncomment
            if ( next_path == ''): # or (run == 100):
                isnext = False
                continue
            else:
                URL = get_next_url(URL, next_path)
            run += 1
        
        # print("URL ",URL)
        # print("next_path ",next_path)

    # file2.close()
    file3.close()


if __name__ == "__main__":  
    #Checking whether the filename is passed as an argument
    if len(sys.argv) > 1:
       main(sys.argv[1])
    else:
        print("usage: python flipkart-reviews.py filename.txt #where filename.txt contains URLs")

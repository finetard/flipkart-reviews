import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from fpdf import FPDF 
import sys
import io


def main():
    df = pd.read_csv('reviews.csv')
    products = list(df.Item.value_counts().keys())

    def cloudmaker(df,product):
        comment_words = '' 
        stopwords = set(STOPWORDS)
        for val in df['Review']: 
            val = str(val) 
            # split the value 
            tokens = val.split() 
        # Converts each token into lowercase 
            for i in range(len(tokens)): 
                tokens[i] = tokens[i].lower() 
                comment_words += " ".join(tokens)+" "
        wordcloud = WordCloud(width = 1000, height = 1000,max_words= 100,
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 
        plt.figure(figsize = (15, 15), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        plt.title(f'{product}')
        plt.savefig(f'{product}_cloud'+'.png')

    def review_pro(df,product):
        rates = df['Rating'].value_counts()
        plt.figure(figsize=(10,10))
        plt.bar(rates.index,rates.values,width = 0.3)
        plt.title(f'Rating from users for {product}')
        plt.ylabel('Number of users', fontsize=12)
        plt.xlabel('Rating', fontsize=12)
        for i, rate in enumerate(list(rates.values)):
            plt.text( rates.index[i] - 0.10, rates.values[i]+ 5, str(rate), color='blue')
            
        plt.savefig(f"{product}_review.png")



    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size = 25)
    pdf.cell(200, 10, txt = '*'*40,ln = 1, align = 'C')
    pdf.cell(200, 10, txt = '"Summary Report"',ln = 1, align = 'C')
    pdf.cell(200, 10, txt = '*'*40,ln = 1, align = 'C')
    pdf.set_font("Arial", size = 15)

    for product in products:
        sub_df = df[df['Item']== product]
        name = product.split()[:3]
        name = "_".join(name)
        mark = '='*50
        pdf.cell(200, 10, txt = mark,ln = 1, align = 'C')
        product = f'Product Name: {name}'
        pdf.cell(200, 10, txt = product,ln = 1, align = 'C')
        review = f'Number of Reviews: {sub_df.shape[0]}'
        pdf.cell(200, 10, txt = review,ln = 1, align = 'C')
        price = sub_df['Price'][:1].values[0]
        p = f'Price of {name} Rs.: {price}'
        pdf.cell(200, 10, txt = p,ln = 1, align = 'C')
        rating = f'Average Rating :' + str(round(np.mean(sub_df['Rating']),2))
        pdf.cell(200, 10, txt = rating,ln = 1, align = 'C')
        review_pro(sub_df,name)
        pdf.image(f'{name}_review.png',w= 190,h = 190, x = 0)
        cloudmaker(sub_df,name)
        pdf.image(f'{name}_cloud.png',w= 190,h = 190)
        mark = '='*50
        pdf.cell(200, 10, txt = mark,ln = 1, align = 'C')
    
    pdf.output("Summary_report.pdf")

main()


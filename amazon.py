from requests_html import HTMLSession
import pandas as pd

key_word = input('Enter words to search: ')
key_word = key_word.replace(' ', '+')
print(key_word)
length=len(key_word.split('+'))
print(length)
file_name = f"{key_word}.csv"
url = f'https://www.amazon.com/s?k={key_word}&ref=nb_sb_noss_{length}'

product = []


def get_price(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render()
    items = r.html.find('div.a-section.a-spacing-medium')
    # print(item)
    t = 'div.a-section>h2.a-size-mini'
    p = 'div.a-section>div.a-row>a.a-size-base>span.a-price '
    i = 'div>img'
    r = 'a>i>span'
    for item in items:
        try:
            title = item.find(t, first=True).text
        except Exception as e:
            title = None

        try:
            price = item.find(p, first=True).text
            price = price.split('$')[1]
        except Exception as e:
            price = None
        try:
            image = item.find(i, first=True).attrs['src']
        except Exception as e:
            image = None

        try:
            rating = item.find(r, first=True).text.split(' ')[0]
        except Exception as e:
            rating = None

        if price is not None:
            product.append({'title': title,
                            'rating': rating,
                            'price': price,
                            'image_link': image
                            })


get_price(url)
product = pd.DataFrame(product)
product.to_csv(file_name)
print(product)

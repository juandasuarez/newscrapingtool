import lxml.html as html
import requests
import os
import datetime

HOME_URL = 'https://www.fichajes.com'
XPATH_LINK_TO_ARTICLE = '//article[@class="articleFeatured " or @class="articleItem articleItem--withImage "]/a/@href'
XPATH_TITLE = '//section/div[2]/div/article/div/h1/text()'
XPATH_PLAYERS = '//div[@class="side__bloc noSmall"]/ul/li[@class="article__cards__person"]/div/div[@class="dataCard__infos"]/a/text()'
XPATH_COMPETITION = '//div[@class="side__bloc noSmall"]/ul/li[@class="article__cards__competition"]/div/div[@class="dataCard__infos"]/a/text()'
XPATH_TEAMS = '//div[@class="side__bloc noSmall"]/ul/li[@class="article__cards__team"]/div/div[@class="dataCard__infos"]/a/text()'


def parse_notice(link, today):
    try: 
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\n','',2)
                title = title.replace('|','')
                players = parsed.xpath(XPATH_PLAYERS)[0]
                competition = parsed.xpath(XPATH_COMPETITION)[0]
                teams = parsed.xpath(XPATH_TEAMS)[0]

            except IndexError:
                return

            # If the file closes by a error, the info still saved
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(players)
                f.write('\n\n')
                f.write(competition)
                f.write('\n\n')
                f.write(teams)
                f.write('\n\n')
                print(f)

        else: 
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)



def parse_home():
    try: 
        # Take HTML file from website
        response = requests.get(HOME_URL)
        # Conditional for avoid status code error
        if response.status_code == 200:
            # Decode is used for transform the content to be understood by Python 
            home = response.content.decode('utf-8')
            # Transform HTML document for using Xpath
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            links_to_notices = links_to_notices
            #print(links_to_notices)

            # A string with the date of today
            today = datetime.date.today().strftime('%d-%m-%Y')
            # Create folder with the data if the same folder does´t exists
            if not os.path.isdir(today):
                os.mkdir(today)

            # Extract info for each link
            for link in links_to_notices:
                link = HOME_URL + link
                parse_notice(link, today)

        else: 
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)       

def run():
    parse_home()

if __name__ == "__main__":
    run()
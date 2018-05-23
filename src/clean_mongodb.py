'''
This module is a single function to convert
the raw html code that was stored in webscrape.py into
a separate collection within the same db in MongoDB
and make it a cleaner format. Ultimately to be used
by clean_mongodb.py to convert this output
a python pandas df.
'''

import pandas as pd
import numpy as np

def raw_html_to_db(raw_html_db):
    '''
    Iterates through the mongodb collection that has all the stored raw html
    code and converts it to a cleaner format that is importable to pandas.

    Inputs: name of raw html database (in notebook its called movies)

    Outputs: None. Stores the cleaned data in a new MongoDB collection called
    movies_clean_v2
    '''

    for i in range(len(list(raw_html_db.find()))):
        single_movie_data = {}
        html = movies.find()[i]['html']
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', attrs={"itemprop" : "name"}).text

        field_name = ''
        field_value = ''

        #Populates most movie data
        table = soup.find('table', attrs={'id':'movie_finances'})
        for row in table.select('tr'):
            cols = row.select('td')
            if len(cols) > 1:
                field_name = cols[0].text.replace('.', '')
                field_value = cols[1].text.replace('$', '').replace(',', '')
            single_movie_data[field_name] = field_value

        tables = soup.select('div#summary table')
        for table in tables:
            table_html = str(table)
            if 'Production Countries:' in table_html :
                table_details = table
                break

        for row in table_details.select('tr'):
            cols = row.select('td')
            field_name = cols[0].text.replace(':', '').replace('\xa0', ' ')
            field_value = cols[1].text.replace('$', '').replace(',', '')
            single_movie_data[field_name] = field_value

        tables = soup.find_all('div', attrs={'class':'cast_new'})

        #Populates cast and crew lists
        for table in tables:
            table_html = str(table)
            if 'Lead Ensemble' in table_html or 'Leading Cast' in table_html:
                table_cast = table
                cast_lst = []
                for row in table_cast.select('tr'):
                    cols = row.select('td')
                    actor_name= cols[0].text
                    cast_lst.append(actor_name)
                single_movie_data['lead_cast'] = cast_lst
            else:
                cast_lst = []

            if 'Production and Technical Credits' in table_html :
                table_crew = table
                for row in table_crew.select('tr'):
                    cols = row.select('td')
                    field_name = cols[2].text.replace('.','')
                    if field_name in single_movie_data.keys():
                        if type(single_movie_data[field_name]) == list:
                            field_value = cols[0].text
                            single_movie_data[field_name].append(field_value)
                        else:
                            field_value = cols[0].text
                            single_movie_data[field_name] = [single_movie_data[field_name]]
                            single_movie_data[field_name].append(field_value)
                    else:
                        single_movie_data[field_name] = cols[0].text
            else:
                table_crew = []

        movies_clean_v2.insert_one({'title': title,
                                'data': single_movie_data})
        # print(i,title)

        return None

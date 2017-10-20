# -*- coding: utf-8 -*-
"""
Take url, parse the html for specified table (adv or reg stats), and return dictionary of stats
"""
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup

def parse_html_table(table):
    n_columns = 0
    n_rows=0
    column_names = []
    
    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):
        
    # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)
            
            # Handle column names if we find them
        th_tags = row.find_all('th') 
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

            # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
         raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,
                index= range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
                    
            # Convert to float if possible
    for col in df:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass
            
    return df

def find_table_of_player(url, stat_table):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    #table #0 is regular stats, #2 is misc stats, #3 is advanced stats
    if (stat_table == 'reg'):
        tbl_nm = 0
    elif (stat_table == 'misc'):
        tbl_nm = 2
    elif (stat_table == 'adv'):
        tbl_nm = 3
    table = soup.find_all('table')[tbl_nm]
    df = parse_html_table(table)
    #df=df.astype(float)
    return df

def get_stats(url, stat_type, year = 'current'):
    df = find_table_of_player(url, stat_type)
    
    row = len(df.index)-2 #current year
    categories = []
    if (stat_type == 'adv'):
        categories = ['ORtg', 'TS%', 'eFG%', 'USG%', 'PER','DRtg', 'ORB%', 'DRB%', 'STL%', 'BLK%']
    elif (stat_type == 'reg'):
        categories = ['FG%', 'FGA', '3P%', '3PA','PTS', 'AST', 'TRB', 'MIN']
    stats = {}
    for cat in categories:
        if (cat in df.columns):
            stats[cat] = df[cat][row]
    return stats


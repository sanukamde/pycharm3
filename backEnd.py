import threading
from bs4 import BeautifulSoup
import requests
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


class GreenhouseGas(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.page_name = "https://www.esrl.noaa.gov/gmd/aggi/aggi.html"
        self.index = index
        self.year = []
        self.ele = []

    def scrape_page(self):
        page = requests.get(self.page_name)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find("table", {"class": "table table-bordered table-condensed table-striped table-header"})
        rows = table.find_all('tr')[2:]
        for row in rows[2:]:
            data = row.find_all('td')
            data = [x.text.strip() for x in data]
            if len(data) <= 0:
                continue
            self.year.append(int(data[0]))
            data_tuple = float(data[self.index])
            self.ele.append(data_tuple)
        return self.ele


class MySQLite:
    def __init__(self):
        self.table_connect = sqlite3.connect('greenhousegas.db')

    def build_SQLite_table(self):
        gas_table_create_query = '''CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, year INTEGER, 
        CO2 REAL, CH4 REAL, NO2 REAL, CFC12 REAL, CFC11 REAL, minor15 REAL); '''
        self.table_connect.execute(gas_table_create_query)

    def update_data_SQLite_table(self, thread_ls):
        id_count = 0
        insert_data_query = '''INSERT OR IGNORE INTO Database (id, year, CO2, CH4, NO2, CFC12, CFC11, minor15)
        VALUES (?,?,?,?,?,?,?,?) '''
        years = thread_ls[0].year
        for year in years:
            data_tuple = (id_count, int(year), float(thread_ls[0].ele[id_count]), float(thread_ls[1].ele[id_count]),
                          float(thread_ls[2].ele[id_count]), float(thread_ls[3].ele[id_count]),
                          float(thread_ls[4].ele[id_count]), float(thread_ls[5].ele[id_count]))
            id_count += 1
            self.table_connect.execute(insert_data_query, data_tuple)
        self.table_connect.commit()

    def graph_builder(self, count):
        df = pd.read_sql_query("SELECT id, year, CO2, CH4, NO2, CFC12, CFC11, minor15 from Database",
                               self.table_connect)
        X = df.iloc[:, 1].values.reshape(-1, 1)
        Y = df.iloc[:, count+2].values.reshape(-1, 1)
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        Y_pred = linear_regressor.predict(X)
        if count == 0:
            plt.ylabel('CO2')
        if count == 1:
            plt.ylabel('CH4')
        if count == 2:
            plt.ylabel('NO2')
        if count == 3:
            plt.ylabel('CFC12')
        if count == 4:
            plt.ylabel('CFC11')
        if count == 5:
            plt.ylabel('15-minor')
        plt.xlabel('Year')
        plt.scatter(X, Y, color='purple')
        plt.plot(X, Y_pred, color='red')
        plt.show()

    def close_SQLite_table(self):
        self.table_connect.close()



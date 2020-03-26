# Title: Stock Price App
# Purpose: To create an application to display stock price
# Created by: Saani Rawat
# Last modifed: 03/21/2020
# Input:
# 1. web_scraping_stock_data.py
# Output:
# Stock Price Application

from flask import Flask, render_template, request, redirect, url_for
import os
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Changing directory
# root = "/Users/saannidhyarawat/Desktop/Projects/TDI/TDI 12-day program/Milestone Project"
# os.chdir(root+"/code")

# Defining the app
app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        ticker = request.form['ticker_entry']
        print(ticker)

        source = requests.get(
            "https://finance.yahoo.com/quote/" + ticker + "/history?period1=1553126400&period2=1584748800&interval=1mo&filter=history&frequency=1mo").text

        soup = BeautifulSoup(source, "lxml")

        # From the entire page's html tags, taking tags specific to the date and adjusted close (stock price)
        stock = []
        date_len = len(soup.findAll("td", class_="Py(10px) Ta(start) Pend(10px)"))
        adj_close_len = len(soup.findAll("td", class_="Py(10px) Pstart(10px)"))

        for i, j in zip(range(0, date_len), range(4, adj_close_len, 6)):

            try:
                date = soup.findAll("td", class_="Py(10px) Ta(start) Pend(10px)")[i].text
            except Exception as e:
                date = None
            try:
                adj_close = soup.findAll("td", class_="Py(10px) Pstart(10px)")[j].text
            except Exception as e:
                adj_close = None
            ticker_col = ticker
            stock.append([date, ticker_col, adj_close])

        stock_df = pd.DataFrame(stock)
        stock_df = stock_df[::-1].reset_index(drop=True)

        data = [go.Scatter(x=stock_df[0], y=stock_df[2], mode='lines', name='graph')]
        fig = go.Figure(data=data, layout_title_text=ticker + " Stock Price over the past year")
        pyo.plot(fig, output_type="file", auto_open=False, filename=os.getcwd()+"/templates/TS_plot.html")

        return render_template("TS_plot.html")



# Running the app
if __name__== '__main__':
    app.debug = False
    app.run()




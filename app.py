import os
from flask import Flask, render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd



####################################################
### Lauch Flask and app settings
####################################################

app = Flask(__name__)




####################################################
### Flask routes
####################################################

@app.route('/')
def index():
    """Load the homepage"""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_formats():
    """That fetch and compare lists of formats + displays it in middle column"""

    if request.method == 'POST':

        soft_in = request.form['btn-in']
        soft_out = request.form['btn-out']

        # Read CSV and get the two columns we need, save them as clean lists
        data = pd.read_csv("data.csv", sep=';')
        df = pd.DataFrame(data, columns=[soft_out, soft_in])

        output_formats = [x for x in df[soft_out].tolist() if isinstance(x, str)]
        input_formats = [x for x in df[soft_in].tolist() if isinstance(x, str)]

        # Check for empty column and return error message if TRUE
        for col in df:            
            if df[col].isnull().sum() == len(df[col]):
                print("An error message because one of the columns is completely empty and that is: " + col)

        # Compare lists and keep common items
        common_formats = list()
        for items in output_formats:
            for numbers in input_formats:
                if items == numbers:
                    if items in common_formats:
                        None
                    else:
                        common_formats.append(items)

        # Output list in middle DIV
        if not common_formats:
            text = "There are no commmon formats."
        else:
            text = common_formats 
            
        return render_template('index.html', text = text)



if __name__ == "__main__":
    app.run()
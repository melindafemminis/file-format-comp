import os
from flask import Flask, render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import re
import csv
import os


####################################################
### Lauch Flask and app settings
####################################################

app = Flask(__name__)





####################################################
### Flask routes
####################################################



@app.route('/')
def index():

    """Render home page and dynamically creates buttons"""


    # Delete previous list of softwares if it exists
    if os.path.exists('software_list.csv'):
        os.remove('software_list.csv')
        print("The file: {} is deleted.".format('software_list.csv'))
    else:
        print("The file: {} does not exist.".format('software_file.csv'))


    # Create a list with all the softwares that are in data.csv and save it
    data = pd.read_csv("full_data.csv", sep=';')
    df = pd.DataFrame(data)
    buttons = list() 

    for col_name in df.columns:
        col_name = re.sub(r'(out|in)$', '', col_name).capitalize()
        if col_name not in buttons:
            buttons.append(col_name)

        with open('software_list.csv', 'w') as f: 
            write = csv.writer(f) 
            write.writerow(buttons) 
              
    # Render index.html and pass software list 
    return render_template('index.html', buttons=buttons)



@app.route('/', methods=['POST'])
def get_formats():

    """Fetch and compare lists of formats + displays it in middle column"""


    if request.method == 'POST':


        # Get chosen buttons value
        soft_in = request.form['btn-in'].lower()
        soft_out = request.form['btn-out'].lower()


        # Read CSV of software list and save as list
        soft_list = pd.read_csv("software_list.csv", sep=',')
        df_soft = pd.DataFrame(soft_list)
        buttons = [el for el in df_soft.columns]
        print(buttons)

        # Read CSV with file formats and get selected software file formats
        data = pd.read_csv("full_data.csv", sep=';')
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

        # If common item list is empty, return that there is no common format
        # else return common formats
        if not common_formats:
            text = "There are no commmon formats."
        else:
            text = common_formats 

        # Render index.html page with output text and button list to use in html with jinja   
        return render_template('index.html', text=text, buttons=buttons)



if __name__ == "__main__":
    app.run()

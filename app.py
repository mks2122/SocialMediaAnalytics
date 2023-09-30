from flask import Flask, render_template, request
import re,requests,csv,pandas
import googleapiclient.discovery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import gcpDeploymentFinalFinal as gcp




app = Flask(__name__,template_folder="./",static_folder="static")

# Define a route for the main page
@app.route('/')
def index():
    return render_template('intial.html')

# Define a route for each HTML file
@app.route('/home.html')
def html4():
    return render_template('home.html')


@app.route('/threads.html')
def html1():
    return render_template('threads.html')

@app.route('/youtube.html')
def html2():
    return render_template('youtube.html')

@app.route('/linkedin.html')
def html3():
    return render_template('linkedin.html')

# Define a route to handle the form submission
@app.route('/submit/', methods=['GET','POST'])
def submit():
    # Get the input from the form
    input = request.form.get('link')

    # Do something with the input
    print(input)

    # Return a success message
    return 'PLEASE GO TO THE YOUTUBE ANALYTICS'

@app.route('/submit/Youtube', methods=['GET','POST'])
def submitYout():
    # Get the input from the form
    input = request.form.get('link')

    #Analysing the youtube link
    return youtubeAna(input)


def getYtComment(id):
    
    #creating api necessity
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "<YOUR API KEY>"

    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    #creating a request
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=id,
        maxResults=100
    )
    response = request.execute()

    comments = []
    #scraping the comments
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append(
            
            comment['textDisplay']
        )

    return (comments)

def youtubeAna(lnk):
        #getting the watch id
        if 'watch?v' in lnk:
            print('single link')
            com = getYtComment(lnk.split("=")[-1])
        else:
            print("INVALID LINK")
            return "INVALID LINK"


        #creating the query for the analysis model
        def query(payload):
            response = requests.post(gcp.API_URL, headers=gcp.headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": com,
        })
        # print(output)
        header = ['label', 'score']
        #creating the csv file for the comments
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for row in output:
                for item in row:
                    writer.writerow([item['label'], item['score']])

        df = pd.read_csv('output.csv')
        
        #changing the labels
        def map_labels(label):
            if label == 'LABEL_0':
                return 'negative'
            elif label == 'LABEL_1':
                return 'neutral'
            elif label == 'LABEL_2':
                return 'positive'
        df['label'] = df['label'].map(map_labels)

        #getting the mean and plotting it
        label_means = df.groupby('label')['score'].mean()
        label_means.to_frame()
        label_means.plot.pie(autopct="%1.1f%%")
        plt.title("Pie Chart of Sentiment Label Counts")
        # plt.sav efig("plot.png")
        plt.show()
        return """<html><style> body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}</style><center><h1>Interrogate more and the data will confess!!!</h1></center></html>"""


if __name__ == '__main__':  
    app.run(debug=False)

from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

FILE = "attendance.csv"

@app.route('/')
def index():
    with open(FILE, 'r') as f:
        data = list(csv.reader(f))
    return render_template('index.html', data=data)

@app.route('/mark', methods=['POST'])
def mark():
    name = request.form['name']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, time])

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
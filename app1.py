from flask import Flask, render_template, request
from datetime import datetime

app1 = Flask(__name__)


@app1.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == "POST":
        file_name = request.form['timelogfile']
        try:
            with open(file_name, "r") as f:
                time_spent = 0
                for curser in f:
                    if curser.find("Time Log:") == 0:
                        continue
                    if 'am' not in curser.lower() and 'pm' not in curser.lower():
                        continue
                    start_time = datetime.strptime(curser.split('-')[0].strip()[-7:].lower().strip(), '%I:%M%p')
                    end_time = datetime.strptime(curser.split('-')[1][1:8].lower().strip(), '%I:%M%p')
                    time_diff = end_time - start_time
                    time_spent = time_spent + (time_diff.seconds / 60)

                return render_template('index.html',
                                       file_name=file_name.split('.')[0],
                                       result='{:02d} hours {:02d} minutes'.format(*divmod(int(time_spent), 60)))
        except FileNotFoundError:
            error = "Please Choose a Correct file"
            return render_template('index.html', file_not_found_error=error)


if __name__ == '__main__':
    app1.run(debug=True)

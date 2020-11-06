from models.models import (DescentCalculator, DescentForm)
from flask import Flask, render_template, redirect, request, url_for, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = "x"

# this text file will hold contents of calculations in a session
with open("session_data.txt", "w") as txtfile:
    txtfile.truncate(0)
    txtfile.close()


@app.route('/', methods=['GET', 'POST'])
def index():

    # form to get data
    form = DescentForm()

    if request.method == "POST":

        # get the data
        start_alt = form.alt_start.data
        dest_alt = form.alt_end.data
        kias = form.kias.data
        distance_nm = form.distance_nm.data

        # perform the calculation
        calc = DescentCalculator(
            start_alt=start_alt,
            dest_alt=dest_alt,
            kias=kias,
            distance_nm=distance_nm)
        calc.run()

        # add the data to the session textfile for use in the HTML table
        with open('session_data.txt', 'a') as txtfile:
            txtfile.write(
                f"{start_alt}, {dest_alt}, {kias}, {distance_nm}, {abs(int(calc.fpm_with_speed))}\n")

        return redirect(url_for('index'))

    # create list of data from session textfile for use in HTML table
    data_rows = []

    with open('session_data.txt', 'r') as txtfile:
        for line in txtfile.readlines():
            data_rows.append(line.replace('\n', '').split(','))
    
    data_rows.reverse()

    return render_template('index.html', form=form, rows=data_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

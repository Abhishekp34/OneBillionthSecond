from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        day = int(request.form.get('day'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        ampm = request.form.get('ampm')

        # Adjust hour based on AM/PM
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        birthdate = datetime(year, month, day, hour, minute)
        billionth_second = birthdate + timedelta(seconds=10**9)

        # Format billionth second as DD-MM-YYYY HH:MM
        formatted_billionth_second = billionth_second.strftime("%d-%m-%Y %H:%M")

        # Convert billionth second to a timestamp for JavaScript
        target_time = int(billionth_second.timestamp() * 1000)

        return render_template(
            "index.html",
            result=formatted_billionth_second,
            target_time=target_time
        )
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><p>Make sure all inputs are correct.</p>"

if __name__ == '__main__':
    app.run(debug=True)

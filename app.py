from flask import Flask, request, render_template
import logging
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


@app.route('/')
def home():
    return render_template('billionth_second_calculator.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Retrieve form data with validation
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        ampm = request.form.get('ampm')

        # Validate form fields
        if not all([day, month, year, hour, minute, ampm]):
            raise ValueError("All form fields are required.")

        day = int(day)
        month = int(month)
        year = int(year)
        hour = int(hour)
        minute = int(minute)

        # Validate the hour
        if hour < 1 or hour > 12:
            raise ValueError("Hour must be between 1 and 12.")

        # Convert to 24-hour format if necessary
        if ampm == 'PM' and hour != 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0

        # Create the birth datetime object with timezone
        birth_datetime = datetime(year, month, day, hour, minute, tzinfo=pytz.UTC)

        # Calculate the 1 billionth second
        billionth_second_date = birth_datetime + timedelta(seconds=10**9)

        # Calculate the age in seconds
        now = datetime.now(pytz.UTC)
        age_in_seconds = int((now - birth_datetime).total_seconds())

        return render_template(
            'billionth_second_calculator.html',
            result=billionth_second_date.strftime("%d-%m-%Y %H:%M"),
            target_time=int(billionth_second_date.timestamp() * 1000),
            birth_time=int(birth_datetime.timestamp() * 1000),
            age_in_seconds=age_in_seconds
        )
    except Exception as e:
        logging.exception("An error occurred during calculation.")
        return render_template(
            'billionth_second_calculator.html',
            details=str(e)
        )


if __name__ == '__main__':
    app.run(debug=True)

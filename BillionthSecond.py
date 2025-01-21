from flask import Flask, request, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1 Billionth Second Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #2c3e50; /* Darker background color */
            color: #ffffff;
        }
        .form-container {
            background: #34495e; /* Slightly lighter box color */
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h2 {
            margin-bottom: 20px;
            color: #ecf0f1; /* Light text color for better readability */
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .input-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: nowrap; /* Prevent wrapping */
        }
        .input-group input, .input-group select {
            width: 60px;  /* Adjust width for all fields */
            padding: 8px;
            font-size: 14px;
            text-align: center;
            border: 1px solid #95a5a6;
            border-radius: 6px;
        }
        .time-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        button {
            padding: 12px;
            font-size: 16px;
            background-color: #3498db; /* Button blue */
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 20px;
        }
        .reset {
            margin-top: 10px;
            text-decoration: underline;
            color: #3498db;
            cursor: pointer;
        }
        .reset:hover {
            color: #2980b9;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>1 Billionth Second Calculator</h2>
        <form action="/calculate" method="post">
            <div class="input-group">
                <input type="text" name="day" placeholder="DD" maxlength="2" required>
                <input type="text" name="month" placeholder="MM" maxlength="2" required>
                <input type="text" name="year" placeholder="YYYY" maxlength="4" required>
            </div>
            <div class="time-group">
                <input type="text" name="hour" placeholder="HH" maxlength="2" required>
                <input type="text" name="minute" placeholder="MM" maxlength="2" required>
                <select name="ampm">
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                </select>
            </div>
            <button type="submit">Calculate</button>
        </form>
        {% if result %}
        <div class="result">
            <h3>Your 1 billionth second is:</h3>
            <p>{{ result }}</p>
        </div>
        <a class="reset" href="/">Enter another date and time</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

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

        return render_template_string(HTML_TEMPLATE, result=billionth_second)
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><p>Make sure all inputs are correct.</p>"

if __name__ == '__main__':
    app.run(debug=True)

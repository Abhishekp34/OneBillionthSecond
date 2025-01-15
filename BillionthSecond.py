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
            background-color: #f4f4f4;
        }
        .form-container {
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h2 {
            margin-bottom: 20px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .input-group {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .input-group input, .input-group select {
            width: 60px;
            padding: 5px;
            font-size: 14px;
            text-align: center;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        select {
            width: 80px;
        }
        button {
            padding: 10px;
            font-size: 16px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
        }
        .reset {
            margin-top: 10px;
            text-decoration: underline;
            color: #007BFF;
            cursor: pointer;
        }
        .reset:hover {
            color: #0056b3;
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

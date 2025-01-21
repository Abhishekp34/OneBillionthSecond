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
            background-color: #2c3e50;
            color: #ffffff;
        }
        .form-container {
            background: #34495e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h2 {
            margin-bottom: 20px;
            color: #ecf0f1;
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
        }
        .input-group input, .input-group select {
            width: 60px;
            padding: 8px;
            font-size: 14px;
            text-align: center;
            border: 1px solid #95a5a6;
            border-radius: 6px;
        }
        button {
            padding: 12px;
            font-size: 16px;
            background-color: #3498db;
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
    <script>
        function startCountdown(targetTime) {
            function updateCountdown() {
                const now = new Date().getTime();
                const distance = targetTime - now;

                if (distance > 0) {
                    const years = Math.floor(distance / (1000 * 60 * 60 * 24 * 365));
                    const months = Math.floor((distance % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24 * 30));
                    const days = Math.floor((distance % (1000 * 60 * 60 * 24 * 30)) / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                    document.getElementById("countdown").innerText = 
                        `${years} years, ${months} months, ${days} days, ${hours} hours, ${minutes} minutes, and ${seconds} seconds`;
                } else {
                    document.getElementById("countdown").innerText = "Your 1 billionth second has already passed!";
                    clearInterval(timer);
                }
            }

            const timer = setInterval(updateCountdown, 1000);
            updateCountdown();
        }
    </script>
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
        {% if result and target_time %}
        <div class="result">
            <h3>Your 1 billionth second is:</h3>
            <p>{{ result }}</p>
            <h3>Time remaining (live):</h3>
            <p id="countdown"></p>
            <script>
                startCountdown({{ target_time }});
            </script>
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

        # Format billionth second as DD-MM-YYYY HH:MM
        formatted_billionth_second = billionth_second.strftime("%d-%m-%Y %H:%M")

        # Convert billionth second to a timestamp for JavaScript
        target_time = int(billionth_second.timestamp() * 1000)

        return render_template_string(HTML_TEMPLATE, result=formatted_billionth_second, target_time=target_time)
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><p>Make sure all inputs are correct.</p>"

if __name__ == '__main__':
    app.run(debug=True)

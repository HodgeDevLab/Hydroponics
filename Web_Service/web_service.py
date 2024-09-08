import pika
import logging
from flask import Flask, render_template_string, jsonify
import time
import re
import threading

app = Flask(__name__)

# Global variable to store the latest temperature
latest_temperature = 50  # Default starting temperature in Celsius

# Function to consume messages from RabbitMQ
def consume_temperature_from_rabbitmq():
    global latest_temperature
    try:
        # Connect to RabbitMQ
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
        channel = connection.channel()

        # Declare the queue (make sure the queue exists)
        channel.queue_declare(queue='cpu_temperature')

        # Callback to update the latest_temperature
        def callback(ch, method, properties, body):
            global latest_temperature
            try:
                # Assume the message comes in the format "CPU Temperature: 50.4°C"
                message = body.decode()  # Decode the message from bytes to string
                # Use a regular expression to extract the numeric temperature value
                temperature_match = re.search(r"([-+]?\d*\.\d+|\d+)", message)  # Regex to match float or integer
                if temperature_match:
                    latest_temperature = float(temperature_match.group())  # Convert the extracted temperature to float
                    logging.info(f" [x] Received {latest_temperature}°C")
                else:
                    logging.warning(f" [!] Could not extract temperature from message: {message}")
            except ValueError as e:
                logging.error(f"Failed to process temperature: {e}")

        # Consume messages from the queue
        channel.basic_consume(queue='cpu_temperature', on_message_callback=callback, auto_ack=True)

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection to RabbitMQ failed: {e}")
        time.sleep(5)  # Wait before retrying
        consume_temperature_from_rabbitmq()  # Retry connection


# Flask route to serve the webpage with JavaScript for dynamic updates
@app.route('/')
def display_temperature_page():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CPU Temperature Monitor</title>
            <style>
                body {
                    background-color: #121212;
                    color: #e0e0e0;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                h1 {
                    margin-bottom: 30px;
                }
                #chart-container {
                    width: 80%;
                    height: 400px;
                    margin: 0 auto;
                }
                #temperature-value {
                    font-size: 36px;
                    margin-top: 20px;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                var chart;
                var timeLabels = [];
                var temperatureData = [];

                // Function to fetch temperature and update the graph
                function fetchTemperature() {
                    fetch('/temperature')
                    .then(response => response.json())
                    .then(data => {
                        var temperature = data.temperature;
                        var currentTime = new Date().toLocaleTimeString();

                        // Push data to arrays
                        timeLabels.push(currentTime);
                        temperatureData.push(temperature);

                        // Keep only the last 20 data points
                        if (timeLabels.length > 20) {
                            timeLabels.shift();
                            temperatureData.shift();
                        }

                        // Update the chart
                        chart.data.labels = timeLabels;
                        chart.data.datasets[0].data = temperatureData;

                        // Change line color based on temperature thresholds for Raspberry Pi
                        var lineColor = temperature > 80 ? '#FF0000' : temperature > 60 ? '#FFFF00' : '#00FF00'; // Red > 80°C, Yellow > 60°C, Green otherwise
                        chart.data.datasets[0].borderColor = lineColor;
                        chart.data.datasets[0].backgroundColor = lineColor;

                        chart.update();

                        // Update the numeric temperature display
                        document.getElementById('temperature-value').innerText = temperature.toFixed(1) + "°C";
                    })
                    .catch(error => console.log('Error fetching temperature:', error));
                }

                window.onload = function() {
                    var ctx = document.getElementById('temperatureChart').getContext('2d');
                    chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: timeLabels,
                            datasets: [{
                                label: 'CPU Temperature (°C)',
                                data: temperatureData,
                                borderColor: '#00FF00',
                                backgroundColor: '#00FF00',
                                fill: false,
                                borderWidth: 2,
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Time',
                                        color: '#e0e0e0'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Temperature (°C)',
                                        color: '#e0e0e0'
                                    },
                                    min: 30,  // Lower limit for temperature
                                    max: 100  // Upper limit for temperature
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: '#e0e0e0'
                                    }
                                }
                            }
                        }
                    });

                    // Update chart every 5 seconds
                    setInterval(fetchTemperature, 5000);
                }
            </script>
        </head>
        <body>
            <h1>CPU Temperature Monitor (°C)</h1>
            <div id="chart-container">
                <canvas id="temperatureChart"></canvas>
            </div>
            <div id="temperature-value">50.0°C</div> <!-- Default starting value -->
        </body>
        </html>
    ''')

# API endpoint to return the latest temperature as JSON
@app.route('/temperature')
def get_temperature():
    global latest_temperature
    return jsonify({'temperature': latest_temperature})

# Main method to start both the web server and RabbitMQ consumer
if __name__ == "__main__":
    logging.info("~~~~~ Started Main")
    # Start a separate thread for the RabbitMQ consumer
    consumer_thread = threading.Thread(target=consume_temperature_from_rabbitmq, daemon=True)
    consumer_thread.start()

    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000)
    logging.info("~~~~~ Ended Main")

import pika
import time

def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            celsius_temp = int(f.read()) / 1000  # Convert from millidegree Celsius to Celsius
        fahrenheit_temp = (celsius_temp * 9/5) + 32
        return fahrenheit_temp
    except FileNotFoundError:
        return "Could not read CPU temperature. Check file permissions or path."

def publish_temperature_to_rabbitmq(temp):
    # Connection parameters (replace with appropriate values)
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
    channel = connection.channel()

    # Declare a queue (you can change the queue name)
    channel.queue_declare(queue='cpu_temperature')

    # Publish the message (CPU temperature)
    message = f"CPU Temperature: {temp}°F"
    channel.basic_publish(exchange='', routing_key='cpu_temperature', body=message)
    print(f" [x] Sent {message}")

    connection.close()

# Main loop: get temperature and publish it every 5 seconds
while True:
    temperature = get_cpu_temperature()
    publish_temperature_to_rabbitmq(temperature)
    time.sleep(5)
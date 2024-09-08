#!/bin/bash

cp /var/lib/rabbitmq/.erlang.cookie /root/.erlang.cookie
chmod 400 /root/.erlang.cookie

# Wait until RabbitMQ is fully up by checking its status in a loop
while true; do
  rabbitmqctl status
  if [ $? -eq 0 ]; then
    echo "RabbitMQ is running!"
    break
  fi
  echo "Waiting for RabbitMQ to start..."
  sleep 5
done

# Create a producer user with write and configure access (so they can create queues)
rabbitmqctl add_user producer producer_password
rabbitmqctl set_permissions -p / producer ".*" ".*" ""

# Create a consumer user with read-only access to the default virtual host
rabbitmqctl add_user consumer consumer_password
rabbitmqctl set_permissions -p / consumer "" "" ".*"

# Set tags for users (e.g., admin for default user)
rabbitmqctl set_user_tags user administrator
rabbitmqctl set_user_tags producer none
rabbitmqctl set_user_tags consumer none

# Optional: Disable guest user
rabbitmqctl delete_user guest

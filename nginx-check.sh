#!/bin/bash

# Threshold for load balancing (adjust as needed)
LOAD_THRESHOLD=2.0  # Adjust based on your server's load average

while true; do
    # Get server's load average
    CURRENT_LOAD=$(uptime | awk -F'[a-z]:' '{ print $2 }' | awk -F',' '{ print $1 }' | sed 's/^[ \t]*//;s/[ \t]*$//')

    # Compare load with the threshold
    if (( $(echo "$CURRENT_LOAD > $LOAD_THRESHOLD" | bc -l) )); then
        # Server load is high, take action (e.g., deploy GCP container)
        echo "Server load is high ($CURRENT_LOAD), taking action..."
        
        # Add your GCP container deployment logic here
        
        # Example: Spin a new GCP container with 100GB space
        gcloud compute instances create new-instance --image-family=ubuntu-1804-lts --image-project=ubuntu-os-cloud --boot-disk-size=100GB
        
        # Example: Deploy Kubernetes cluster as prod-4
        gcloud container clusters create prod-4 --num-nodes=3 --machine-type=n1-standard-2
        
        echo "Action completed. Sleeping for 1 hour..."
        sleep 1h
    else
        echo "Server load is within the threshold ($CURRENT_LOAD). Sleeping for 10 minutes..."
        sleep 10m
    fi
done


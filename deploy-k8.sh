# Make the script executable
chmod +x nginx-check.sh

# Create the systemd service file
sudo cp nginx-check.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Start and enable the service
sudo systemctl start nginx-check.service
sudo systemctl enable nginx-check.service

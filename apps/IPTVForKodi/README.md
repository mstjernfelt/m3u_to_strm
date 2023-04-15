pip install flask
sudo nano /etc/systemd/system/m3u_2_strm.service

[Unit]
Description=m3u_2_strm loggviewer

[Service]
User=yourusername
WorkingDirectory=/path/to/your/flask/app
ExecStart=python3 /path/to/your/flask/app/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl status myapp
sudo systemctl enable myapp
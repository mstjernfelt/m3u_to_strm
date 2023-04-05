# m3u to strm

Convert m3u playlist to strm in order to view content in Kodi.

## Execute manually
```
sudo python3.7 main.py --m3u_file "myIPTVURL" --output_dir "myOutputDir" --provider "myProvider" --generate_groups
```

## Schedule
run.sh file will run at 8:00 AM and 8:00 PM every day.

```
crontab -e
```

```
0 8,20 * * * /path/to/python /path/to/your/script.py
```

## Logg viewer

Setup m3u 2 strm logg viewer

```
pip install flask
```
```
sudo nano /etc/systemd/system/m3u_2_strm.service
```

```
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
```
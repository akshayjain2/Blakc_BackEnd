# Blakc 
 Blakc is a messaging program designed specifically for the office, but has also been adopted for personal use.

>Pre requirment

1. Mongodb
2. Python3

> Installation of MongoDB

	curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
	sudo apt update
	sudo apt install mongodb-org
	sudo systemctl start mongod.service
	sudo systemctl status mongod
	sudo systemctl enable mongod




>Install Package

	apt-get install python3-venv 
	python3 -m venv venv 
	source venv/bin/activate
	pip3 install -r requirement.txt

> In case of error 
	pip3 install --upgrade pip

>execute command
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver 0.0.0.0:8000


## Make Project More scalable 
	sudo nano /etc/systemd/system/gunicorn.service

>EDIT IT

	[Unit]
	Description=stub gunicorn service
	After=network.target
	StartLimitIntervalSec=0
	[Service]
	WorkingDirectory=<Working location>
	Type=simple
	Restart=always
	RestartSec=1
	User=root
	ExecStart=<working location>/venv/bin/gunicorn --env DJANGO_SETTINGS_MODULE=stub.settings.prod  --access-logfile - --workers 3 --bind 0.0.0.0:5256 stub.wsgi:application
	[Install]
	WantedBy=multi-user.target

>Now start the service and enable it 

	sudo systemctl start gunicorn
	sudo systemctl enable gunicorn
	sudo systemctl status gunicorn




## References

https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04-source
https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-linux/

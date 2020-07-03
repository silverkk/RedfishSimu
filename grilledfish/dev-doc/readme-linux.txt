you better check docker first

	1. Install python3 on ubuntu, and check the version by: python3 --version
	2. Install the pip3
	sudo apt install -y python3-pip
	3. Install other packages:
	sudo apt install build-essential libssl-dev libffi-dev python3-dev
	4. Setup virtualenv
	sudo apt install -y python3-venv
	5. Create the virtual environment
		 mkdir environments 
		 cd environments
		 python3 -m venv redfish_env
		 source redfish_env/bin/activate
	Please ref "https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-18-04-server" for more details
	
	6. After redfish_env activated, install django( pip support proxy by "pip install --proxy http://child-prc.intel.com:913 Django"):
		(redfish_env) allen@ubu18-auto22:~/work/pyenvs$ pip install Django 
	Make sure Django is good:
		python -m django --version
	7. Django in vs code:
	
	8. Run the django check if django is good: python manage.py runserver 0.0.0.0:8000, then open browser and vistor http://127.0.0.1:8000
	9. Install uwsgi:
		a. First install wheel: pip install wheel --proxy https_proxy="http://child-prc.intel.com:913"
		b. Install uwsgi: pip install uwsgi --proxy https_proxy="http://child-prc.intel.com:913"
	10. Start uwsgi: navigate to the grilledfish directory,  then run: uwsgi --ini uwsgi.ini
	11. Install and config nginx:
		a. apt-get install nginx
		b. Config the nginx using https and uwsgi:
			i. sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
			ii. sudo vim /etc/nginx/snippets/self-signed.conf, add the following line:
			ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
			ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
			iii. Config nginx using SSL
			First backup the old config: 
			sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
			Then copy our nginx config file to /etc:
			Sudo cp ./nginx/default /etc/nginx/sites-available/default
			Then update file /etc/nginx/sites-available/default's last line 
			"uwsgi_pass     unix:/home/allen/work/DCM/DCMUtility/Main/Redfish_Emulators/grilledfish/grilledfish/grilledfish.sock;" 
			to your path
			iv. Restart the nginx: sudo service nginx restart
			
			
Debug using stunnel:
DCM SDK only allow https, so during development, we have to wrapper the https into our django server.
	1. Install stunnel: apt-get install stunnel, and using the following cmd to generate the cert:
		openssl req -new -x509 -days 365 -nodes -out stunnel.pem -keyout stunnel.pem
	2. Navigate to our simulator folder, and start stunnel by: sudo  ./launch_stunnel.sh
	3. Start django in vscode.
	4. Pls ref:
	https://stackoverflow.com/questions/8023126/how-can-i-test-https-connections-with-django-as-easily-as-i-can-non-https-connec
Ref:


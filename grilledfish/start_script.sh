#!/bin/bash
#/bin/bash
echo "starting......"
cd /grilledfish/grilledfish
#nginx
service openresty start
echo "nginx*(openresty) started"

if [ -d /ipmi_simulator ]; then 
    uwsgi --ini uwsgi.ini --daemonize /var/log/grilledfish_uwsgi.log
	echo "IPMI simulator found, try to start it"
	cd /ipmi_simulator/linux/
	./startSimulator.sh
else
    uwsgi --ini uwsgi.ini
	echo "IPMI simulator not found. we are done!"
    #while true; do sleep 1000; done
fi




Quick start using exist config files:
	1. Download the python installer, then install python to c:/python37
	2. Install Django using pip:  
		pip install django --proxy http://child-prc.intel.com:913
	Make sure Django is good:
		python -m django --version
	
	3. Copy the simulator folder "Redfish_Emulators/grilledfish/grilledfish/" to "C:\rfsimulator\", navigate to this folder, and run the django check if django is good: python manage.py runserver 0.0.0.0:8000, then open browser and vistor http://127.0.0.1:8000
	4. Unzip Apache to "C:\rfsimulator\Apache24", and copy files under windows\conf to "C:\rfsimulator\Apache24\conf",
	5. Install mod_wsgi: pip install windows\mod_wsgi-4.5.24+ap24vc14-cp37-cp37m-win_amd64.whl
	6. navigate to C:\rfsimulator\Apache24\bin, start httpd



Install and setup on windows
	1. Download the python installer, then install python to c:/python37
	2. Install Django using pip:  
		pip install Django --proxy https_proxy="http://child-prc.intel.com:913"
	Make sure Django is good:
		python -m django --version
	
	3. Copy the simulator code to "C:\rfsimulator\grilledfish", navigate to this folder, and run the django check if django is good: python manage.py runserver 0.0.0.0:8000, then open browser and vistor http://127.0.0.1:8000
	4. Unzip Apache to "C:\rfsimulator\Apache24", and update "C:\rfsimulator\Apache24\conf\httpd.conf",
		a.  change SRVROOT to "C:/rfsimulator/Apache24"
		b. Add "ExecCGI" to "Options" directive:
		Locate the following line:
		Options Indexes FollowSymLinks
		...and append "ExecCGI":
		Options Indexes FollowSymLinks ExecCGI
		...this tells Apache that CGI/Perl scripts are allowed outside of the cgi-bin directory
		c. Locate and uncomment the following line: (by removing the # symbol from the start of the line)
		AddHandler cgi-script .cgi
		...and also add the following line:
		AddHandler cgi-script .pl
		...These two lines tell Apache how to handle .cgi/.pl files (i.e. execute them rather than present them to as text to a web browser)
		d. Add the following line to the end of the httpd.conf file:
		ScriptInterpreterSource Registry
		...this allows Apache to ignore the very first line of .cgi/.pl files which direct Apache to the install location of Perl, and instead determine the location of Perl from the Windows Registry
		
	5. Open cmd windows and navigate to "C:\rfsimulator\Apache24\bin", then start Apache by run "httpd.exe". 
	open your web browser and navigate to http://127.0.0.1
	If Apache is running, you should see the words "It works!" displayed in your browser
	6. Install mod_wsgi: pip install C:\rfsimulator\mod_wsgi-4.5.24+ap24vc14-cp37-cp37m-win_amd64.whl
	7. Run mod_wsgi-express module-config, make sure you get the following lines:
	LoadFile "c:/python37/python37.dll"
	LoadModule wsgi_module "c:/python37/lib/site-packages/mod_wsgi/server/mod_wsgi.cp37-win_amd64.pyd"
	WSGIPythonHome "c:/python37"
	8. Update httpd.conf again, add the following lines:
	LoadFile "c:/python37/python37.dll"
	LoadModule wsgi_module "c:/python37/lib/site-packages/mod_wsgi/server/mod_wsgi.cp37-win_amd64.pyd"
	WSGIPythonHome "c:/python37"
	
	WSGIScriptAlias / C:/rfsimulator/grilledfish/grilledfish/wsgi.py
	
	WSGIPythonPath C:/rfsimulator/grilledfish
	
	<Directory C:/rfsimulator/grilledfish/grilledfish>
	    <Files wsgi.py>
	        Require all granted
	    </Files>
	</Directory>
	
	9. Enable SSL for apache:
		a. Uncomment line:
			i. LoadModule ssl_module modules/mod_ssl.so
			ii. Include conf/extra/httpd-ssl.conf
			iii. LoadModule proxy_module modules/mod_proxy.so
			iv. LoadModule proxy_http_module modules/mod_proxy_http.so
	10.start httpd

https://mid.as/kb/00143/install-configure-apache-on-windows#download-apache
https://www.jianshu.com/p/598d8b5fbee6
https://blog.csdn.net/weixin_40754816/article/details/80955817

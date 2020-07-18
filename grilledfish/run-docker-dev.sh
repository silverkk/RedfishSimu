docker run -p 443:443 -v $PWD/grilledfish:/grilledfish/grilledfish -v $PWD/docker/nginx/nginx.conf:/etc/nginx/nginx.conf -v $PWD/docker/nginx/default:/etc/nginx/sites-available/default grilledfish

docker run -it --network host -p 443:443 \
    -v $PWD/grilledfish:/grilledfish/grilledfish \
    -v $PWD/docker/nginx/nginx.conf:/etc/nginx/nginx.conf \
    -v $PWD/docker/nginx/default:/etc/nginx/sites-available/default \
    -v $PWD/../Simulator/installer/share/conf:/ipmi_simulator/share/conf \
    -v $PWD/../Simulator/installer/share/simulator.jar:/ipmi_simulator/share/simulator.jar \
    grilledfish

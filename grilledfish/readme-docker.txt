redfish standalone mode
    1. add ip address to your host machine, then update grilledfish/grilledfish.json for your simulator config
    2. build the docker image: 
        docker build -t grilledfish .
    3. start the simulator:
        docker run -p 443:443 grilledfish

combined mode:
    in this mode, the docker image will contains both redfish simulator and ipmi simulator.
    1. add ip address to your host machine, then update grilledfish/grilledfish.json 
       for your simulator config, you don't need to update the ipmi config file, it will
       be generated during the docker image building process.
    2. build the docker image by run the following script: 
        build-full.sh
    3. start the simulator:
        docker run -it --network host grilledfish

To monitor the performance of nginx:
    we create a tool that could analyse the ngnix access.log file, to calc the performance:
        python tools/calc_resp_time.py path-to-nginx-access.log
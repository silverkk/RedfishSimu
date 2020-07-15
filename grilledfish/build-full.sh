#/bin/bash
ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
dir_name=$(dirname $ABSOLUTE_PATH)
#echo "The scripth installer running at $dir_name"

docker_context_path="${dir_name}/.."
echo "docker context path is: $docker_context_path"

cd ${docker_context_path}

grilledfish_path="grilledfish"
docker_file_path="${grilledfish_path}/UnifiedEnv.Docerfile"
#ipmi_simulator_path="Simulator/installer"
ipmi_simulator_path="Simulator/installer"

echo "ipmi_simulator_path is: $ipmi_simulator_path"
if [ -d ${ipmi_simulator_path} ]; then 
	echo "ipmi simulator located."
else
	echo "ipmi simulator not found. exit!"
	exit -1 
fi
ipmi_simu_conf="${ipmi_simulator_path}/share/conf/simulatorcfg.xml"
ipmi_simu_conf_gen="${ipmi_simulator_path}/share/conf/simulatorcfg_g.xml"

echo "grilledfish_path is: $grilledfish_path"
if [ -d ${grilledfish_path} ]; then 
	echo "grilledfish simulator located."
else
	echo "grilledfish simulator not found. exit!"
	exit -1 
fi
gf_simu_conf="${grilledfish_path}/grilledfish/grilledfish.json"


python ${grilledfish_path}/docker/config_gen.py ${gf_simu_conf} ${ipmi_simu_conf} ${ipmi_simu_conf_gen}

DOCKER_BUILDKIT=0 docker build -t grilledfish --build-arg grilledfish_path=${grilledfish_path} --build-arg ipmi_simu_path=${ipmi_simulator_path} -f ${docker_file_path} .
#DOCKER_BUILDKIT=1 docker build --build-arg grilledfish_path=${grilledfish_path} -f ${docker_file_path} .
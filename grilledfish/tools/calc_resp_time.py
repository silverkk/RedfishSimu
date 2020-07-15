import sys
import shlex

if len(sys.argv) < 1:
    print("you missed the nginx access log file")
filepath = sys.argv[1]

# the log file is like:
#"15/Jul/2020:06:12:54 +0000" client=192.168.1.1 method=GET request="GET /favicon.ico HTTP/1.1" request_length=501 status=500 bytes_sent=83881 body_bytes_sent=
#83638 referer=https://192.168.1.1/redfish/control/perf user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116
# Safari/537.36" upstream_addr=unix:/grilledfish/grilledfish/grilledfish.sock upstream_status=500 request_time=0.146 upstream_response_time=0.148 upstream_conn
#ect_time=0.000 upstream_header_time=0.148

total_request_time = 0.0
total_request_count = 0
max_request_time = 0.0
#request_time is the total process time for a request
with open(filepath) as fp:
   line = fp.readline()
   while line:
        #print("Line {}: {}".format(cnt, line.strip()))
        result = shlex.split(line)
        if len(result) > 15:
            request_time_str = result[12]
            #print(request_time_str)
            #print(*result, sep = "\n")
            #print("------------------\n") 
            request_time = float(request_time_str.split('=')[1])
            total_request_time = total_request_time + request_time
            total_request_count = total_request_count + 1
            if max_request_time < request_time:
                max_request_time = request_time
        line = fp.readline()


total_average_response_time = total_request_time/total_request_count
responseContent = "totalResTime: {0}, totalRequestCount: {1}, averageResTime:{2}, maxResTime:{3}\n"
print(responseContent.format(total_request_time, total_request_count, total_average_response_time, max_request_time))
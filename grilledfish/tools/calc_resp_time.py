import sys
import json
import mysql.connector

if len(sys.argv) < 7:
    print("params: nginx-log-file mysql-host mysql-username mysql-password database table-name")
    exit()
filepath = sys.argv[1]
dbhost = sys.argv[2]
dbuser = sys.argv[3]
dbpassword = sys.argv[4]
database=sys.argv[5]
dbtable = sys.argv[6]

mydb = mysql.connector.connect(
  host=dbhost,
  user=dbuser,
  password=dbpassword,
  database=database
)

mycursor = mydb.cursor()

sql = """
INSERT INTO {} (time, client, host, method, uri, path, request_length, 
status, bytes_sent, upstream_status, request_time, upstream_response_time, 
upstream_connect_time, upstream_header_time) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(dbtable)



# each line of the log file is a json string, refer to the sample-nginx-access.log
total_request_time = 0.0
max_request_time = 0.0
total_request_count = 0
with open(filepath) as fp:
   line = fp.readline()
   while line:
        #print("number: {}, Line: {}".format(total_request_count, line.strip()))
        if total_request_count%1000 == 0:
          print("number: {}, Line: {}".format(total_request_count, line.strip())) 
        try:
          access_item = json.loads(line)
          total_request_time = total_request_time + access_item['request_time']
          total_request_count = total_request_count + 1
          if max_request_time < access_item['request_time']:
              max_request_time = access_item['request_time']

          val = (
            access_item['time'], 
            access_item['client'], 
            access_item['host'], 
            access_item['method'], 
            access_item['uri'], 
            access_item['path'], 
            access_item['request_length'], 
            access_item['status'],
            access_item['bytes_sent'], 
            access_item['upstream_status'], 
            access_item['request_time'], 
            access_item['upstream_response_time'],
            access_item['upstream_connect_time'],
            access_item['upstream_header_time']
          )
          mycursor.execute(sql, val)
        except json.JSONDecodeError:
          print("number: {}, Line: {}".format(total_request_count, line.strip()))       

        line = fp.readline()

mydb.commit()
print("{} records writes into mysql".format(total_request_count))

total_average_response_time = total_request_time/total_request_count
responseContent = "ngnix performance summary: totalResTime: {0}, totalRequestCount: {1}, averageResTime:{2}, maxResTime:{3}\n"
print(responseContent.format(total_request_time, total_request_count, total_average_response_time, max_request_time))
import psycopg2
from datetime import datetime, timedelta

connection = None
cursor = None

try:
   connection = psycopg2.connect(user="dcmdba",
                                  password="intel_123",
                                  host="127.0.0.1",
                                  port="6443",
                                  database="dcm_console")
   cursor = connection.cursor()

   postgres_insert_query = """ INSERT INTO \"T_Event\" (\"severity\", \"entityName\", \"assetTag\", \"eventType\", \"description\",
   \"timestamp\", \"entityId\", \"notificationId\", \"customEventId\", \"currentValue\", \"condition\", \"threshold\") VALUES 
   (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   records_per_5_minutes = 8493

   for x in range(records_per_5_minutes):
       now = datetime.now()
       record_to_insert = (3, "Entity Name", "Asset tag", "Event type", "Description", now.strftime("%Y-%m-%d, %H:%M:%S"), 1, -1, -1, -1, -1, -1)
       cursor.execute(postgres_insert_query, record_to_insert)

   
   records_per_5_minutes = 45
   now = datetime.now()
   now = now + timedelta(seconds=1)
   for x in range(records_per_5_minutes):       
       record_to_insert = (3, "Entity Name", "Asset tag", "Event type", "Description", now.strftime("%Y-%m-%d, %H:%M:%S"), 1, -1, -1, -1, -1, -1)
       cursor.execute(postgres_insert_query, record_to_insert)
   connection.commit()
   count = cursor.rowcount
   print (count, "Record inserted successfully into event table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into event table", error)
    else:
        print("Failed to connect to db", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
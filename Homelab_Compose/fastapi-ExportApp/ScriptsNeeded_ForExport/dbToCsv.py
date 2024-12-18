import mariadb
import sys
import csv
import os

# Database connection parameters
config = {
    'user': 'cole',
    'password': 'aaa1aaa',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'hass_db'
}

# Retrieve time parameters from environment variables
time_begin = float(os.getenv('TIME_BEGIN'))
time_end = float(os.getenv('TIME_END'))

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(**config)
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# SQL query with parameters
sql = """
SELECT
  sm.entity_id,
  FROM_UNIXTIME(s.last_reported_ts, '%Y-%m-%d %H:%i:%s.%f') AS UTC_Last_Reported,
  s.state,
  sa.shared_attrs,
  et.event_type,
  e.time_fired_ts,
  s.last_changed_ts,
  s.last_updated_ts,
  s.old_state_id,
  s.attributes_id,
  e.event_id,
  e.data_id,
  s.state_id
FROM 
  events e
JOIN 
  event_types et ON e.event_type_id = et.event_type_id
RIGHT JOIN
  states s ON s.context_id_bin = e.context_id_bin
JOIN
  states_meta sm ON s.metadata_id = sm.metadata_id
JOIN
  state_attributes sa ON s.attributes_id = sa.attributes_id
WHERE 
  s.last_reported_ts > %s AND s.last_reported_ts < %s
ORDER BY 
  s.last_reported_ts DESC;
"""

try:
    cursor.execute(sql, (time_begin, time_end))  # Using parameterized query for security
    results = cursor.fetchall()
    
    # Define the path for the CSV file in the EXPORTS directory
    csv_path = os.path.join('/EXPORTS', 'output.csv')
    
    # Write results to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write headers
        csvwriter.writerow([i[0] for i in cursor.description])  # This line gets column names
        # Write data
        csvwriter.writerows(results)

    print("Data has been written to 'output.csv'.")
except mariadb.Error as e:
    print(f"Error executing SQL query: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

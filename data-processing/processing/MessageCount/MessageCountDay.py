import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from configparser import ConfigParser # Used for reading config file

config = ConfigParser()
config.read('../config.conf')

user        = config.get('database', 'user')
password    = config.get('database', 'password')
host        = config.get('database', 'host')
database    = config.get('database', 'database')

cnx = mysql.connector.connect(user=user, password=password,
                              host=host,
                              database=database)

cursor = cnx.cursor()
query = ("christianclausen_dk_db2.MessageCount") # Requires that the DB has installed the stored procedure sp_MessageCount.sql
cursor.callproc(query, (1585605600000, 7)) # Call the stored procedure on the MySQL DB with the given parameters
                                            # 1st parameter is the day in millis since 1970 to start counting messages
                                            # 2nd parameter is amount of days to calculate for

counts = []
#bins = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"] # Must match with the Number of days set in the stored procedure
bins = []

for result in cursor.stored_results(): # The stored_results yield only one result in this case which represents the whole table returned from the stored procedure
    for (DayStart, DayEnd, MessageCount) in result.fetchall(): # Process each row
        print(str(DayStart) + ", " + str(DayEnd) + ", " + str(MessageCount))
        counts.append(MessageCount)
        dt_start = datetime.fromtimestamp(DayStart/1000)  # fromtimestamp() can only handle seconds and not milliseconds.
        bins.append(str(dt_start))

cursor.close()
cnx.close()

plt.figure(figsize=[6, 6])
plt.bar(bins, counts)
plt.ylabel("Message Count")
plt.xlabel("Day")
plt.title("Messages Received / Day")
plt.xticks(rotation=45)
plt.savefig("Plots/MessageCountDays.svg", bbox_inches = "tight") # 'tight' makes room for x-axis labels
plt.show()  # Must be called last since this clears the figure, resulting in a white svg.

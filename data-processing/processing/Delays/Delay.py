import mysql.connector
from datetime import datetime
import numpy
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

days = [1585605600000, 1585692000000, 1585778400000, 1585864800000, 1585951200000, 1586037600000, 1586124000000]
day = 0
query = ("SELECT TransmissionsCounter, TimeStampReceived FROM Messages "
         "WHERE TimeStampReceived > %s AND TimeStampReceived < %s ORDER BY TransmissionsCounter")
cursor.execute(query, (days[day], days[day+1]))

messagesDelays = []              # List of delays for each message
previousMessage = ()             # The message that was last processed
processedMessagesCounter = 0     # Number of processed messages
outlierThreshold = 10000
outliers = []

#
# Process messages
#
for (TransmissionsCounter, TimeStampReceived) in cursor:
    # Skip first message, since we can't calculate delay for this
    if processedMessagesCounter == 0:
        previousMessage = (TransmissionsCounter, TimeStampReceived)
        processedMessagesCounter += 1
        continue

    delay = TimeStampReceived - previousMessage[1]
    if delay < outlierThreshold:
        messagesDelays.append(delay)
    else:
        outliers.append(delay)

    previousMessage = (TransmissionsCounter, TimeStampReceived)
    processedMessagesCounter += 1

cursor.close()
cnx.close()

print("##### Statistics #####")
processedMessagesCounter += 1  # Add one, since we start counting from zero
print("Number of processed messages: {}".format(processedMessagesCounter))
print("Avg delay: {}".format(numpy.average(messagesDelays)))
print("Std delay: {}".format(numpy.std(messagesDelays)))
print("Median delay: {}".format(numpy.median(messagesDelays)))
print("Min delay: {}".format(numpy.min(messagesDelays)))
print("Max delay: {}".format(numpy.max(messagesDelays)))
print("Outliers: {}".format(str(len(outliers))))
print(outliers)

plt.figure(figsize=[6, 6])
plt.ylabel("Message Count")
plt.xlabel("Delay [ms]")
plt.title("Day " + str(day+1) + " - Message delay")
plt.xticks(rotation=45)
axes = plt.gca() # Get current axes
axes.set_ylim([0,7200])
axes.set_xlim([0,10000])
plt.hist(messagesDelays, bins=50)
plt.savefig("Plots/MessageDelay_" + str(day) + ".svg", bbox_inches = "tight") # 'tight' makes room for x-axis labels
plt.show()  # Must be called last since this clears the figure, resulting in a white svg.
import mysql.connector
from datetime import datetime
from configparser import ConfigParser # Used for reading config file

config = ConfigParser()
config.read('config.conf')

user        = config.get('database', 'user')
password    = config.get('database', 'password')
host        = config.get('database', 'host')
database    = config.get('database', 'database')

cnx = mysql.connector.connect(user=user, password=password,
                              host=host,
                              database=database)

cursor = cnx.cursor()
query = ("SELECT TransmissionsCounter, TimeStampSent, TimeStampReceived FROM Messages "
         "ORDER BY TransmissionsCounter")
cursor.execute(query)

expectedTransmissionCounter = 0  # The expected message transmission counter
lostMessagesCounter = 0          # Amount of messages that was lost
lostMessagesTimeIntervals = []   # List of intervals when messages was lost
previousMessage = ()             # The message that was last processed

#
# Process lost messages
#
for (TransmissionsCounter, TimeStampSent, TimeStampReceived) in cursor:
    actualTransmissionsCounter = TransmissionsCounter

    if expectedTransmissionCounter == actualTransmissionsCounter:  # We agree that we received the expected message
        expectedTransmissionCounter += 1
        previousMessage = (TransmissionsCounter, TimeStampSent, TimeStampReceived)
        continue  # Process next row
    else:
        lostMessagesCounter += actualTransmissionsCounter-expectedTransmissionCounter+1  # We must have lost messages
        # The message was lost somewhere between the previous received message and the current message
        # Save this time interval and the amount of messages that was lost
        lostMessagesTimeIntervals.append((previousMessage[1], TimeStampSent, lostMessagesCounter))
        expectedTransmissionCounter = actualTransmissionsCounter  # Stay in sync
        expectedTransmissionCounter += 1  # The next expected message is: actual transmissions counter + 1
        previousMessage = (TransmissionsCounter, TimeStampSent, TimeStampReceived)

cursor.close()
cnx.close()


def print_lost_messages(lost_messages_time_intervals):
    for (lostMessageTimeInterval) in lost_messages_time_intervals:
        dt_start = datetime.fromtimestamp(lostMessageTimeInterval[0]/1000)  # fromtimestamp() can only handle seconds and not milliseconds.
        dt_end = datetime.fromtimestamp(lostMessageTimeInterval[1]/1000)

        print("{} messages was lost between {} and {}".format(lostMessageTimeInterval[2], dt_start, dt_end))

print("##### Statistics #####")
print("Number of processed messages: {}".format(expectedTransmissionCounter))
print("Number of lost messages: {}".format(lostMessagesCounter))
print("Lost messages / Total messages ratio: {}".format(lostMessagesCounter/expectedTransmissionCounter))

print("##### Lost messages tuples #####")
print(lostMessagesTimeIntervals)

print("##### Pretty print lost messages #####")
print_lost_messages(lostMessagesTimeIntervals)

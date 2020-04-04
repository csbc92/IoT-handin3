-- Stored procedure that is used to calculate the amount of messages that arrived at a given day + n days forward
-- Returns a table with columns: DayStart, DayEnd, MessageCount
-- DayStart: Timestamp in millis from 1970
-- DayEnd: Timestamp in millis from 1970
-- MessageCount: The amount of messages that arrived between DayStart and DayEnd (excluded)

CREATE DEFINER=`christiancl_dk`@`%` PROCEDURE `MessageCount`(
	IN daystart BIGINT, -- The day from where to start counting. In millis since 1970.
    IN days INT -- Amount of n days to calculate forward given daystart
)
BEGIN
	CREATE TEMPORARY TABLE OUT_TEMP(DayStart BIGINT, DayEnd BIGINT, MessageCount INT);

    SET @currentDayCounter = 0;
    SET @currentDay = daystart;

	WHILE(@currentDayCounter < days) DO
		SET @dayend = @currentDay + 24*60*60*1000; -- The next day in millis since 1970

          INSERT INTO OUT_TEMP
          SELECT @currentDay AS DayStart,
				 @dayend AS DayEnd,
				 COUNT(*) AS MessageCount FROM Messages
		  WHERE TimeStampSent > @currentDay
          AND TimeStampSent < @dayend;

          SET @currentDay = @dayend;
          SET @currentDayCounter = @currentDayCounter + 1;
      END WHILE;

	-- Output results
	SELECT * FROM OUT_TEMP;
	DROP TEMPORARY TABLE OUT_TEMP;
END
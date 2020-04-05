CREATE DEFINER=`christiancl_dk`@`%` PROCEDURE `MessageCountHour`(
	IN daystart BIGINT, -- The day from where to start counting in milliseconds
    IN days INT -- Amount of days to process
)
BEGIN
	CREATE TEMPORARY TABLE OUT_TEMP(DayStart BIGINT, DayEnd BIGINT, DayHourStart BIGINT, DayHourEnd BIGINT, MessageCount INT);

    SET @currentDayCounter = 0;
    SET @currentDay = daystart;
    SET @currentDayHour = @currentDay;

	WHILE(@currentDayCounter < days) DO
		SET @dayend = @currentDay + 24*60*60*1000;

		WHILE(@currentDayHour < @dayend) DO
			  SET @currentDayHourEnd = @currentDayHour + 60*60*1000;
              INSERT INTO OUT_TEMP
			  SELECT @currentDay AS DayStart,
					 @dayend AS DayEnd,
                     @currentDayHour AS DayHourStart,
                     @currentDayHourEnd AS DayHourEnd,
					 COUNT(*) AS MessageCount FROM Messages
			  WHERE TimeStampSent >= @currentDayHour
			  AND TimeStampSent < @currentDayHourEnd;

              SET @currentDayHour = @currentDayHourEnd;
          END WHILE;

          SET @currentDay = @dayend;
          SET @currentDayCounter = @currentDayCounter + 1;
      END WHILE;

	-- Output results
	SELECT * FROM OUT_TEMP;
	DROP TEMPORARY TABLE OUT_TEMP;
END
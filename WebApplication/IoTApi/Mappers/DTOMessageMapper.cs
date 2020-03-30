using System;
using System.Collections.Generic;
using IoTApi.DTOs;
using IoTApi.Model;

namespace IoTApi.Mappers
{
    public class DTOMessageMapper
    {
        public static IoTDevice DTOMessageToIoTDevice(DTOMessage dtoMessage)
        {
            IoTDevice ioTDevice = new IoTDevice()
            {
                Id = dtoMessage.Iotdeviceid,
                Messages = new HashSet<Message>()
            };

            Message message = new Message()
            {
                TimeStampSent = dtoMessage.TimeStamp,
                TimeStampReceived = (long)DateTime.Now.ToUniversalTime().Subtract(
                    new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc)
                ).TotalMilliseconds,
                
                TransmissionsCounter = dtoMessage.TransmissionsCounter,
                IoTDevice = ioTDevice,
                Measurements = new HashSet<Measurement>()
            };

            foreach (var dtoMeasurement in dtoMessage.Measurements)
            {
                message.Measurements.Add(new Measurement()
                {
                    SensorType = dtoMeasurement.SensorType,
                    Value = dtoMeasurement.Value,
                    Message = message
                });
            }
            
            ioTDevice.Messages.Add(message);

            return ioTDevice;
        }
    }
}
namespace IoTApi.DTOs
{
    public class DTOMessage
    {
        public string Iotdeviceid { get; set; }
        public long TimeStamp { get; set; }
        public long TransmissionsCounter { get; set; }

        public DTOMeasurement[] Measurements { get; set; }
    }
}
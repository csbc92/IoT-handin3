using System;
using System.Text;

namespace IoTApi.Model
{
    public class Measurement
    {
        public Guid Id { get; set; }
        
        public string SensorType { get; set; }
        public double Value { get; set; }
        
        public virtual Message Message { get; set; }
        
        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("Guid: ").AppendLine(Id.ToString());
            sb.Append("SensorType: ").AppendLine(SensorType);
            sb.Append("Value: ").AppendLine(Value.ToString("N"));

            return sb.ToString();
        }
    }
}
using System;
using System.Collections.Generic;
using System.Text;

namespace IoTApi.Model
{
    public class Message
    {
        public Guid Id { get; set; }
        public long TransmissionsCounter { get; set; }
        public long TimeStamp { get; set; }
        
        
        public virtual IoTDevice IoTDevice { get; set; }
        public virtual ISet<Measurement> Measurements { get; set; }

        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("Guid: ").AppendLine(Id.ToString());
            sb.Append("Transmissions Counter: ").AppendLine(TransmissionsCounter.ToString());
            sb.Append("TimeStamp: ").AppendLine(TimeStamp.ToString());

            return sb.ToString();
        }
    }
}
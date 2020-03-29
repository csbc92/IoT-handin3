using System.Collections.Generic;

namespace IoTApi.Model
{
    public class IoTDevice
    {
        public string Id { get; set; }
        
        public virtual ISet<Message> Messages { get; set; }
    }
}
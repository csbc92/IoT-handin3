using IoTApi.Model;
using Microsoft.EntityFrameworkCore;

namespace IoTApi.DAL
{
    public class IoTContext : DbContext
    {
        public DbSet<IoTDevice> IoTDevices { get; set; }
        public DbSet<Message> Messages { get; set; }
        public DbSet<Measurement> Measurements { get; set; }

        /**
         * Necessary constructor when using the AddDbContext in Startup.cs
         */
        public IoTContext(DbContextOptions<IoTContext> options) : base(options)
        {
        }
        
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            //optionsBuilder.EnableSensitiveDataLogging(true);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<IoTDevice>(iotdevice =>
            {
                iotdevice.HasKey(iot => iot.Id);
                iotdevice.HasMany(iot => iot.Messages)
                    .WithOne(message => message.IoTDevice);
            });

            modelBuilder.Entity<Message>(message =>
            {
                message.HasKey(m => m.Id);
                message.HasMany(m => m.Measurements)
                    .WithOne(measurement => measurement.Message);
            });
            
            modelBuilder.Entity<Measurement>(measurement =>
            {
                measurement.HasKey(m => m.Id);
            });
        }
    }
}
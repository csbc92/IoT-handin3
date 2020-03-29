using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using IoTApi.DAL;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace IoTApi
{
    public class Program
    {
        public static void Main(string[] args)
        {
            InitializeEFContext();
            
            CreateHostBuilder(args).Build().Run();
        }
        
        private static void InitializeEFContext()
        {
            using (var context = new IoTContext())
            {
                // EnsureCreated() and Migrate are mutually exclusive.
                // Use EnsureCreated for rapid prototyping and not for production.
                
                //context.Database.Migrate();
                context.Database.EnsureCreated(); 

                // Other db initialization code.
            }
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder => { webBuilder.UseStartup<Startup>(); });
    }
}
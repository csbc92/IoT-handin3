using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using IoTApi.DAL;
using Pomelo.EntityFrameworkCore.MySql.Infrastructure;

namespace IoTApi
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }
        
        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers().AddNewtonsoftJson(options =>
                // This needs to be configured, in order to convert IEnumerable to JSON, when there are cycles in the model.
                // See: https://stackoverflow.com/questions/59199593/net-core-3-0-possible-object-cycle-was-detected-which-is-not-supported
                options.SerializerSettings.ReferenceLoopHandling = Newtonsoft.Json.ReferenceLoopHandling.Ignore
            );

            //string connectionString = ConfigurationManager.ConnectionStrings["connectionStringName"].ConnectionString;
            string connectionString = Configuration.GetConnectionString("Production");
            
            // https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql/blob/master/README.md
            services.AddDbContextPool<IoTContext>(options =>
                //options.UseMySql("Server=localhost; Port=3306; Database=iotdb; Uid=root; Pwd=toor;", mysqlOptions =>
                //    mysqlOptions.ServerVersion(new Version(10, 4, 12), ServerType.MariaDb))
                
                options.UseMySql(connectionString, mysqlOptions =>
                    mysqlOptions.ServerVersion(new Version(5, 7, 29), ServerType.MySql))
            );
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints => { endpoints.MapControllers(); });
        }
    }
}
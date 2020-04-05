using System;
using System.Collections.Generic;
using System.Linq;
using IoTApi.DAL;
using IoTApi.DTOs;
using IoTApi.Mappers;
using IoTApi.Model;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace IoTApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class IoTController : ControllerBase
    {
        private readonly IoTContext _context;

        /*
         * Dependency injection of IotContext.
         * Injected automatically when services.AddDbContext<IoTContext> is called in Startup.cs
         */
        public IoTController(IoTContext context)
        {
            _context = context;
            _context.Database.SetCommandTimeout(180);

            InitializeEFContext();
        }
        
        private void InitializeEFContext()
        {
            using (var context = _context)
            {
                // EnsureCreated() and Migrate are mutually exclusive.
                // Use EnsureCreated for rapid prototyping and not for production.
                
                //context.Database.Migrate();
                context.Database.EnsureCreated(); 

                // Other db initialization code.
            }
        }
        
        [HttpGet("all")]
        public IEnumerable<IoTDevice> GetAll()
        {
            using (var ctx = _context)
            {
                return ctx.IoTDevices.Include("Messages.Measurements").ToList();
            }
        }
        
        [HttpGet]
        public IActionResult Get()
        {
            return Ok();
        }
        
        [HttpPost("upload")]
        public IActionResult UploadMessage([FromBody] DTOMessage message)
        {
            Console.WriteLine("Got POST message");
            PrintDTOMessage(message);
            
            using (var ctx = _context)
            {
                var entity = ctx.IoTDevices.Find(message.Iotdeviceid);
                IoTDevice ioTDevice = DTOMessageMapper.DTOMessageToIoTDevice(message);
                
                if (entity == null) // Add or Update?
                {
                    ctx.IoTDevices.Add(ioTDevice);
                }
                else
                {
                    ctx.Entry(entity).Collection("Messages").IsModified = true;
                    ctx.Entry(entity).Collection("Messages").Load();
                    entity.Messages.Add(ioTDevice.Messages.First());
                }

                try
                {
                    ctx.SaveChanges();
                }
                catch (DbUpdateException e)
                {
                    return Problem("Could not update the DB. " + e.Message + e.StackTrace, statusCode: 500);

                }
                catch (Exception e)
                {
                    return Problem("Unspecified error while saving the given data. " + e.Message + e.StackTrace, statusCode: 500);
                }
            }
            
            return Ok();
        }

        private void PrintDTOMessage(DTOMessage message)
        {
            Console.WriteLine($"IoT Device ID: {message.Iotdeviceid}");
            Console.WriteLine($"Message Timestamp: {message.TimeStamp}");
            Console.WriteLine($"Message TransmissionsCounter: {message.TransmissionsCounter}");

            foreach (var measurement in message.Measurements)
            {
                Console.WriteLine($"    Measurement SensorType: {measurement.SensorType}");
                Console.WriteLine($"    Measurement Value: {measurement.Value}");
            }
        }
    }
}
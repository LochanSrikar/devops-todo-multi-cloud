var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/notify", (object data) => {
    // Simulate notification (log to console; can add email later)
    Console.WriteLine($"Notification sent for task: {data.ToString()}");
    return Results.Ok("Notified");
});

app.Run();
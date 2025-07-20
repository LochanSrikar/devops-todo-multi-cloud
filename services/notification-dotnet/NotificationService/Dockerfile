# Start with .NET runtime "box"
FROM mcr.microsoft.com/dotnet/aspnet:8.0
# Set "room" inside
WORKDIR /app
# Copy the published package
COPY out/ .
# "Start the app when box opens"
ENTRYPOINT ["dotnet", "NotificationService.dll"]
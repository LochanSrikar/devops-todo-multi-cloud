# Start with a basic "box" that has Python (slim version is small and fast).
FROM python:3.11-slim

# Set a "room" inside the box for your code—keeps things tidy.
WORKDIR /app

# Copy the "shopping list" of libraries.
COPY requirements.txt .

# "Shop" and install the libraries.
RUN pip install -r requirements.txt

# Copy your code (app.py, etc.) into the box.
COPY . .

# "Start the app when box opens".
CMD ["python", "app.py"]
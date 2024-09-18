import requests
from django.shortcuts import render, HttpResponse, redirect
from .models import TodoItem
from .forms import TodoForm
import csv
import io
from .models import SolarEnergyData
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, "home.html")

def todos(request):
    items=TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def add_todo(request):
      if request.method=="POST":
            form=TodoForm(request.POST)
            if form.is_valid():
                 form.save()
                 return redirect('todos')
      form = TodoForm()
      return render(request, 'addTodo.html', {'form': form})


def cat_facts(request):
      url = "https://catfact.ninja/fact"
      response=requests.get(url)
      if response.status_code==200:
            data=response.json()
            cat_fact=data['fact']
      else:
            cat_fact="Cant get a cat fact at the meowment!"
      return render(request, "catfact.html", {"cat_fact": cat_fact})



def excel_input_view(request):
    data = None

    if request.method == 'POST' and request.FILES.get('csv_file'):
        uploaded_file = request.FILES['csv_file']

        # Read the uploaded CSV file
        csv_file = io.StringIO(uploaded_file.read().decode('utf-8'))
        csv_reader = csv.reader(csv_file)

        # Skip header line
        header = next(csv_reader)
        print(f"CSV Header: {header}")  # Debugging line

        # Initialize a list to store valid rows
        valid_rows = []

        # Process the CSV file
        for row in csv_reader:
            if row:
                try:
                    # Remove timezone information and parse the timestamp
                    timestamp_str = row[0].replace('.000Z', '')
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    
                    kwh = float(row[1])  # Convert kWh to float
                    valid_rows.append((timestamp, kwh))

                    # Update or create the database entry
                    SolarEnergyData.objects.update_or_create(
                        timestamp=timestamp,
                        defaults={'kwh': kwh}
                    )
                    print(f"Updated or Created Record: {timestamp}, {kwh}")  # Debugging line

                except ValueError as e:
                    # Handle errors in data conversion
                    print(f"Skipping invalid row: {row}. Error: {e}")

        # Re-fetch data to display
        solar_data = SolarEnergyData.objects.all()
        data = valid_rows

    return render(request, 'excelinput.html', {'data': data})



def view_solar_data(request):
    # Fetch all records from the SolarEnergyData model
    solar_data = SolarEnergyData.objects.all()
    
    # Pass the data to the template
    return render(request, 'viewSolarData.html', {'solar_data': solar_data})

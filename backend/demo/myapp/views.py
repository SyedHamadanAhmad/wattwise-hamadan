import csv
from io import StringIO
from datetime import datetime

from django.shortcuts import render
from django.utils.dateparse import parse_date

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from .serializers import *
from .models import *


def home(request):
    return render(request, "home.html")


def processCSV(csv_reader):
    valid_rows = []

    # Process the CSV file
    for row in csv_reader:
        if row:
            try:
                # Remove timezone information and parse the timestamp
                timestamp_str = row[0].replace('.000Z', '')
                timestamp = datetime.strptime(
                    timestamp_str, '%Y-%m-%d %H:%M:%S')

                kwh = float(row[1])  # Convert kWh to float
                valid_rows.append((timestamp, kwh))

                # Update or create the database entry
                SolarEnergyData.objects.update_or_create(
                    timestamp=timestamp,
                    defaults={'kwh': kwh}
                )

            except ValueError as e:
                # Handle errors in data conversion
                print(f"Skipping invalid row: {row}. Error: {e}")
    return valid_rows


def excel_input_view(request):
    data = None

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Read the uploaded CSV file
        csv_file = StringIO(uploaded_file.read().decode('utf-8'))
        csv_reader = csv.reader(csv_file)

        data = processCSV(csv_reader)

    return render(request, 'excelinput.html', {'data': data})


def view_solar_data(request):
    # Fetch all records from the SolarEnergyData model
    solar_data = SolarEnergyData.objects.all()

    # Pass the data to the template
    return render(request, 'viewSolarData.html', {'solar_data': solar_data})


class SolarEnergyDataViewSet(viewsets.ModelViewSet):
    queryset = SolarEnergyData.objects.all()
    serializer_class = SolarEnergyDataSerializer

    @action(detail=False, methods=['get'])
    def filter_by_dates(self, request):
        # Get query parameters for start_date and end_date
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate the date format
        if not start_date or not end_date:
            return Response({"error": "Both start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date_parsed = parse_date(start_date)
        end_date_parsed = parse_date(end_date)

        if not start_date_parsed or not end_date_parsed:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        data = SolarEnergyData.objects.filter(
            timestamp__date__gte=start_date_parsed, timestamp__date__lte=end_date_parsed)

        serializer = SolarEnergyDataSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        data = None
        file_obj = request.FILES.get('file', None)
        if not file_obj:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_data = file_obj.read().decode('utf-8')
            csv_reader = csv.reader(StringIO(file_data))
            data = processCSV(csv_reader)
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": data}, status=status.HTTP_201_CREATED)

./demo

To Run the django app, turn on the virtual env (1) everytime. After the first clone, install the requirements.txt to get the dependencies(3). Before comiting, run (2) to save any dependencies you might have added.


  1]source env/bin/activate --To activate the virtual environment

  2]pip freeze > requirements.txt  -- Before every commit to keep the requirements.txt file updated

  3]pip install -r requirements.txt --To install any new dependencies

After this it's run django normally.


apiDetails:

Get - http://127.0.0.1:8000/api/SolarEnergyData/

Get - filter between two dates
http://127.0.0.1:8000/api/SolarEnergyData/filter_by_dates/?start_date=2024-06-15&end_date=2024-06-25

Post - http://127.0.0.1:8000/api/SolarEnergyData/
Body for Post-{
        "timestamp": "2024-06-29T18:30:00Z",
        "kwh": 205.984
}

Post - http://127.0.0.1:8000/api/SolarEnergyData/upload_csv/

Body of form for Post -
type=file
name/value="file"
accept=.csv
# Running this repo using dagster in dev
dagster dev

# Running dash_app on local machine 
cd dash_app
python3 src/app.py

# Running dagster 
docker compose up

# dash app as docker containers
Please access http://127.0.0.1:3000/locations/workflow/jobs/apdv_etl_job , click on Materialize all button

Once all assets are materialized. run the following command from the same folder

# dash dash board app as docker containers
docker compose start dash_app 

Please open http://localhost:8070 in your browser to access the dashboard

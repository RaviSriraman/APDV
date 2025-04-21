# Create Virtual env
conda env create -f environment.yml
conda activate apdv
pip install dagster dagster-webserver dagstermill psycopg2
pip install 

# Running this repo using dagster in dev
dagster dev

# dash app as docker containers
Please access http://127.0.0.1:3000/locations/workflow/jobs/apdv_etl_job , click on Materialize all button

Once all assets are materialized. run the following command from the same folder

# Running dash_app on local machine 
cd dash_app
python3 src/app.py
Please open http://localhost:8070 in your browser to access the dashboard

# Running dagster  (only on unix based systems)
docker compose up

# dash dash board app as docker containers
docker compose start dash_app 

Please open http://localhost:8070 in your browser to access the dashboard

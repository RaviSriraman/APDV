import papermill as pm
from dagster import job, op

@op
def read_and_load_enterprise_data():
    input_notebook = "./enterprises.ipynb"
    output_notebook = "./enterprises_output.ipynb"
    pm.execute_notebook(input_notebook, output_notebook)
    return f"Notebook {output_notebook} executed successfully!"

@op
def load_from_mongo(message: str):
    input_notebook = "./load_from_mongo.ipynb"
    output_notebook = ".load_from_mongo_output.ipynb"
    pm.execute_notebook(input_notebook, output_notebook)
    return message

@job
def my_notebook_job():
    load_from_mongo(read_and_load_enterprise_data())

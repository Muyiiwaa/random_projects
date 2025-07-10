diabetes project.
PROCESSES.
    1. grab the data from kaggle
    2. train the base model
    3. finetune the basemodel
    4. retrain the final model
    5. build a pipeline
    6. build a demo streamlit application
    6. wrap the model in an api.
    7. deploy.

STEPS.
1. setup our package manager.(using uv)
    - install uv (pip install uv)
    - create a project folder (uv init diabete-ml-app)
    - enter into the project folder that is just created (cd diabetes-ml-app)
2. create the project structure
    - create notebook.ipynb for training 
    - create the file and folder for the pipeline.
3. add all the required libraries using (uv add 'the name of the library')
4. activate our virtual environment (.venv\Scripts\activate)
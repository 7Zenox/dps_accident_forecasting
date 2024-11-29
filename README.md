# Accident Prediction API

## Directory Structure
Here is an overview tree structure of the directory:

```
|-requirements.txt
|-Dockerfile
|-utilities
| |-core
| | |-security.py
| | |-exceptions.py
| |-api
| | |-v1
| | | |-endpoints               <- endpoint routes
| | | | |-accident.py
| | | |-api.py
| | |-health.py                 <- check app health at 0.0.0.0:port/
| |-main.py
| |-helpers                     <- write helper functions
| | |-response.py
| | |-hosprec                   
| | | |-utils                   <- store models and utils in utils directory
| | | | |-util1.py
| | | | |-hosprec_model.keras
| | | | |-...
| | | |-experiment              <- store experiment files
| | | | |-experiment.ipynb
| | | | |-Basic_v26.sqlite
| | | |-main.py                 <- maintain main.py naming convention
| | | |-create_model.py
| | |-icd_search
| | | |-utils
| | | | |-...
| | | |-main.py
|-.dockerignore
|-logs
| |-debug_icd.log               <- store one log file per helper
|-.gitignore
|-.gitattributes
|-.git
| |-config
|-start-server.py               <- run server
```

## Common Practices

### 1. Add Experimentation Files within Helper Directory

- Experimentation files should be placed in the `experiment` folder within the respective helper directory.
- Example: `utilities/helpers/hosprec/experiment/experiment.ipynb`

### 2. Maintain Utilities of a File inside Respective Helper Folder's Util Folder

- Utility functions, models and supporting files specific to a module should be kept in the `utils` folder within the respective helper directory.
- Example: `utilities/helpers/hosprec/utils/util1.py`

### 3. Use Pre-created DB Engine Class

- For database connections, use the pre-created `DBEngine` class from `utilities/core/db_engine.py`.
- This ensures a consistent approach to database connections, reducing number of engine creations, improving modularity and code readability across the project.

Use:
```python
from utilities.core.db_engine import DBEngine
from utilities.core.config import settings
```
### 4. Maintain Logs Using Logger

- All logs should be maintained using the `logger`.
- Logs should be stored in the `logs` directory.
- Ensure rolling file size is used to prevent large storage files from being created.
- Example: `logs/debug_icd.log`

Sample log template for config:
```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logger
logger = logging.getLogger('icdhelper')
logger.setLevel(logging.INFO)

# Create a RotatingFileHandler with a maximum file size of 10 MB and no backups
log_file = 'logs//debug_icd.log'
max_size = 10 * 1024 * 1024  # 10 MB
backup_count = 0  # Maintaining no backup files

rotating_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
rotating_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
```
Sample Usage
```python
try:
    # If processed data is not empty, append it to the database.
    if processed_df:
        # ...
        logger.info("Processed dataframe is not empty and pushed to db")
    else:
        logger.warning("Processed dataframe is empty. Please check API.")
except Exception as e:
    logger.error(f"Failed to append processed data: {e}")
```

## Important Guidelines

- Use relative paths when loading files.
- Right click on file you wish to load, copy relative path

#### For h5py issues
- All dependencies are up to date. However you may notice tensorflow 2.17 works fine with h5py 3.11 on local when running the FastAPI server. However it will not build on docker due to dependency conflicts. Set `tensorflow==2.17` and `h5py==3.10` till compatibility updates.

### Push Dependencies to Docker ECR
- How to login to ecr 
```aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 106102357433.dkr.ecr.ap-south-1.amazonaws.com```

- Build image using dockerfile names Dockerfile_build

`docker build -f Dockerfile_build -t hosprecommendation .`

- Tag the latest image to ecr repo

```docker tag ee85d0a9514c 106102357433.dkr.ecr.ap-south-1.amazonaws.com/hosprecommendation:latest```

- Push docker image to ecr

```docker push 106102357433.dkr.ecr.ap-south-1.amazonaws.com/hosprecommendation:latest```


## Running the Application
**To create a virtual environment and install requirements**
```sh
python3 -m venv venv
source venv/bin/activate
python3 install -r requirements.txt
```
**To start the FastAPI application**
```sh
pip3 start-server.py
```
**Build docker container**
```sh
docker build -t onsurityAI .
```
**Run Docker container**
```sh
docker run -d -p 5001:5001 onsurityAI
```
**Check running containers**
```sh
docker ps -a
```

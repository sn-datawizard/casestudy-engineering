# Proof of Concept (PoC) Data Engineering

## Summary
The Proof of Concept (PoC) follows industry best practices, implementing a three-layer Azure Data Lake for efficient data storage. Python Docker Applications are chosen for data fetching and processing, offering a smooth development and deployment process with custom configurations. Kubernetes is utilized for Docker deployment, providing smooth orchestration. ​<br>

The PoC's expectations include successful execution of the data pipeline, Terraform-based infrastructure creation, and sequential updates to the Data Lake. The architecture can be extended with additional data sources, showcasing a future-proof solution. ​<br>

Overall, the PoC demonstrates a seamless integration of technologies for a reliable data engineering pipeline.

## Use Case
The population of Germany experience continiuous growth with each passing year. 
This has impact on various aspects like rent prices, public transport systems and the retirement system.
To project the population's growth in the coming years, relevant data is required to develop predictive models.​ <br><br>
In order to enhance the precision of the developed model, more data sources will be integrated to the data pipeline in future. <br>

### Milestone
Provide population data and data related to population growth in Germany to Data Scientists.


### Data Source
The API for GENESIS ONLINE Database from Statistisches Bundesamt Deutschland is used as data source. <br> <br>
https://www-genesis.destatis.de/genesis/online
#### Tables: <br>
12411-0001 Population: Germany, reference date <br>
12711-0008 Migration between Germany and abroad: Germany, yers, nationality, countries of origin/destination <br>
12612-0001 Live births: Germany, years, sex <br>


## High Level Design Architecture
### Architecture Diagram
![HH-Design Architecture](https://github.com/sn-datawizard/casestudy-engineering/assets/77932366/4cf0778f-1837-4150-b669-10cc9f76f3f9)



## Architecture Requirements & Design Decisions
### Requirements for architecture
- Can be extended by additional data sources
- Offers Scalability
- Has consistent configurations and can be fast deployed
- Is reducing management overhead, fast if additional infrastructure is required

### Design Decisions
#### Three layer Azure Data Lake (Bronze, Silver, Gold)
- Following reference architectures and best practices​ (https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/ingest-etl-stream-with-adb)
- Data can be stored in native format, required data formats are supported​
- Storage can easily be extended, for instance logging files​
- Faster development process and code is easy to maintain​

#### Python Docker Applications to fetch and process data
- Own configuration​
- Fast deployment possible​
- Proper testing possible as Docker runs as isolated environment​
  
#### Kubernetes for Docker deployment
- Smooth development process​
- Custom configuration for orchestration of Python applications​
- Fast deployment and scaling with Kubernetes
- Logging


#### Terraform for infrastructure
- Easier management of services

## Low Level Design Archtiecture
### Architecture Diagram
![LL-Desgin Architecture](https://github.com/sn-datawizard/casestudy-engineering/assets/77932366/d0a0e2bf-fe6a-4e38-9705-2a9262e9eaef)

### Technologies
Ingestion: Python, Docker <br>
Storage: Azure Data Lake Storage (Storage containers) <br>
Processing: Python, Docker <br>
Orchestration: Kubernetes <br>
Infrastructure: Terraform <br>
Code Repository: Github <br>


## Low Level Design Pipeline
### Pipeline Diagram
![LL-Design Pipeline](https://github.com/sn-datawizard/casestudy-engineering/assets/77932366/c576bd42-417e-470e-b33f-a6e50edc593f)

### Data extraction
The Python scripts population_fetch.py, migration_fetch.py and birth_fetch.py are fetching data from the data source. A logic is implemented that before actually sending the API request to fetch the data, the script will call the 'Logincheck' endpoint and if the response code is 200 (successful) then API call for data fetching will be executed. <br>
All scripts convert the JSON response to multiple lists which then will create a pandas data frame to be uploaded to the Azure Storage Container (Data Lake).

### Data transformation
The Python script transform.py is reading and cleaning data from Azure Data Lake (Bronze Layer) and uploads the cleaned dataset to Silver Layer. The following transformation are performed:
- Convert integer values from column 'Year' into actual dates and assign date data type with pandas datetime function
- JOIN data frames
- Fill NaN values with custom values (NONE for non-integer and non-float values, 0 for integer and float values) to ensure no error when do calculations and aggregations

Furthermore transform.py is reading data from Azure Data lake (Silver Layer) and uploads the enriched dataset to Gold Layer to be used by Data Scientists. The following enrichtments are performed:
- Select required columns 'Year' and 'Population'
- Use pandas pct_change function to calculate the year over year change in percentage for each year

### Reusable Functions
The script helper.py contains three functions:
- check_login: Sends API request to 'Logincheck' endpoint and returns the status code
- fetch_data: Sends API request to 'Data' endpoint and returns the JSON response
- upload_data: Converts the pandas data frame to a .csv file and uploads the file to Azure Data Lake (Storage container)

### Docker image
The Dockerfiles are containerizing the Python applications to run on any machine without running into dependency probles and to have a seperated environment. The Python image python:3.9-slim-buster is used as base image. <br>
The Dockerfile copys all required Python files and the requirements.txt file into the Docker directory. Furthermore all required Python modules will be installed. <br> 
The Docker image is configured to execute the Python script as soon as the Docker container starts. <br> <br>

To ensure fast deployment, a docker-compose.yml file is configured to build all Docker images at once.

### Kubernetes configuration
To ensure fast deployment, a pod.yaml file is configured to run all Docker container with created Docker images. <br>
The containers will not restart.


## Testing & Monitoring
### Testing
Several tests are performed to ensure a successful run of the data pipeline and a correct dataset.
#### Test case 1: ​
- Run containers with Kubernetes and check logs​
- Check 'Modified' datetime in storage containers​
Expected result: Successful run without errors, Date modified changed

#### Test case 2:​
- Run Docker image locally to validate successful run on different machines​
Expected result: Successful run without errors

#### Test case 3:​
- Download data in Gold Layer storage container and validate data
Expected result: Transformations are applied to final data set

### Monitoring
Kubernetes logs is used for monitoring



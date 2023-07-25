# casestudy-engineering
## Use Case
The population of Germany experience continiuous growth with each passing year. 
This has impact on various aspects like rent prices, public transport systems and the retirement system.
To project the population's growth in the coming years, relevant data is required to develop predictive models.​ <br><br>
In order to enhance the precision of the developed model, more data sources will be connected to the data pipeline in future.

## Data Source
The API for GENESIS ONLINE Database from Statistisches Bundesamt Deutschland is used as data source. <br> <br>
https://www-genesis.destatis.de/genesis/online
#### Tables: <br>
12411-0001 Population: Germany, reference date <br>
12711-0008 Migration between Germany and abroad: Germany, yers, nationality, countries of origin/destination <br>
12612-0001 Live births: Germany, years, sex <br>


## High Level Design Architecture
### Architecture Diagram
![HH-Design Architecture](https://github.com/sn-datawizard/casestudy-engineering/assets/77932366/ba443866-2364-4971-b8db-0f8f588a8c51)

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
- Proper testing possible as Docker runs as new environment​
  
#### Kubernetes for Docker deployment
- Smooth development process​
- Easy configuration for orchestration of Python applications​
- Easy deployment and scaling with Kubernetes
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

### Scripts




## Data Transformations




## Testing & Monitoring

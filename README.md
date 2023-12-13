# Delta Sharing Examples

Example that extends the [Delta Sharing Python Connector](https://github.com/delta-io/delta-sharing) and simplifies its use.
DeltaShareCLient class defines a new set of methods to access the share and simplifies the logic to get the shares and the list of tables per share.

## What is delta-sharing ?
[Delta Sharing](https://delta.io/sharing) is an open protocol for secure real-time exchange of large datasets, which enables organizations to share data in real time regardless of which computing platforms they use.

                                                                                                                                                                                                                                                                                                                                                     
## Depedencies                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                      
* [Docker](https://docs.docker.com/engine/install/)                                                                                                                                                                                                                                                                                                   
* [Docker Compose](https://docs.docker.com/compose/install/)                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                      
## Getting started                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                      
### Build the container                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                      
First step to create the environment is to build the container image.                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                      
In the root folder of the project execute the next command to start the creation process.                                                                                                                                                                                                                                                             
```bash                                                                                                                                                                                                                                                                                                                                               
$ docker-compose build --force-rm                                                                                                                                                                                                                                                                                                                     
```                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                      
If the container was built more than one time in the past, sometimes could exist inconsistencies in the install libs or, in that case is recommended to add the **--no--cache** argument.                                                                                                                                                             
```bash                                                                                                                                                                                                                                                                                                                                               
$ docker-compose build --force-rm --no-cache                                                                                                                                                                                                                                                                                                          
```                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                      
The next step is to start the container.                                                                                                                                                                                                                                                                                                              
```bash                                                                                                                                                                                                                                                                                                                                               
$ docker-compose up -d                                                                                                                                                                                                                                                                                                                                
```                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                      
To login into container instance.                                                                                                                                                                                                                                                                                                                     
```bash                                                                                                                                                                                                                                                                                                                                               
$ docker exec -it delta_sharing bash                                                                                                                                                                                                                                                                                                  
```                                                                

## Quick Start

```python
from share import DeltaShareClient
from log import Log

# config.share or profile file, provided by Databricks
profile_file = "resources/config.share"

# Create DeltaShareClient
delta = DeltaShareClient(profile_file=profile_file)

# Print list of shares and tables
log.info(f"f{delta.get_list_of_tables()}")

# Get specific table from the list
ingresos_tbl = delta.get_table("ingresos", limit=100)


log.info(f"Print Pandas dataframe context")
df = ingresos_tbl.to_pandas()
print(df)

log.info(f"Print filtered data")
print(df[df['anlage'] == 4100002134])

log.info(f"Store data into csv file")
df.to_csv('outputs/ingresos_tbl.csv')

```
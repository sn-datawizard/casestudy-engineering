import helper
import config
import time
import pandas as pd

start_time = time.time()
#Set login parameter
USERNAME = config.username
PASSWORD = config.password

#Check if login succesfull, if yes fetch data
if helper.check_login(USERNAME, PASSWORD) == 200:
    tablename = "12711-0008"
    result = helper.fetch_data(USERNAME, PASSWORD, tablename, 2000, 2021)
    data = result.json()["Object"]["Content"].split("\n")[8:-4]
    #print(data)
    
    year_list = []
    country_list = []
    immigration_list = []
    emigration_list = []
    migration_list = []

    for i in range(len(data)):
        year_list.append(data[i].split(";")[0])
        country_list.append(data[i].split(";")[1])
        immigration_list.append(data[i].split(";")[8])
        emigration_list.append(data[i].split(";")[9])
        migration_list.append(data[i].split(";")[10])


    df = pd.DataFrame(
        {'Year': year_list, 
        'Country': country_list, 
        'Immigration': immigration_list, 
        'Emigration': emigration_list, 
        'Migration': migration_list}
        )
    
    # Upload dataframe as csv to Data Lake Storage
    print(df.head(10))

    
    conx_string = config.connection_string
    storagecontainer = 'bronze-dlscontainer-amazingetl'
    filename = 'migration.csv'
    helper.upload_data(df, storagecontainer, filename, conx_string)
    
else:
    print("Error, Status code is not 200, get response failed")

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds") 



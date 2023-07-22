import helper
import config
import pandas as pd
import time

start_time = time.time()
#Set login parameter
USERNAME = config.username
PASSWORD = config.password

#Check if login succesfull, if yes fetch data
if helper.check_login(USERNAME, PASSWORD) == 200:
    tablename = '12411-0001'
    result = helper.fetch_data(USERNAME, PASSWORD, tablename, 1950, 2022)
    data = result.json()
    cleaned = data['Object']['Content'].splitlines()[6:-6]


    year_list = []
    population_list = []

    for i in range(len(cleaned)):
        year_list.append(cleaned[i].split(';')[0])
        population_list.append(cleaned[i].split(';')[1])

    df = pd.DataFrame(
        {'Year': year_list, 
        'Population': population_list,}
        )    

    # Upload dataframe as csv to Data Lake Storage
    print(df.head(10))

    conx_string = config.connection_string
    storagecontainer = 'bronze-dlscontainer-amazingetl'
    filename = 'data.csv'
    helper.upload_data(df, storagecontainer, filename, conx_string)

else:
    print("Error, Status code is not 200, get response failed")

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds") 

import helper
import config
import pandas as pd
import time

#Set login parameter
USERNAME = config.username
PASSWORD = config.password

#Check if login succesfull, if yes fetch data
if helper.check_login(USERNAME, PASSWORD) == 200:
    tablename = '12612-0001'
    result = helper.fetch_data(USERNAME, PASSWORD, tablename, 1950, 2022)
    data = result.json()
    cleaned = data['Object']['Content'].splitlines()[6:-6]

    year_list = []
    male_birth_list = []
    female_birth_list = []
    total_birth_list = []

    for i in range(len(cleaned)):
        year_list.append(cleaned[i].split(';')[0])
        male_birth_list.append(cleaned[i].split(';')[1])
        female_birth_list.append(cleaned[i].split(';')[2])
        total_birth_list.append(cleaned[i].split(';')[3])

    df = pd.DataFrame(
        {'YearOfBirth': year_list, 
        'Male': male_birth_list, 
        'Female': female_birth_list, 
        'Total': total_birth_list}
        )    

    # Upload dataframe as csv to Data Lake Storage
    print(df.head(10))

    
    conx_string = config.connection_string
    storagecontainer = 'bronze-dlscontainer-amazingetl'
    filename = 'birth.csv'
    helper.upload_data(df, storagecontainer, filename, conx_string)
    
else:
    print("Error, Status code is not 200, get response failed")

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds") 


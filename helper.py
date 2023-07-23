import config
import requests

def check_login(username, password):
    url = f"https://www-genesis.destatis.de/genesisWS/rest/2020/helloworld/logincheck?username={username}&password={password}&language=de"
    response = requests.get(url)
    return response.status_code

def fetch_data(username, password, tablename, startyear, endyear):
    url = f"https://www-genesis.destatis.de/genesisWS/rest/2020/data/table?username={username}&password={password}&name={tablename}&area=all&startyear={startyear}&endyear={endyear}&compress=false&transpose=false&job=false&stand=01.01.1970&language=de"
    response = requests.get(url)
    return response

def upload_data(df, storagecontainer, filename, connection):
    df.to_csv(f'abfs://{storagecontainer}/{filename}', storage_options = {'connection_string' : connection}, sep=';', index=False)
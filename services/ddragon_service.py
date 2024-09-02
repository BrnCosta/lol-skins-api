import requests
from logger import logger

class DDragonService:
    DDRAGON_API_URL = 'https://ddragon.leagueoflegends.com/api/'
    DDRAGON_DATA_URL = f'https://ddragon.leagueoflegends.com/cdn/'
    VERSION_URL = ''
    VERSION = ''

    def __init__(self):
        self.get_latest_package_version()

    def get_latest_package_version(self) -> None:
        try:
            version_url = self.DDRAGON_API_URL + 'versions.json'
            logger.info(f'Getting DDragon latest package version from {version_url}...')

            response = requests.get(version_url)
            if response.status_code == 200:
                version_data = response.json()

                if self.VERSION is None or self.VERSION == '':
                    self.VERSION = version_data[0]
                    self.VERSION_URL = self.VERSION + '/data/en_US/'
                    logger.info(f'Version defined {self.VERSION}...')
                
                return version_data[0]
            else:
                logger.error(f'Failed to get package version: {response.status_code}')
                return {"error": "Failed to get package version"}
        except Exception as e:
            logger.exception("An error occurred while getting the package version.")
            return {"error": str(e)}
    
    def get_champions_list(self):
        try:
            data_url = self.DDRAGON_DATA_URL + self.VERSION_URL + f'champion.json'
            logger.info(f'Getting champions list from {data_url}...')

            response = requests.get(data_url)
            if response.status_code == 200:
                champions_data = response.json()['data']
                champions_list = []
                for champion in champions_data:
                    champions_list.append(champion)
                return champions_list
            else:
                logger.error(f'Failed to get champions list: {response.status_code}')
                return {"error": "Failed to get champions list"}
        except Exception as e:
            logger.exception("An error occurred while getting the champions list.")
            return {"error": str(e)}
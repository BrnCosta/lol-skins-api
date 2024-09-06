import requests, tarfile, os
from sqlalchemy.orm import Session

from logger import logger
from database.models import Champion, Skin
from database.database_config import get_db

DDRAGON_API_URL = 'https://ddragon.leagueoflegends.com/api'
DDRAGON_DATA_URL = f'https://ddragon.leagueoflegends.com/cdn'

def get_latest_package_version() -> None:
    try:
        version_url = DDRAGON_API_URL + '/versions.json'
        logger.info(f'Getting DDragon latest package version from {version_url}...')
        response = requests.get(version_url)

        if response.status_code == 200:
            version_data = response.json()
            return version_data[0]
        
        logger.error(f'Failed to get package version: {response.status_code}')
        return None
    except Exception as e:
        logger.exception(f"An error occurred while getting the package version: {e}")
        return None

def get_champions_data(version):
    try:
        data_url = f'{DDRAGON_DATA_URL}/{version}/data/en_US/championFull.json'
        logger.info(f'Getting champions list from {data_url}...')
        response = requests.get(data_url)

        if response.status_code == 200:
            return response.json()['data']
        
        logger.error(f'Failed to get champions list: {response.status_code}')
        return None
    except Exception as e:
        logger.exception(f"An error occurred while getting the champions list: {e}")
        return None

def filter_champion_data(champion_data) -> tuple[list[Champion], list[Skin]]:
    champions_list, skins_list = [], []
    for champion_id in champion_data:
        champion_name = champion_data[champion_id]['name']
        skins = champion_data[champion_id]['skins']
        for skin in skins:
            skin_object = Skin(name=skin['name'], number=skin['num'], image=f'{champion_id}_{skin['num']}', champion_name=champion_name)
            skins_list.append(skin_object)
        champion_object = Champion(name=champion_name)
        champions_list.append(champion_object)
    return champions_list, skins_list
    
async def verify_if_register_exists_database(entity, *register_key) -> bool:
    try:
        async for db in get_db():
            register = db.get(entity, register_key if len(register_key) > 1 else register_key[0])
        return register is not None
    except Exception as e:
        raise Exception(f"An error occurred while verifying {register_key} in database: {e}")
        
async def insert_champion_info_database(champions_info: list[Champion]):
    try:
        async for db in get_db():
            for champion in champions_info:
                if not await verify_if_register_exists_database(Champion, champion.name):
                    db.add(champion)
            db.commit()
    except Exception as e:
        raise Exception(f"An error occurred while inserting the champions list into database: {e}")

async def insert_skin_info_database(skins_info: list[Skin]):
    try:
        async for db in get_db():
            for skin in skins_info:
                if not await verify_if_register_exists_database(Skin, skin.name, skin.champion_name):
                    db.add(skin)
            db.commit()
    except Exception as e:
        raise Exception(f"An error occurred while inserting the champions list into database: {e}")
    
def download_ddragon_file(ddragon_url, ddragon_file_tgz):
    try:
        if os.path.exists(ddragon_file_tgz):
            logger.info(f"File {ddragon_file_tgz} already exists!")
            return

        logger.info(f"Downloading file {ddragon_url}...")
        response = requests.get(ddragon_url, stream=True)

        os.makedirs(os.path.dirname(ddragon_file_tgz), exist_ok=True)

        with open(ddragon_file_tgz, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        logger.info(f"File downloaded at: {ddragon_file_tgz}")
    except Exception as e:
        raise Exception(f"An error occurred while downloading the ddragon files: {e}")

def extract_tar_file(tgz_file, folder_to_extract, output_dir):
    try:
        logger.info(f"Extracting {tgz_file} to {output_dir}...")
        with tarfile.open(tgz_file, "r:gz") as tar:
            members = tar.getmembers()
            for member in members:
                if member.isreg() and member.name.__contains__(folder_to_extract):
                    member.name = os.path.basename(member.name)

                    if os.path.exists(os.path.join(output_dir, member.name)):
                        continue

                    tar.extract(member, path=output_dir)
    except Exception as e:
        raise Exception(f"An error occurred while extracting the ddragon files: {e}")
    
async def initiate_ddragon_information():
    latest_version = get_latest_package_version()

    if latest_version == None:
        raise Exception(f'Not starting the application without the latest version.')

    logger.info(f'Using latest DDragon version: {latest_version}')

    champion_data = get_champions_data(latest_version)

    champions, skins = filter_champion_data(champion_data)

    logger.info(f'{len(champions)} champions found! Inserting in database if needed...')
    logger.info(f'{len(skins)} skins found! Inserting in database if needed...')

    await insert_champion_info_database(champions)
    await insert_skin_info_database(skins)

    logger.info(f'Database loaded successfully! All DDragon data imported.')
    
    logger.info(f'Getting DDragon files...')
    
    ddragon_url = f'{DDRAGON_DATA_URL}/dragontail-{latest_version}.tgz'
    ddragon_tgz = f'download/{latest_version}.tgz'

    download_ddragon_file(ddragon_url, ddragon_tgz)
    extract_tar_file(ddragon_tgz, 'loading', 'static/images/skins')

    logger.info(f'DDragon files downloaded!')
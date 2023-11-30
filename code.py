import json
import os
import zipfile
import sys
import datetime
import requests

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Sequence, DateTime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# One cup data url from cricksheet
base_url = "https://cricsheet.org/downloads/rlc_json.zip"

# File Name to Save on Local
file_name = f"odi_cup_data_{str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))}"

def download_file(base_url, file_name):
    format = 'zip'
    url = base_url.format(format=format)
    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {format} data")

# Download the file
download_file(base_url, file_name + '.zip')

def extract_zip(zip_file_path, extract_to_directory):
    # Ensure the extraction directory exists
    os.makedirs(extract_to_directory, exist_ok=True)

    # Open the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all contents to the specified directory
        zip_ref.extractall(extract_to_directory)


# Extract the file
extract_zip(file_name + '.zip', file_name)


# Set Directort Path
directory_path = file_name

# List all files in the directory
files = os.listdir(directory_path)

# Filter JSON files
json_files = [file for file in files if file.endswith('.json')]


# Database Credentials
database_username = 'root'
database_password = '1111'
database_host = 'localhost'
database_port = '3306'
database_name = 'cricket_data'


# Loop through JSON files
for json_file in json_files:
	json_file_path = directory_path + "/" +  json_file
	with open(json_file_path, 'r') as file:
		data = json.load(file)	


	Session = sessionmaker(bind=engine)
	session = Session()

	# Create a connection string
	connection_string = f"mysql+mysqlconnector://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"

	# Create an SQLAlchemy engine
	engine = create_engine(connection_string, echo=True)  # Set echo to True for logging SQL statements

	Base = declarative_base()

	class Players(Base):
		__tablename__ = 'players'
		player_id = Column(String(20), primary_key=True)
		player_name = Column(String(50))
		player_gender = Column(String(10))
		extend_existing=True

	class Match_results(Base):
		__tablename__ = 'match_results'
		match_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
		team1 = Column(String(50))
		team2 = Column(String(50))
		winner = Column(String(50))
		result = Column(String(50))
		gender = Column(String(10))
		date_of_match = Column(DateTime)
		extend_existing=True

	class Ball_by_ball(Base):
		__tablename__ = 'ball_by_ball'
		match_id = Column(Integer, primary_key=True)
		inning_number = Column(Integer, primary_key=True)
		over_number = Column(Integer, primary_key=True)
		ball_number = Column(Integer, primary_key=True)
		runs_by_onstrike_player = Column(Integer)
		runs_by_extra = Column(Integer)
		runs_by_total = Column(Integer)
		wicket = Column(Boolean)
		player_out = Column(String(50))
		onstrike_player_id = Column(String(50))
		extend_existing=True


	# Create tables in the database
	Base.metadata.create_all(engine)

	# Create a session
	Session = sessionmaker(bind=engine)
	session = Session()

	for player_name, player_id in data['info']['registry']['people'].items():
		new_players = Players(player_name=player_name, player_id=player_id, player_gender=data['info']['gender'])
		session.merge(new_players)

	print(data['info']['outcome'])
	if 'result' in data['info']['outcome'].keys():
		winner = data['info']['outcome']['result']
		result = data['info']['outcome']['result']
	else:
		winner = data['info']['outcome']['winner']
		result = str(data['info']['outcome']['by'])

	new_match_results = Match_results(team1=data['info']['teams'][0], team2=data['info']['teams'][1], winner=winner, result=result, gender=data['info']['gender'], date_of_match=data['info']['dates'][0])
	session.add(new_match_results)
	session.commit()

	print('Match ID - ',  new_match_results.match_id)

	for inning_index, inning_data in enumerate(data['innings']):
		for over_index, over_data in enumerate(inning_data['overs']):
			for deliveries_index, deliveries_data in enumerate(over_data['deliveries']):
				new_ball_by_ball = Ball_by_ball(
					match_id=new_match_results.match_id, 
					inning_number=inning_index+1, 
					over_number= over_data['over'],
					ball_number = deliveries_index+1,
					runs_by_onstrike_player=deliveries_data['runs']['batter'],
					runs_by_extra=deliveries_data['runs']['extras'],
					runs_by_total=deliveries_data['runs']['total'],
					wicket= True if 'wickets' in deliveries_data.keys() else False,
					player_out=deliveries_data['wickets'][0]['player_out'] if 'wickets' in deliveries_data.keys() else None,
					onstrike_player_id = dict(data['info']['registry']['people'].items())[deliveries_data['batter']]
				)
				session.add(new_ball_by_ball)

	session.commit()
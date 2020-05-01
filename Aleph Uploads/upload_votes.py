import os
from pathlib import Path
import requests
# Import alephclient:
from alephclient.api import AlephAPI

# By default, alephclient will read host and API key from the 
# environment. You can also pass both as an argument here:
api = AlephAPI()

# Get the collection (dataset)
foreign_id = '5eaeb12a65fd4b1d956aa309b6cd101a'
collection = api.load_collection_by_foreign_id(foreign_id)
collection_id = collection.get('id')

votes = "https://www.nassnig.org/documents/votes_track"
docs_url = "https://www.nassnig.org/documents/download/"

response = requests.get(votes)
doc_json = response.json()
docs = doc_json['data']

folder_location = './votes'
for doc in docs:
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)

    metadata = {
        'title': doc[0],
        'languages': ['en'],
        'Date' : doc[1],
        'Chamber' : doc[2],
        'Parliament': doc[3],
        'Session' : doc[4],
        'Type' : doc[5],
        }

    url = docs_url + doc[6]
    file_name =  doc[0].strip().title()+'.pdf'
    file_path = Path(os.path.join(folder_location,file_name))

    ####  make Downloads
    try:
        if not file_path.is_file():
            with open(file_path, 'wb') as f:
                doc_file = requests.get(url).content
                f.write(doc_file)

    except Exception as e:
          print(e,"Doc hasn't been posted or File Exists")

        # # # Upload the document:
        result = api.ingest_upload(collection_id, file_path, metadata)

        # # # Finally, we have an entity ID:
        document_id = result.get('id') 
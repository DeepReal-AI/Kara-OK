# Kara-OK

Repository for a Karaoke app

## Set up conda environment

```sh
conda env create --prefix ./karaoke-env --file ./karaoke_app/audio_splitter/environment.yml
conda activate ./karaoke-env
```
## Google Cloud API key set up

You need to push your api key in the "grandfather" of current directory. Current directory is <grandfather>/<father>/Kara-OK and you have to push your key at <grandfather>/key.json.
 
## Use the app

 ```sh
uvicorn api.main:app --reload
```

  
```sh
cd client && npm run start
```
  
The application will run on localhost:3000
  

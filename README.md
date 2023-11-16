# Personalized Restaurant Search

an autonomous AI agent

# How to Run?

### Create a `.env`file with the following

```
OPENAI_API_KEY = "<your open ai api key>"
GOOGLE_MAPS_API_KEY = "<google maps api key>"
```

### Run the app
To install requirements: `pip install -r  requirements.txt`

To run the app: `python3 main.py`

### Endpoints

POST request to `/query` with the following body:
```
{
    "address" : "2000 Central Dr Boulder, CO",
    "dietaryRestrictions" : "peanut allergy"
}
```

## Customize
Adjust as desired in `config.py`
- CHAT_MODEL 
  - OpenAI model used.
- MAX_NUMBER_OF_RESTAURANTS 
  - Maximum number of restaurants to retrieve from Google maps search.
  - The more restaurants, the longer the user wait time. 
- RESTAURANT_SEARCH_RADIUS 
  - The radius for the Google map search. In meters. 

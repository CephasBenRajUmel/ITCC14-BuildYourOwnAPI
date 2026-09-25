# Videogame API

## Technology
- Python
- Flask
- SQLite

## Database
Database Contents
- "id": Game ID
- "title": Game Title
- "genre": Game Genre
- "platform": Game Platform
- "release_year": Game Release Year
- "developer": Game Developer
- "rating": Game Rating

## Endpoints
### GET /games
Returns all video games
### GET /games/<id>
Returns a specific video game by its ID
### POST /games
Create a new video game
### PUT /games/<id>
Update a video game by ID
### DELETE /games/<id>
Delete a video game by ID

## Running the API Local
- pip install -r requirements.txt
- python app.py
- Check local house http://127.0.0.1:5000

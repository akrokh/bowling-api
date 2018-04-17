# Bowling REST API

Intended to be used as an API for keeping score in a bowling game (e.g. by a front-end (display) in a bowling alley.  
  
  
## Notes
- Implemented using Flask and Python
- All HTTP requests and return values are in JSON format
- Appropriate HTTP status codes are returned for success and error
- Results are not backed to a database, they are valid only while the server is running
- Intended use case:
  - Create players  
  - Pass in data for each player's ball roll  
  - Get updated score (to display)  
  - Start a new game (reset)  
  
  Example (using curl):  
  curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Bob"}' http://localhost:5000/bowling/api/players  
  curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Bob", "pinsDown":10}' http://localhost:5000/bowling/api/players/roll  
  curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/bowling/api/players  
  etc.  

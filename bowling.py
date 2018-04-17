#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request

app = Flask(__name__)

# Global constants
MAX_ROLLS = 21
MAX_PINS_DOWN = 10
MAX_FRAMES = 10

     
# Returns the total score for a given player (sequence of rolls)
def computeScore(rolls):
    score = 0
    rollIndex = 0
    frameIndex = 0
    
    def isStrike():
        return rolls[rollIndex] == MAX_PINS_DOWN
        
    def isSpare():
        return rolls[rollIndex] + rolls[rollIndex+1] == MAX_PINS_DOWN
 
    while (frameIndex < MAX_FRAMES):
        if (isStrike()):    # Add next two rolls
            score += MAX_PINS_DOWN + rolls[rollIndex+1] + rolls[rollIndex+2]
            rollIndex += 1
        elif (isSpare()):   # Add next roll
            score += MAX_PINS_DOWN + rolls[rollIndex+2]
            rollIndex += 2
        else:               # Only score the current frame
            score += rolls[rollIndex] + rolls[rollIndex+1]
            rollIndex += 2

        frameIndex += 1
    
    return score


players = []    #Initial empty player list

# HTTP requests

# Reset all players (start new game)
@app.route('/bowling/api/players', methods=['DELETE'])
def resetAll():
    players[:] = []

    return 200
    
    
# Return all players
@app.route('/bowling/api/players', methods=['GET'])
def getPlayers():
    return jsonify({'players': players})


# Return a single player
@app.route('/bowling/api/players/<string:name>', methods=['GET'])
def getPlayer(name):
    player = [player for player in players if player['name'] == name]
    if (not player):
        abort(404)
    return jsonify({'player': player[0]})
    

# Add a player
@app.route('/bowling/api/players', methods=['POST'])
def createPlayer():
    if not request.json or not 'name' in request.json:
        abort(400)
        
    existingPlayer = [player for player in players if player['name'] == request.json['name']]
    if (existingPlayer):
        return jsonify({'player': existingPlayer[0]}), 409      #player already exists
        
    player = {
        'name': request.json['name'],
        'score': 0,
        'rolls': [0] * MAX_ROLLS,
        'rollNum': 0,
        'done': False
    }
    players.append(player)
    
    return jsonify({'player': player}), 201     #created new player
    

# A single roll for a given player
# Updates and returns the score
@app.route('/bowling/api/players/roll', methods=['PUT'])
def updateScore():
    if not request.json or not 'name' in request.json or not 'pinsDown' in request.json:
        abort(400)  #invalid request
    
    player = [player for player in players if player['name'] == request.json['name']]

    pinsDown = int(request.json['pinsDown'])

    if (not player):
        abort(404)  #player not found
        
    if (pinsDown < 0 or pinsDown > MAX_PINS_DOWN):    
        abort(400)  #invalid request
            
    player = player[0]

    # Update the player's rolls list
    rollNum = player['rollNum']
    player['rolls'][rollNum] = pinsDown
        
    # Update score
    player['score'] = computeScore(player['rolls'])
    
    # Update current roll number
    rollNum += 1
    player['rollNum'] = rollNum
    
    return jsonify({'score': player['score']}), 200     #updated player score successfully
  
    
 # Run the app   
if __name__ == '__main__':
    app.run(debug=True)
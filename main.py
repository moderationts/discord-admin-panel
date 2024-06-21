import requests,secrets
from flask import Flask, request,send_from_directory
from discord import Discord
from lightdb import LightDB

app = Flask("")

db = LightDB('./db.json') # database to store fake data

discord = Discord()

@app.route('/')
def home():
    return send_from_directory('./',"index.html")

@app.route('/api/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)


# userProfile: /users/:id/profile (GET)
@app.route('/users/<id>/profile')
def userProfile(id):
    if id == "@me":
        return { "message": "Unkown user", "code":0}
    r = discord.get("users/"+id+"/profile")
    user = r.json()

    user["archives"] = db.get('archives').get(id,[]) 
    user["infractions"] = db.get('audit-log').get(id,[]) 
    print(user)
    return user

@app.route('/api/users/<id>')
def user(id):
    if id == "@me":
        return { "message": "Unkown user", "code":0}
    r = discord.get("users/"+id)
    return r.json()

# userInfractions: /users/:id/audit-log (GET,POST)
@app.route('/users/<id>/audit-log',methods=["GET","POST"])
def userInfractions(id):

    if request.method == "GET":
        return db.get("audit-log").get(id,[])
    if request.method == "POST":
        data = request.json 
        data['_id'] = secrets.token_hex(10)
        real = db.get("audit-log")
        if real.get(id):
            real = db.get("audit-log")
            temp = real.get(id)
            temp.append(data)
            db.set("audit-log",real)
            return {}
        real[id] = [data]
        db.set("audit-log",real) 
        return {"infractions":db.get("audit-log").get(id,[])}
    
# archives: /archives/:id (POST)
@app.route('/api/archives/<id>',methods=["GET",'POST'])
def archives(id):
    if request.method == "GET":
        return db.get("archives").get(id,[])
    data = request.json 
    data['_id'] = secrets.token_hex(10)
    real = db.get("archives")
    if real.get(id):
        real = db.get("archives")
        temp = real.get(id)
        temp.append(data)
        db.set("archives",real)
        return {}
    real[id] = [data]
    db.set("archives",real) 
    return {}    

@app.route('/api/guilds/<id>')
def guild(id):
    return discord.get("/guilds/"+id+"?with_counts=true").json()

@app.route('/api/guilds/<id>/channels')
def guild_channels(id):
    return discord.get("/guilds/"+id+"/channels").json()

@app.route('/api/guildss')
def guilds(id):
    return discord.get("/guilds/"+id+"/channels").json()


if __name__ == "__main__":
    app.run(port=80)

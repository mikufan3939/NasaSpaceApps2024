from flask import Flask, redirect, render_template, request  
from datetime import datetime
from helper import getNDVI
app = Flask(__name__)
imageId=0

@app.route("/map", methods=["GET", "POST"])
async def map():
    global imageId
    if request.method=="GET":
        return render_template("mapa.html")
    else:
        cords=request.get_json()
        print(cords[0])
        ndviImage= await getNDVI(cords[0],cords[1],cords[2],cords[3])
        ndviImage.save("static/images/nvdi"+str(imageId)+".jpeg")
        imageId=imageId+1
        return redirect("/nvdi")

@app.route("/nvdi", methods=["GET"])
def nvdi():
    global imageId
    return render_template("nvdi.html", imageId=imageId)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
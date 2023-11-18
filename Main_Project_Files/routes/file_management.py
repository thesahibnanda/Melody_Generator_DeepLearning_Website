from flask import Flask, jsonify, request, Blueprint, session, render_template
from model_building.melody_generator import MelodyGenerator

# Initiating Blueprint
file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/result', methods = ["POST"])
def melody_generation():
    try:
        if request.method == "POST":
            if 'midiFile' not in request.files:
                return jsonify({"Error": "No File Found"})
            
            file = request.files['midiFile']

            if file.filename == '':
                return jsonify({"Error": "No File Found"})
            
            file.save(file.filename)
            # File Is Saved

            MelodyGenerator().midi_accept(file.filename)

            


            return render_template('final.html')
        else:
            return jsonify({"Error": "POST Method Required"}) 
    except Exception as e:
        return jsonify({"Error": str(e)})
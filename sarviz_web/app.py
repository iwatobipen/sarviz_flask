# this is test app for SARviz.
# Author iwatobipen
# Licence FREE and prease enjoy chemoinfromatics

from flask import Flask
from flask import render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from chemolib import sarviz
import pickle
from rdkit import Chem

class Smiles( Form ):
    smi = StringField( "- mol to smiles", validators=[ DataRequired() ] )

def create_app():
    app = Flask( __name__ )
    Bootstrap( app )
    return app

app = create_app()

@app.route( "/top/" )
def top():
    return render_template( "top.html" )


@app.route( "/predict/", methods = ( "GET", "POST" ) )
def predict():
    actcls = { -1: "non-active", 1: "active" }
    form = Smiles( csrf_enabled=False )
    if form.validate_on_submit():
        smi = form.smi.data
        try:
            mol = Chem.MolFromSmiles( smi )

        except:
            mol = Chem.MolFromSmiles( "c1ccccc1" )
        # get molwt, mollogp, tpsa
        molprop = sarviz.molprop_calc( mol )
        # predict active / nonactive as integer and save image.
        res, fname = sarviz.mapperfunc( mol )
        res = int( res[0] )
        return render_template( "result.html", res = actcls[res], fname=fname, molprop = molprop )
    else:
        return render_template( "query.html", form = form, fname="dummy.png" )

if __name__ == "__main__":
    app.run( debug = True )

from flask import Flask,request,render_template
import os
import json
from glob import glob
import subprocess

app=Flask(__name__)


@app.route('/upload',methods=['POST'])
def upload_data():
    if not os.path.exists('upload'):
        os.mkdir('upload')
    source=request.files['source']
    driving=request.files['driving']
    source.save(os.path.join('upload',source.filename))
    driving.save(os.path.join('upload',driving.filename))
    return 'upload sussess',200
@app.route('/data')
def get_data():
    source_lists = glob('upload/*.png')
    driving_lists = glob('upload/*.mp4')
    print(source_lists,driving_lists)
    return json.dumps({'source':source_lists,'driving':driving_lists}),200
@app.route('/job',methods=['POST'])
def make_job():
    source_path=request.values['source']
    driving_path=request.values['driving']
    print(source_path,driving_path)
    cmd =f'python animation_demo.py --config config/end2end.yaml --source_image_path {source_path} --driving {driving_path} --adapt_scale --relative '

    subprocess.run(cmd)
    return 'sussess',200



@app.route('/')
def index():
    return render_template("upload.html")
@app.route('/select')
def select():
    return render_template('select.html')

if __name__=='__main__':
    app.run(debug=True)
import os
from flask import Flask, jsonify, send_file

app = Flask(__name__)

@app.route('/servinfo')
def home():
    return "OK"
    
@app.route('/pkg/<pkgname>')
def pkg(pkgname):
    try:
        if os.path.exists('packages/'+pkgname+'.apk'):
            return send_file('packages/'+pkgname+'.apk')
        else:
            return "400"
    except:
        return "500"
        
@app.route('/pkgcheck/<pkgname>')
def pkg(pkgname):
    try:
        if os.path.exists('packages/'+pkgname+'.apk'):
            return "200"
        else:
            return "400"
    except:
        return "500"
        
if __name__ == "__main__":
    app.run()
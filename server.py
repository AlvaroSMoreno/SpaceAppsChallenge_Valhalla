from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html');

@app.route('/arduino')
def arduino():
	vel = request.args.get('vel')
	gyro = request.args.get('gyro')
	return {"status": "success", "vel":vel, "gyro":gyro}

@app.route('/phone')
def phone():
	gyroX = request.args.get('gyroX')
	gyroY = request.args.get('gyroY')
	gyroZ = request.args.get('gyroZ')
	return {"status": "success", "gyro":{"x":gyroX, "y": gyroY, "z":gyroZ}}

if __name__ == '__main__':
	app.run(debug=True, port=3000)
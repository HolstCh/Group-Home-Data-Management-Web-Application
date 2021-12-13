from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
	return redirect(url_for("home"))

@app.route("/home", methods = ["POST", "GET"])
def home():
	if request.method == 'POST':
		user = request.form["inputUsername"]
		return redirect(url_for("account", usr = user))
	else :
		return render_template('designApp.html')

@app.route("/account/<usr>")
def account(usr):
	return render_template('designAcc.html', usr = usr)

if __name__ == "__main__":
	app.run()




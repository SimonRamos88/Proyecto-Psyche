from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def definicion():
    return render_template("definicion.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/jack')
def jack():
    return render_template("jack.html")

@app.route('/jade')
def jade():
    return render_template("jade.html")
        
if __name__ == '__main__':
    app.run(debug=True)




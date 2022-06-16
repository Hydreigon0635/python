from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        print('POSTされたIDは？'  + str(request.form['id']))
        print('POSTされたPASSWORDは？' + 
        str(request.form['pwd']))
        return render_template('form.html')
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run(port = 8000, debug = True)
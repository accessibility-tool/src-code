from os import name
import final, link_rec, cluster_info, section_links, section_rec, summary_model
from flask import Flask, request
import training
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
@cross_origin()
def hello_world():
    return {'message':"Hello, World"}

@app.route("/page_name/<page_name>", methods=['GET'])
@cross_origin()
def initialising_function(page_name):
    final.final(page_name)
    return {'message':page_name}

@app.route("/links/<page_name>/<int:num>", methods=['GET'])
@cross_origin()
def link_recommendation(page_name, num):
    return {'recommendations':link_rec.link_rec(page_name, num)}


@app.route("/cluster/<page_name>/<int:num>", methods=['GET'])
@cross_origin()
def cluster_recommendation(page_name, num):
    return {'recommendations':cluster_info.get_cluster_links(page_name, num)}

@app.route("/section/<page_name>/<int:num>", methods=['GET'])
@cross_origin()
def section_recommendation(page_name, num):
    sec_links=section_links.section_text(page_name)
    final_dict=section_rec.get_rec(sec_links, num, page_name)
    return {'recommendations':final_dict}

@app.route("/chatbot/<page_name>")
#@cross_origin()
def chatbot(page_name):
    if page_name=="favicon.ico":
        pass
    training.train(page_name)
    return {'message':'Bot trained'}

@app.route("/chatbot/get")
#@cross_origin()
def get_bot_response():
    userText = request.args.get('msg')
    userText = userText.lower()
    print(userText)
    return {'message':training.getResponse(userText)}

@app.route('/summary/<page_name>')
@cross_origin()
def summarize(page_name):
    x = summary_model.get_summary(page_name)
    return {'summary':x}

if __name__=='__main__':
    print("HI")
    app.run(host='127.0.0.1', port=12000, threaded=True)


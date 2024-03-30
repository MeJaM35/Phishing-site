import uvicorn
from fastapi import FastAPI, Request
import joblib,os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import numpy as np
from pydantic import BaseModel







app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

#pkl
phish_model = open('phishing.pkl','rb')
phish_model_ls = joblib.load(phish_model)



tfidf = joblib.load(open('vectorizer.pkl', 'rb'))
spam = joblib.load(open('model.pkl', 'rb'))


# 1. preprocess
# 2. vectorize
# 3. display
# 4. predict

@app.get('/spam/', response_class=HTMLResponse)
async def spam(request:Request):
	return templates.TemplateResponse(
		request=request, name='spam.html'
	)

@app.get('/spam/predict/{feature}')
async def spam_predict(request:Request, features):
	return templates.TemplateRessponse(
		request=request, name='res.html', context = {}
	)

@app.get('/', response_class=HTMLResponse)
async def index(request:Request):
	return templates.TemplateResponse(
		request=request, name='index.html'

	)



# ML Aspect
@app.get('/predict/{feature}')
async def predict(request:Request, features):
	X_predict = []
	X_predict.append(str(features))
	y_Predict = phish_model_ls.predict(X_predict)
	if y_Predict == 'bad':
		result = "Phishing Site"
	else:
		result = "not a Phishing Site"



	return templates.TemplateResponse(
		request=request, name='result.html', 	context = {
		"result": result,
		"feature": features,
	}

	

	)
if __name__ == '__main__':
	uvicorn.run(app,host="127.0.0.1",port=33)
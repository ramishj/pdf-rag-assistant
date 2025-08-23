FROM python:slim
 
WORKDIR /app
COPY . .
 
RUN pip install -r requirements.txt
 
CMD ["sh", "-c", "streamlit run app.py ${PORT:+--server.port=$PORT} --server.address=0.0.0.0"]
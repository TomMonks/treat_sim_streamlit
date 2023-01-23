FROM python3.8

# streamlit working dir
WORKDIR /app

# copy the pip requirements file 
COPY requirements.txt ./requirements.txt

# pip install the requirements
RUN pip3 install -r requirement.txt

# expose port 8989
EXPOSE 8989

# copy everything across - note dockerignore will avoid bloat
COPY . /app

# use streamlit by default
ENTRYPOINT ["streamlit", "run"]

# command to run - this is run when docker image is opened (by streamlit)
# equiv to `streamlit run Overview.py` 
CMD ["Overview.py"]



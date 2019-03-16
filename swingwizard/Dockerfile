FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    git python3-dev gcc && rm -rf /var/lib/apt/lists/*

RUN conda update -n base -c defaults conda
# RUN conda create -n env
# RUN echo "source activate env" > ~/.bashrc
# ENV PATH /opt/conda/envs/env/bin:$PATH
# RUN conda activate env

RUN conda install -c pytorch -c fastai fastai==1.0.49 -y
RUN conda install -c anaconda flask==1.0.2 -y
RUN conda install -c conda-forge flask-sqlalchemy==2.3.2 -y
RUN conda install -c conda-forge flask-migrate==2.4.0 -y
RUN conda install -c anaconda flask-login==0.4.1 -y
RUN conda install -c conda-forge av==6.1.2 -y
RUN conda install -c anaconda flask-wtf==0.14.2 -y

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt --upgrade


COPY app app/
COPY migrations migrations/
COPY models models/
COPY app.db app.db
COPY config.py config.py
COPY swingwizard.py swingwizard.py
COPY swingwizard.py config.py boot.sh ./
# RUN chmod a+x boot.sh
# RUN conda init bash && conda activate env
# RUN conda activate env
# ENV FLASK_APP swingwizard.py

RUN python swingwizard.py

EXPOSE 5000
# ENTRYPOINT [ "./boot.sh" ]

CMD ["python", "swingwizard.py", "serve"]

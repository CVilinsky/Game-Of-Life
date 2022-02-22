#DockerFile, Image, Container
FROM python:3.10.1
ADD  ChenVilinsky_ConwaysGameOfLife.py .
RUN pip install pygame

CMD [ "python", "./ChenVilinsky_ConwaysGameOfLife.py" ]

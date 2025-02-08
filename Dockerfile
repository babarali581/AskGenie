FROM python:3.10

USER root

WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt .

RUN apt update -y

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
EXPOSE 9000

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]

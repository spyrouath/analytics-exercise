# EFood Customer Segmentation Analysis/Application 

## How to execute the project locally without Docker

Make sure your working directory is */segmentation_app and simply run the index.py
Then you can see the app in your browser at [local link](http://0.0.0.0:8050)

## How to execute the project locally with Docker

Download and install Docker

Go to project folder in command line

Run the following commands:

docker build -t segmentation_app .

docker run -p 8050:8050 -v "$(pwd)"/app:/app -it --rm segmentation_app

open the browser at 0.0.0.0:8050

## How to access it directly

[segmentation_app](https://anexercise.azurewebsites.net/segmentation_app/segments)


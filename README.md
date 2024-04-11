### songuess

# Advanced Databases Course Project
![image](https://github.com/cmkuczun/songuess/assets/93489352/259ce3dd-e34b-4937-bb9e-0a0216327ef6)

Data used based on dataset found [here]([url](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)).


## Docker Instructions

- Two Environments:
+ Stage
    Use for local development.
    To run both backend and frontend in stage environment, run:
    `docker compose --profile stage up`
    Edits saved to files will be reflected in real-time

+ Production
    Use on AWS machine for deployment
    To run both backend and frontend in production environment, run:
    `docker build`
    `docker compose --profile prod up`
    This updates the container and then runs it.


    

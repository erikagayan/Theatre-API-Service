# Theatre API Service


## Features
In theatre api service you can see list of genres, actors, plays and theatre halls. Also you can reservate a ticker for play


# Installation
1. Docker: [Install Docker](https://docs.docker.com/get-docker/)
- If you want to use PostgreSQL: [Install PostgreSQL](https://www.postgresql.org/download/)
2. Clone this repository to your local machine: https://github.com/erikagayan/Theatre-API-Service
3. Navigate to the project directory
4. Create `.env` file and define environmental variables by following '.env.sample'.
5. Build the Docker container using Docker Compose:`docker-compose build`
6. Access list of containers: `docker ps -a`
7. Create a superuser for accessing the Django admin panel and API: `docker exec -it <container_id here> python manage.py createsuperuser`
8. Start the Docker container: `docker-compose up` 
9. To stop the container, use: `docker-compose down`


## Theatre DB scheme
![DB](images/DB%20scheme.png)


## Theatre example
![api root](images/Theatre%20api%20root.png)
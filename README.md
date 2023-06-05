![YaMDb deploy](https://github.com/mikeburn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg) 
 
# Server
http://51.250.24.168/api/v1/
  
# My_YaMDb 
This is a REST API project for the YaMDb service, which is a platform for collecting reviews of movies, books, or music. 
 
## Description 
The My_YaMDb project aims to gather user reviews for various works. The works are categorized into "Books," "Movies," and "Music." The list of categories can be expanded to include categories like "Visual Arts" or "Jewelry." 
 
### How to Run the Project: 
The following instructions are specific to Linux operating systems. 
 
Check if Docker is installed by running the following command: 
```bash 
docker -v 
``` 
Verify that the latest version of Compose is installed. You can also refer to the official installation guide. 
 
 
Clone the repository and navigate to it: 
```bash 
git clone https://github.com/mikeburn/yamdb_final  
cd api_yamdb 
``` 
 
Go to the directory with the docker-compose.yaml file: 
```bash 
cd infra 
``` 
 
 
Create the .env file based on the provided .env.template. 
 
Launch docker-compose:  
 
   ```bash 
   docker-compose up -d 
   ``` 
 
 
Run the migrations: 
```bash 
docker-compose exec web python manage.py makemigrations 
``` 
```bash 
docker-compose exec web python manage.py migrate 
``` 
 
Create a superuser: 
```bash 
docker-compose exec web python manage.py createsuperuser 
``` 
 
Collect static files: 
```bash 
docker-compose exec web python manage.py collectstatic --no-input 
``` 
 
Populate the database with test data: 
```bash 
cd api_yamdb && python manage.py loaddata ../infra/fixtures.json 
``` 
 
Stop the containers: 
```bash 
docker-compose down -v 
```

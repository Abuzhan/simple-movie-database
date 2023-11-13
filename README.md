# Simple movie database

## Description
This service is responsible for managing movies and integrating with an external API in order to comply with coding challenge requirements. The service owns the entities, the domain logic of reading and managing movies as well as exposing external API and integration with OMDB API (3-rd party tool).

## Implementation
### Current tech stack
I mainly leaned towards python web frameworks and sql databases as main starting point. Below you can find all frameworks and libraries used in this project with short reasoning behind each choice.

- Python - language that I am quite familiar with and main requirement of the coding challenge. 
- Sanic - async web framework that I have been using for a while now. It is quite fast and easy to use. It is also quite similar to Flask and allows less opinionated approach to building web services.
- PostgresQL - a great choice for relational database. I was mainly comparing Google Firestore and Postgres when deciding between document or relational database to choose, and the main reason of going with latter was that it is fairly likely that we would want to search movies and related data by more complex queries, where the relational database would be a better choice.
There is also always an option to combine both for different parts of data.
- Hexagonal architecture (Ports and Adapters) - in order have infrastructure-agnostic domain implementation and better
maintainability and testability.
- SQLAlchemy - well known and popular ORM library for python. It is quite easy to use and allows to switch between different databases without changing the code. It also allows using raw SQL queries if needed. 
- Aiohttp - one of the main asynchronous HTTP Client/Server for asyncio and Python. Fast enough and versatile.
- Docker + Supervisord - for containerization and easier deployment.
- Pre-commit + Black - for code formatting and linting.
- Pytest + Aioresponses + Sanic_testing - for testing.


### API Flows
- #### Get all movies
    `[GET] /movies.list` - returns all movies in the database. `page` and `number_of_records` can be passed as parameters for pagination, otherwise defaults to `page=1` and `number_of_records=10`.

- #### Get movie by title
    `[GET] /movies.get`- returns movie by title. `title` is a required parameter.

- #### Create movie
    `[POST] /movies.create` - creates a movie in the database. `title` is a required in the request body.

- #### Delete movie
    `[DELETE] /movies.delete/<imdb_id:str>` - deletes a movie from the database by imdb_id. This endpoint is protected and requires api token to access.

- #### Login
    `[POST] /login` - returns api token. This endpoint is very simple and doesn't require any authentication. It is used only for the purpose of this coding challenge and returns JWT token.

### Deployment
The service is deployed on Google Cloud Platform (GCP) using Google Cloud Run service. It is a fully managed serverless container platform that automatically scales your stateless containers. It is also quite easy to deploy and manage. The service is deployed using Dockerfile and Cloud Build with Dockerfile.
The service is also connected to Google Cloud SQL database (PostgresQL).

Service is deployed and can be accessed by the url - https://simple-movie-database-rztgjpsruq-ew.a.run.app

## Future improvements
- Better error handling and logging.
- Better test coverage. Due to time constraints there are a few tests missing that felt repetitive and not necessary to implement, but if this becomes a real life application it would be a good idea to cover all endpoints and main functions with tests. 
- Supporting different users and authentication on the API and integration levels. Current authentication is very basic and serves more of as an example of using decorators for token validation and logic in general. However, for the app to be user-friendly and secure it is necessary to introduce user models with possibilities to set/update credentials and initializing sessions.  
- Transactions and Idempotency. This is a very important aspect of any system, but it is not needed in this service at the moment due to simplicity of flows. In the future some flows (fetching external data, storing data in the database, updating external integrations with new data) might require atomic approach to support many writes (dual writes problem) triggered by the same action. While drawbacks of dual writes are obvious, it is vital to break the flow into atomic phases, which are retryable and idempotent. This can be achieved by using db callbacks, event driven flows, asynchronous tasks, or setting up domain transactions. The last one is more of a last resort, as it is a very complex solution and requires a lot of effort to implement and maintain.
- Separating main movie service and OMDB integration into separate microservices. This will help if codebase is being managed by a bigger team of engineers and will allow to scale each service separately. It will also allow using generic agnostic port for different 3-rd party integrations.
- Introducing deployment phases and CI/CD for pushing the service to production and enable agile way of working. (Docker, Terraform, Kubernetes, Jenkins, DigitalOcean, etc.). I usually prefer IaC approach in any DevOps job, so deploying this service to GCP with something like Terraform including proper monitoring and alerting would be a good idea.

## Surprise part
I wasn't sure if I should really build something cool to showcase by skills, but in the end decided to just go with old but gold easter egg on [teapot](https://en.wikipedia.org/wiki/Hyper_Text_Coffee_Pot_Control_Protocol). I hope it makes you smile.

## Final words
I tried to take this challenge closer to real-life problem and produce a solution that would be easy to maintain and extend. I also tried to keep it simple and not over-engineer it. I hope you will enjoy reading it as much as I enjoyed writing it.



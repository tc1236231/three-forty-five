# People

The People applicaiton provides a layer of abstraction between the databases that hold people
data and the public front ends that provide access to the data in them. See the
*people/routes/web.php* file for the URLs to access the data.

## IMPORTANT NOTIFICATION

** Don't save any real secrets in this repo while this notification is here!!**

## Directory Overview

The directory with this file in it from now on will be refered to as the **project root**. 
It contians the configuration information Docker Environment and is also where the Docker
commands should be run.

The sub-directory *people* is the root of the PHP application. It will be referred to from 
now on as the **application root** or **app root**.

In general, readme.md files will be added to the directories that contain files created or
modified by MNHS staff. If a directory does not have a readme.md file or a readme.md file
dated before 1/1/2019 it was created as part of the set up of the dev environment.

## Getting Started

To download a copy of this repository on your computer using the git command:

`git clone https://gitlab.com/mnhs/php/people.git`

### Prerequisites
Things you will need to have installed before being able to run this are:

  * [Docker](https://www.docker.com/products/docker-desktop)
  * [PHP 7.X or higher](http://php.net/downloads.php)

### Dev Environment Setup
Unless otherwise noted, run all installs and commands in the **project root** directory.

1. If necessary switch to the approriate git branch.
1. [Install Composer](https://getcomposer.org/download/) inside the project root. 
The exact method of doing this depends on if you are using a Mac, Windows or Linux box. Follow the
instructions on the page you are shown.
2. Enter at the command prompt `php composer.phar install -d people` - this will create the vendor directory in the 
**app root**.
3. At the command prompt enter `cp docker-compose.override.example.yml docker-compose.override.yml` 
to build the Docker image. This step only has to be done once per clone of the repository.
4. At the command prompt enter `docker-compose up` to start Docker. 
Note, if you are not returned to a command prompt, like on Windows computers, this window must remain 
open for Docker to continue to run properly.
5. To test that the environment is up and running corretly open a browser and go to `http:///localhost:8000`. 
If all worked, you should see a response that the People app is running.
6. If needed open another window and make sure you are in the **project root** directory. At the command prompt 
enter the command `cp people/.env.example people/.env` to copy a configuration file.
7. In the same window as step 6 enter one of the following commands to populate
the database. See the **MySQL Admin** section for the credentials. 

   `winpty docker-compose exec web bash -c "php artisan db:seed"` **for Windows**  
 
   `docker-compose exec web bash -c "php artisan db:seed"` **for Macs**  
   
8. When finished use the `docker-compose down` command to shut the docker environment down.. 
If Docker is running in a differnt window, like on Windows computers, go to that window first and press `<Ctrl-C>`
to return to the command prompt, then enter the down command at that command prompt.

#### Starting the Dev Environment once it is setup
After you have completed all of the steps above you can shorten the start up of the 
Docker environment to the following steps, as long as you have not cloned the repository.

1. At the command prompt enter `docker-compose up` to start Docker. 
Note, if you are not returned to a command prompt, like on Windows computers, this window must remain 
open for Docker to continue to run properly.
2. To test that the environment is up and running corretly open a browser and go to `http:///localhost:8000`. 
If all worked, you should see a response that the People app is running.
3. If needed open another window and make sure you are in the **project root** enter one of the following commands to populate
the database. See the **MySQL Admin** section for the credentials.

   `winpty docker-compose exec web bash -c "php artisan db:seed"` **for Windows**  
 
   `docker-compose exec web bash -c "php artisan db:seed"` **for Macs**  
   
4. When finished use the `docker-compose down` command to shut the docker environment down.. 
If Docker is running in a differnt window, like on Windows computers, go to that window first and press `<Ctrl-C>`
to return to the command prompt, then enter the down command at that command prompt.

#### MySQL Admin
To see what records were added to the database, and you do need to know so you can access them, point your browser
to `http://localhost:8080` Use the following credentials to get into MySQL:

```
System: MySQL
Server: db
Username: root
Password: password
Database: [leave blank]
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [PHP 7.X or higher](http://php.net/downloads.php)
* [Lumen framework](https://lumen.laravel.com) - which is s subset of [Laravel](https://laravel.com/)
* [Composer](https://getcomposer.org/download/)
* [Docker](https://www.docker.com/products/docker-desktop)

## Handy to Have
* [Application Development Environment](https://www.techopedia.com/definition/27850/application-development-environment-ade)  
  such as [Postman](https://www.getpostman.com/) to make testing of POST, PUT and DELETE requests easier
* [Account on authO](https://auth0.com/signup) or whatever service is providing authentication


## Versioning -- Is this needed?

We use [SemVer](http://semver.org/) for versioning. For the versions availabel, see the [tags on this repository](https://gitlab.com/mnhs/php/people/tags). 

## Authors

* Marj Kelly
* Samuel Courtier

## App root directory overview

This application was developed using the Lumen Framework. As such you will find a readme.md
file that is part of the install of that and has not been modified since it could be overwritten
later by upgrades etc. Because of that the overview for that directory is here.

```
 /app - core code of the application
 /bootstrap - holds the app.php file which is used to bootstrap the application
 /config - holds the database.php file which configs the database connections
 /database - holds the code that will populate test and development versions of the database
 /public - holds the index.php file which is the standard entry point for Lumen applicaitons
 /resources - holds resources such as Javascript files, views, language files, etc
 /routes - holds the web.php file which is where the application routes are defined
 /storage - holds things created by the framework such as logs, caches, files, etc.
 /tests - automated testing scripts
 /vendor - contains the Composer dependencies.
```


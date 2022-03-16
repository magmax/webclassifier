bogofilter applied on webs with a web interface.

The more pages you classifies by hand, the better it will work.

# basic usage

1. clone the repository: `git clone git@github.com:magmax/webclassifier.git`
2. run docker-compose: `docker-compose up -d`
4. initialize the database with `docker-compose exec web python manage.py migrate`
4. go to localhost:8000
5. add some urls
6. classify some of them by hand
7. press the "Process All" button.

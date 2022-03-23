# ChatApp  #


## Architecture ##
 

## Run ##

0. move to project root folder

1. Install requirements
```bash
pip install -r requirements
```
2. Create a MySQL database
```sql
CREATE DATABASE oo_community CHARACTER SET utf8;
```
4. Start Redis Server
```bash
docker run -p 6379:6379 -d redis:5
```
5. Init database
```bash
python manage.py migrate
```
6. Run development server
```bash
python manage.py runserver
```


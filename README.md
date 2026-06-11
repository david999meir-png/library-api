# library - api #

## Project description ##

### Server-side system ###  
The system will manage a list of books and a list of members with the option to add or remove books as well as the option to add or remove members.  

The system will monitor the number of books per member and issue organized reports on the status of the books and members.
##
# docker requirements #
## run this docker first! ##
```docker run mysql_library my-mysql \```  
```-e MYSQL_ROOT_PASSWORE=root \```  
```-e MYSQL_DATABASE=library_db \```  
```-p 3306:3306 \```  
```-d mysql:latest```  
##
# folders structure #  
library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore  
##
# tables structure #  
### books table ###  
| TYPE | FIELD | MORE |
| :---- | :--------------- |  ------ |
id |INT PRIMARY KEY  | AUTO_INCREMENT     
title  | VARCHAR(50) | NOT NOLL
author  | VARCHAR(50) | NOT NULL
genre  | ENUM(Fiction, Non-Fiction, Science, History, Other) | NOT NULL  
is_available  | BOOLEAN | NOT NULL
borrowed_by_member  | member id | NOT NULL
##   
### members ###  
| TYPE | FIELD | MORE |
| :---- | :--------------- |  ------ |
id |INT PRIMARY KEY  | AUTO_INCREMENT     
name  | VARCHAR(50) | NOT NULL
email  | UNIQUE | NOT NULL
is_active  BOOLEAN | NOT NULL
tatal_borrows | INT | NOT NULL

##
# system rules #
| number | subject | rule |
| :- | :-------- | :------------------------ |
1 | create book |the user sends `title, author, genre` the system will add ```is_available=True``` ```borrowed_by=NULL```  
2 | genre | must be / Non-Fiction / Science / History / Other . **oder value will raise an error**
3 | create member | the user sends name and email the system will add `is_active=True` and `total_borrows=0`
4 | email | must be unique **if not, errer will be returned**  
5 | unactive member | if `is_active=False` the member can't borrow  
6 |unavailble book | you can't borrow a book if the book alrady borrowed  
7 | max books | the max books that member can borrow is only 3  
8 | return book | only the member who borrow can return the book

##
# endpoints #
## books ##  
| method | endpoint | description |  
| :----- | :------------------- | :------------- |  
POST | /books | create book  
GET | /books | all books  
GET | /books/{id} | book by id
PATCH | /books/{id} | update book  
PATCH | /books/{id}/borrow/{member_id} | borrow book to member  
PATCH | /books/{id}/retuen/{member_id} | return book from member 

##
## members ##  
| method | endpoint | description |  
| :----- | :------------------- | :------------- |  
POST |/members | create member
GET |/members | all members  
GET |/members/{id} | members by id  
PATCH |/members/{id} | update member  
PATCH |/members/{id}/deactive | deactive member  
PATCH |/members/{id}/active | active member   

##
## reports ##  
| method | endpoint | description |
| :----- | :------------------- | :------------- |  
GET | /reports/summay | general report
GET | /reports/books-by-genre | report by genre
GET | /reports/top-member | the most active member

# system  flow #  
http requests -> fastapi -> router -> endpoints -> db_dle -> respond
##
# Running instructions #  
## programs ##
- python 3.14
- docker
## python library ##
`python -m venv .venv`
### requierements ###
- fastapi
- uvicorn
- mysql.connector
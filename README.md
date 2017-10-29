# smartexLab-api
## test project

### User queries
/users GET (all users)
/users POST query fields { "last_name":"", "first_name":"","patronymic_name":"","password": "","email":""}
/users/id - GET (one user)
/users/id - DELETE (delete one user) query field {“password”: “пароль пользователя”}

### User-cards queries
/cards GET (all cards)
/users/id/cards - GET (all cards one user)
/users/id/cards -POST (create card for user) query field {“password”: “пароль пользователя”}

Admin panel added to view databases
You can also view the logfile on a separate page

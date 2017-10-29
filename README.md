# smartexLab-api
## test project

### User queries
/users GET (all users)<br>
/users POST (create user) query fields { "last_name":"", "first_name":"","patronymic_name":"","password": "","email":""}<br>
/users/id - GET (one user)<br>
/users/id - DELETE (delete one user) query field {“password”: “_______”}<br>

### User-cards queries
/cards GET (all cards)
/users/id/cards - GET (all cards one user)<br>
/users/id/cards -POST (create card for user) query field {“password”: “_________”}<br>

<p>Admin panel added to view databases.<br>
<p>You can also view the logfile on a separate page

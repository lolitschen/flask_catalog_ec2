#My Catalog Application

**Description**: A angular/flask application that allows users to login using existing google plus accounts and list items. Items have an associated price, description, name, and image (user uploaded) that will be stored in the database after being added. Users may edit/delete item listings at any time and can browse through all listings.

##http://ec2-52-25-58-187.us-west-2.compute.amazonaws.com/

##SSH Details
**Server IP:** 52.25.58.187
**SSH Port:** 2200

User:grader

RSA Key:submission comments

##Server setup summary
1. Packages update & upgrade via apt-get, ensure time is UTC
2. Create user 'student' & grant sudo access via /etc/sudoers.d/student
  1. Generate rsa key on local machine & scp to server for student
  2. Verify password ssh is no longer allowed (key only)
  3. Logout and ssh in as student instead of root
  *Repeat for user 'grader' using given udacity rsa key

3. Setup UFW
  1. deny all incoming, allow all outgoing
  2. change SSH port from 22 to 2200, reload & reboot to apply settings
  3. allow ports (www)80, 2200/tcp, and NTP(123)
  4. enable and test still able to ssh via port 2200

4. Install & Setup Dependencies
  1. Install pip, flask, sqlalchemy, psycopg2, postgresql, bleach, oauth2client, requests, httplib2, PyJWT, apache2
  2. Setup PostgreSQL
    *create roles student (superuser permissions), catalog (CRUD permissions on tables), grant necessary permissions

5. Install git & clone catalog repository
  1. modify db connection string to reflect catalog:pw@localhost/dbname
  2. install under /var/www/applicationname
  3. create a catalog.wsgi file 

6. Configure Apache2
  1. Create catalog.com.conf file, add in location of source directory
  2. sudo a2dissite default
  3. sudo a2ensite
  4. sudo service apache2 reload (and then restart)

7. OAuth Credentials
  * add the ec2 urls to authorized redirect & source urls in google developer console

##Resources

#####Ubuntu Setup:
- http://askubuntu.com/questions/117359/how-do-i-change-the-timezone-to-utc 

#####Postgres: 
- http://www.postgresql.org/docs/9.3/static/
- https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps

#####Apache Setup: 
- https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps

#####Markdown Styling:
- https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

**General Instructions**

Log in with your google plus account and post away!

To post a new item, go to account and click "add new listing."

Your listings will show up in your account profile page if you wish to modify them.

**JSON API Routes**

| Allowed Verbs | Route                                                |
| -------------:|------------------------------------------------------|
|GET            | localhost:8080/api/v1.0/user/<int:user_id>/          |
|GET,POST       | localhost:8080/api/v1.0/item/                        |
|GET,PUT,DELETE | localhost:8080/api/v1.0/item/<int:item_id>/          |
|GET            | localhost:8080/api/v1.0/categories/                  |
|GET            | localhost:8080/api/v1.0/categories/<int:category_id>/|

note: categories are created during creation of items and not supported separately

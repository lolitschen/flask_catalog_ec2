#My Catalog Application

**Description**: A angular/flask application that allows users to login using existing google plus accounts and list items. Items have an associated price, description, name, and image (user uploaded) that will be stored in the database after being added. Users may edit/delete item listings at any time and can browse through all listings.

**To Run**:
1. terminal: vagrant up, vagrant ssh, cd \vagrant\catalog
2. terminal: python database_setup.py
3. terminal: python application.py
4. browser: localhost:8080

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


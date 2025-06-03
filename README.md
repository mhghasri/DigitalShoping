1. Create a new file named .env in the root directory of your project.

2. Replace the values below with your own database information:
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=your_password_here
    DB_NAME=your_database_name_here


# Database Setup for mh-digitalshop

This repository contains the SQL dump file for the `digitalshop` database.

## Importing the Database

To set up the database locally, follow these steps:

### Prerequisites

- MySQL Server installed and running  
- MySQL Workbench or any MySQL client tool  
- Access credentials (username and password) for MySQL

### Steps to Import

1. Open MySQL Workbench (or your preferred MySQL client).

2. Connect to your MySQL server.

3. Open the SQL dump file `digitalshop.sql` included in this repository.

4. Run the entire script to create the database, tables, and insert all the data.

   - Alternatively, from the command line, you can use the following command:

   ```bash
   mysql -u your_username -p < digitalshop.sql

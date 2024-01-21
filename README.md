# Splitwise

A simple backend application to add and manage expenses for users.

---
### Setup -
```
# Commands -

1. git clone https://github.com/kunalbagdare/splitwise.git
2. add credentials to .env
2. flask run
3. celery -A scheduler.tasks worker --loglevel=info
```
---
### Technologies Used -

- **Flask:** A micro web framework.
- **SQLAlchemy:** An ORM for SQL operations.
- **Flask-Smorest:** An extension for Flask that simplifies the creation of REST APIs.
- **Marshmallow:** An object serialization and validation library.
- **Celery:** A distributed task queue for handling asynchronous tasks and run scheduling tasks.
---

### API Endpoints -

1. **Check Status/Health**
   - **URL:** `/status`
   - **Method:** GET
   - **Description:** Check if the application is running and healthy.

2. **Add User**
   - **URL:** `/add-user`
   - **Method:** POST
   - **Description:** Add a new user to the system.

3. **Add Expense**
   - **URL:** `/add-expense`
   - **Method:** POST
   - **Description:** Add a new expense to be shared among users.

4. **List Expenses for a User**
   - **URL:** `/expenses/<user_id>`
   - **Method:** GET
   - **Description:** Get a list of expenses for a specific user.

5. **Get Balance for a User**
   - **URL:** `/balance/<user_id>`
   - **Method:** GET
   - **Description:** Get a balance for a specific user.

6. **Get Balances**
   - **URL:** `/balances`
   - **Method:** GET
   - **Description:** Get balances for all users. Supports optional query parameter `simplify` (true/false) to simplify balances.
---
### User Table -
   - `id`: Primary key, uniquely identifies each user (auto-generated UUID).
   - `name`: Full name of the user.
   - `email`: Email address of the user.
   - `mobile_number`: Mobile number of the user.

### Passbook Table -
   - `id`: Primary key, uniquely identifies each passbook entry (auto-generated UUID).
   - `payer_id`: Foreign key referencing the User Table, indicates the payer in the transaction.
   - `payee_id`: Foreign key referencing the User Table, indicates the payee in the transaction.
   - `expense_id`: Foreign key referencing the Expense Table, links to the specific expense.
   - `amount`: Amount involved in the transaction.
   - `date`: Date and time of the transaction.

### Expense Table -
   - `id`: Primary key, uniquely identifies each expense (auto-generated UUID).
   - `expense_name`: Name or description of the expense.
   - `payer_id`: Foreign key referencing the User Table, indicates the user who paid for the expense.
   - `date`: Date and time when the expense was incurred.
   - `amount`: Total amount of the expense.
   - `expense_type`: Type of expense (EQUAL, EXACT, PERCENT).

### Emailing Service -
- Celery task sends an email everytime an expense is added.
- Celery scheduler sends a weekly email via Celery task to users with their respective amount dues.

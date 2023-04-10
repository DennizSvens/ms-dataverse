# DataverseORM
DataverseORM is a Python module that simplifies working with Microsoft Dataverse by providing a lightweight Object-Relational Mapper (ORM) for querying, creating, updating, and deleting entities. It uses the Dataverse Web API for communication. 

## Installation
```
pip install ms-dataverse
```

## Dependencies
- Python 3.6+

## Usage
To use DataverseORM, import the DataverseORM class from the dataverse_orm.py file:

``` python
from ms_dataverse import DataverseORM
```

Create an instance of the DataverseORM class, passing in the URL to your Dataverse environment and an access token for authentication:

``` python
orm = DataverseORM(dynamics_url="https://your_environment.crm.dynamics.com", access_token="your_access_token")
```


## Authentication
You can obtain an access token using the MSAL Python package available at:
https://github.com/AzureAD/microsoft-authentication-library-for-python

Both `PublicClientApplication` and `ConfidentialClientApplication` classes work effectively with this package and the Dataverse Web API.


## Refresh token callback
The refresh_token_callback parameter is an optional function that you can provide to handle token expiration. When the access token expires, the callback function will be called automatically to refresh the token. The callback function should return a new access token. To use the refresh_token_callback, pass it when creating an instance of DataverseORM:

``` python

def refresh_access_token():
    # Your token refresh logic here
    return new_access_token

orm = DataverseORM(dynamics_url="https://your_environment.crm.dynamics.com", access_token="your_access_token", refresh_token_callback=refresh_access_token)

```

By providing a refresh_token_callback, you can ensure seamless operation of the DataverseORM instance, even when the access token expires during its usage.

## Working with entities
To work with a specific entity, get an instance of the Entity class:

``` python
account = orm.entity("accounts")
```
### Query entities
To query entities, use the query method with optional OData filter expressions, select fields, and order by:

``` python
accounts = account.query(filter_expression="name eq 'Contoso'", select_fields=["name", "email"], order_by="name")
```
### Create a new entity
To create a new entity, use the create method with a dictionary of property names and values:

``` python
new_account = {"name": "Contoso", "email": "info@contoso.com"}
created_account = account.create(new_account)
```
### Update an existing entity
To update an existing entity, use the update method with the entity ID and a dictionary of property names and values to update:

``` python
updated_account = {"name": "Contoso Ltd.", "email": "info@contoso.com"}
account.update(entity_id="account_id", entity_data=updated_account)
```

### Delete an entity
To delete an entity, use the delete method with the entity ID:

``` python
account.delete(entity_id="account_id")
````
### Get an entity by ID
To get an entity by ID, use the get method with the entity ID:
``` python
retrieved_account = account.get(entity_id="account_id")
```
### Error handling
The module provides a custom DataverseError exception class for handling errors that may occur during API requests or metadata validation. To handle errors, wrap your code in a try-except block and catch the DataverseError exception:

``` python
from dataverse_orm import DataverseError

try:
    # Your code here
except DataverseError as e:
    print(f"An error occurred: {e}")
```
The DataverseError exception provides additional information such as the status code and the response object from the API request.

## License
This project is licensed under the MIT License.


## Contributions
We welcome contributions to the ms-dataverse project! If you'd like to contribute, follow these steps:

1. **Fork the repository:** Click the "Fork" button at the top-right corner of the repository page on GitHub to create a copy of the repository under your own account.

2. **Clone the forked repository:** Clone your forked repository to your local machine:
``` bash
git clone https://github.com/yourusername/ms-dataverse.git
```
Replace yourusername with your GitHub username.

3. **Create a new branch:** Create a new branch for your changes:

```bash
git checkout -b your-new-branch-name
```
Replace your-new-branch-name with a descriptive name for your branch.

4. **Make your changes:** Modify the code, fix bugs, or add new features to your branch.

5. **Commit your changes:** After making your changes, commit them to your branch:

```bash
git add .
git commit -m "Your commit message"
```
Replace Your commit message with a short description of the changes you made.

6. **Push your changes:** Push your changes to your forked repository on GitHub:

```bash
git push origin your-new-branch-name
```
7. **Create a pull request:** Go to the original ms-dataverse repository on GitHub and click the "New pull request" button. Choose your forked repository and the branch you created as the source, and the main ms-dataverse repository as the destination. Provide a brief description of your changes and submit the pull request.

Once you've submitted your pull request, we'll review your changes and, if everything looks good, merge them into the main repository. Thank you for your contributions!
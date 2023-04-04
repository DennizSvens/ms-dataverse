# DataverseORM
DataverseORM is a Python module that simplifies working with Microsoft Dataverse by providing a lightweight Object-Relational Mapper (ORM) for querying, creating, updating, and deleting entities. It uses the Dataverse Web API for communication and includes optional metadata validation to ensure that entities and properties exist in the connected Dataverse environment.

## Installation
```
pip install ms-dataverse
```

## Dependencies
- Python 3.6+
- requests library (install via pip: pip install requests)

## Usage
To use DataverseORM, import the DataverseORM class from the dataverse_orm.py file:

``` python
from ms_dataverse import DataverseORM
```

Create an instance of the DataverseORM class, passing in the URL to your Dataverse environment and an access token for authentication:

``` python
orm = DataverseORM(dynamics_url="https://your_environment.crm.dynamics.com", access_token="your_access_token")
```
## Fetching metadata
If you want to enable metadata validation (recommended during development), pass metadata_validation=True when creating an instance of DataverseORM:

``` python
orm = DataverseORM(dynamics_url="https://your_environment.crm.dynamics.com", access_token="your_access_token", metadata_validation=True)
```

Metadata validation verifies the existence of entities and properties prior to issuing API requests, which results in improved error handling and messaging.

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

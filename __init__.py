import requests
import xml.etree.ElementTree as ET

class DataverseError(Exception):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class DataverseORM:
    def __init__(self, dynamics_url, access_token, metadata_validation=False):
        self.dynamics_url = dynamics_url
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "OData-MaxVersion": "4.0",
            "Prefer": "return=representation"
        }
        self.base_url = f"{dynamics_url}/api/data/v9.2/"
        self.metadata_validation = metadata_validation
        self._entity_cache = {}
        if metadata_validation:
            self.fetch_metadata()

    def fetch_metadata(self):
        metadata_url = f"{self.base_url}$metadata"
        headers = self.headers.copy()
        headers["Accept"] = "application/xml"
        try:
            response = requests.get(metadata_url, headers=headers)
            response.raise_for_status()
            metadata_xml = response.text
            self.metadata = ET.fromstring(metadata_xml)
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error fetching metadata: {e}", response=e.response)

    def entity(self, entity_name):
        if entity_name not in self._entity_cache:
            self._entity_cache[entity_name] = Entity(self, entity_name)
        return self._entity_cache[entity_name]

class Entity:
    def __init__(self, orm, entity_name):
        self.orm = orm
        self.entity_name = entity_name
        if orm.metadata_validation:
            self.entity_set, self.entity_type_element = self._validate_entity()

    def _validate_entity(self):
      entity_set = self.orm.metadata.find(f".//EntitySet[@Name='{self.entity_name}']")
      if entity_set is None:
          raise DataverseError(f"Entity '{self.entity_name}' not found in the metadata.")
      entity_type = entity_set.get("EntityType").split(".")[-1]
      entity_type_element = self.orm.metadata.find(f".//EntityType[@Name='{entity_type}']")
      return entity_set, entity_type_element

    def _validate_properties(self, entity_data):
        for property_name in entity_data.keys():
            property_element = self.entity_type_element.find(f".//Property[@Name='{property_name}']")
            if property_element is None:
                raise DataverseError(f"Property '{property_name}' not found in entity '{self.entity_name}' in the metadata.")

    def get(self, entity_id):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.get(url, headers=self.orm.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error getting entity: {e}", response=e.response)

    def create(self, entity_data):
        self._validate_properties(entity_data)
        url = f"{self.orm.base_url}{self.entity_name}"
        try:
            response = requests.post(url, headers=self.orm.headers, json=entity_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error creating entity: {e}", response=e.response)

    def update(self, entity_id, entity_data):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.patch(url, headers=self.orm.headers, json=entity_data)
            response.raise_for_status()
            return response.status_code == 204
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error updating entity: {e}", response=e.response)

    def delete(self, entity_id):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.delete(url, headers=self.orm.headers)
            response.raise_for_status()
            return response.status_code == 204
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error deleting entity: {e}", response=e.response)

    def query(self, filter_expression=None, select_fields=None, order_by=None):
        url = f"{self.orm.base_url}{self.entity_name}"
        params = {}

        if filter_expression:
            params["$filter"] = filter_expression
        if select_fields:
            params["$select"] = ",".join(select_fields)
        if order_by:
            params["$orderby"] = order_by

        try:
            response = requests.get(url, headers=self.orm.headers, params=params)
            response.raise_for_status()
            return response.json()["value"]
        except requests.exceptions.RequestException as e:
            raise DataverseError(f"Error querying entity: {e}", response=e.response)
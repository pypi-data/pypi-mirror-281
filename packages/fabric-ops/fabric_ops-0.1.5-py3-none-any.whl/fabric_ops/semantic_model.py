# Author: Jonathan Cuéllar Viveros
# Company: Dalatic S.L
# Contact: info@dalatic.com
# Copyright (C) 2024 Jonathan Cuéllar Viveros. All rights reserved.
# Derechos de autor (C) 2024 Jonathan Cuéllar Viveros. Todos los derechos reservados.

from .auth import AuthOperation
from .base import BaseOperation

class SemanticModelOperation(BaseOperation):
    """
    A client for interacting with PowerBI API.
    """
    def __init__(self, auth_operation=None):
        if auth_operation is None:
            auth_operation = AuthOperation(api_scope='pbi', auth_type='service_principal')
        super().__init__(auth_operation)

    def get_sm(self, workspaceId, datasetId):
        """
        Retrieve a dataset ID based on its name within a workspace.

        :param workspaceId: ID of the workspace.
        :param ds_name: Dataset name.
        :return: Dataset ID.
        """

        response = f"admin/groups/groups/{workspaceId}/datasets/{datasetId}"
        return response

    def get_all(self, workspaceId):
        """
        Retrieve all datasets within a workspace.

        :param workspaceId: ID of the workspace.
        :return: List of datasets.
        """
        url = f"/admin/groups/{workspaceId}/datasets"

    
        return self.get(url)["value"]

    def dax_query(self, workspaceId, datasetId, query):
        """
        Execute a DAX query on a dataset within a workspace.

        :param workspaceId: ID of the workspace.
        :param datasetId: ID of the dataset.
        :param query: DAX query to be executed.
        :return: Query result.
        """
        url = f"/groups/{workspaceId}/datasets/{datasetId}/executeQueries"
        body = {
            "queries": [
                {
                    "query": "EVALUATE INFO.MEASURES()"
                }
            ],
            "serializerSettings": {
                "includeNulls": "true"
            },
            "impersonatedUserName": "someuser@mycompany.com"
        }
        return self.post(url, body)

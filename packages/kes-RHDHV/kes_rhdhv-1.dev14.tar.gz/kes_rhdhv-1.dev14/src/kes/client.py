"""Client module.

This module is the starting point for wrting a Kes Python script.
Scripts typically start by configuring and creating a client, after which this client can be used to open projects.

Usage example::

    config = Config(kes_service_address='localhost:50051')
    client = Client(config)
    project = client.open_project("Preview Python client example")
"""
import os
from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

import grpc

from kes.project import Project, Activity
from kes.proto.project_pb2 import LookupProjectRequest
from kes.proto.project_pb2_grpc import ProjectDetailStub
from kes.proto.table_pb2_grpc import TableStub


class ProjectNotFound(Exception):
    """ Exception indicating when a project could not be found."""
    ...


@dataclass
class Config:
    """Holds configuration of the client.

    Attributes:
        kes_service_address:
            Address of the service which interacts with the Kes database.
            Defaults to the production instance.
            Example: :code:`kes-table-service-production.delightfuldesert-b9ce0345.westeurope.azurecontainerapps.io:443`
        access_token:
            Access token. Can be obtained from the Kes project manager.
        root_certificates_path:
            Path to the file containing the root certificates.
            Defaults to :code:`None`. Can be left blank unless connecting to a custom KES instance.
    """
    access_token: str = os.getenv('ACCESS_TOKEN', 'token')
    kes_service_address: str = os.getenv('URL',
                                         'kes-table-service-production.delightfuldesert-b9ce0345.westeurope.azurecontainerapps.io:443')
    root_certificates_path: Optional[str] = None
    test_user_id: Optional[str] = os.getenv('TEST_USER_ID', None)


class Client:
    """Kes client.

    Starting point of a kes script. After creating a client instance, kes projects can be opened using open_project.
    """

    _channel: grpc.Channel
    _table_stub: TableStub
    _project_stub: ProjectDetailStub

    def __init__(self, config: Config):
        """Constructs a client.

        Args:
            config (Config): The client configuration
        """
        root_certificates = None
        if config.root_certificates_path != None:
            with open(config.root_certificates_path, 'rb') as f:
                root_certificates = f.read()
        channel_credentials = grpc.ssl_channel_credentials(root_certificates)
        call_credentials = grpc.access_token_call_credentials(config.access_token)
        if config.test_user_id is not None:
            test_user_cred = lambda context, callback: callback([('test-user-id', config.test_user_id)], None)
            metadata_credentials = grpc.metadata_call_credentials(test_user_cred, name='Test User Cred')
            combined_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials,
                                                                      metadata_credentials)
        else:
            combined_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        self._channel = grpc.secure_channel(config.kes_service_address, combined_credentials)
        self._table_stub = TableStub(self._channel)
        self._project_stub = ProjectDetailStub(self._channel)

    def load_project_by_master_id(self, master_id: str) -> List[Project]:
        """Load Kes project's by master project id.

        Args:
            master_id (str): Master Project Id of the projects to load.

        Returns:
            One or multiple Kes projects.

        Raises:
            ProjectNotFound: The requested project could not be found.
        """
        try:
            request = LookupProjectRequest(masterProjectId=master_id)
            reply = self._project_stub.lookupProject(request)
            projects: List[Project] = []
            for pb_project in reply.projects:
                project = Project(UUID(pb_project.id), pb_project.name, pb_project.projectNumber,
                                  pb_project.masterProjectId, self._table_stub, self._project_stub)
                projects.append(project)
            return projects
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ProjectNotFound
            else:
                raise

    def open_project_by_id(self, project_id: UUID) -> Project:
        """Open a Kes project by id

        Args:
            project_id (UUID): uuid of the project to open.

        Returns:
            An instance representing the requested Kes project.
        """
        return Project(project_id, "", "", "", self._table_stub, self._project_stub)

    def open_activity_by_id(self, activity_id: UUID = os.getenv('ACTIVITY_ID', '')) -> Activity:
        """Open a Kes project by id

        Args:
            activity_id (UUID): uuid of the activity to open.

        Returns:
            An instance representing the requested Kes Activity.
        """
        return Activity(self._table_stub, activity_id, "", self._project_stub)

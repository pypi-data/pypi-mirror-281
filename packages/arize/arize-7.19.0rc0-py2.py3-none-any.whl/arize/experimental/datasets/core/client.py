from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
from google.protobuf import json_format, message
from pyarrow import flight

from .. import requests_pb2 as request_pb
from ..utils.constants import (
    ARIZE_PROFILE,
    DEFAULT_ARIZE_FLIGHT_HOST,
    DEFAULT_ARIZE_FLIGHT_PORT,
    DEFAULT_CONFIG_PATH,
    DEFAULT_PROFILE_NAME,
    DEFAULT_TRANSPORT_SCHEME,
)
from .session import Session
from .validations import validate_df_and_convert_to_arrow


@dataclass
class ArizeDatasetsClient:
    api_key: Optional[str] = None
    arize_profile: str = ARIZE_PROFILE or DEFAULT_PROFILE_NAME
    arize_config_path: Optional[str] = DEFAULT_CONFIG_PATH
    host: str = DEFAULT_ARIZE_FLIGHT_HOST
    port: int = DEFAULT_ARIZE_FLIGHT_PORT
    scheme: str = DEFAULT_TRANSPORT_SCHEME

    def __post_init__(self) -> None:
        f"""
        Initializes the Arize Dataset Client.

        Arguments:
        ----------
            api_key (str, optional): Arize provided personal API key associated with your user profile,
                located on the API Explorer page. API key is required to initiate a new client, it can
                be passed in explicitly, or set up as an environment variable or in profile file.
            arize_profile (str, optional): profile name for ArizeExportClient credentials and endpoint.
                Defaults to '{DEFAULT_PROFILE_NAME}'.
            arize_config_path (str, optional): path to the config file that stores ArizeExportClient
                credentials and endpoint. Defaults to '~/.arize'.
            host (str, optional): URI endpoint host to send your export request to Arize AI. Defaults to
                "{DEFAULT_ARIZE_FLIGHT_HOST}".
            port (int, optional): URI endpoint port to send your export request to Arize AI. Defaults to
                {DEFAULT_ARIZE_FLIGHT_PORT}.
        """
        self.__session = Session(
            self.api_key,
            self.arize_profile,
            self.arize_config_path,
            self.host,
            self.port,
            self.scheme,
        )

    @property
    def session(self) -> Session:
        return self.__session

    def create_dataset(
        self,
        space_id: str,
        dataset_name: str,
        dataset_type: request_pb.DatasetType,
        data: pd.DataFrame,
    ) -> bool:

        req = request_pb.DoPutRequest(
            create_dataset=request_pb.CreateDatasetRequest(
                space_id=space_id,
                dataset_name=dataset_name,
                dataset_type=dataset_type,
            )
        )

        dsc = self._desc_for_request(req)
        flight_client = self.session.connect()
        tbl = validate_df_and_convert_to_arrow(data)
        try:
            writer, metadata_reader = flight_client.do_put(
                dsc, tbl.schema, self.session.call_options
            )
            with writer:
                writer.write_table(tbl, max_chunksize=10_000)
                writer.done_writing()
                response = metadata_reader.read()
                if response is not None:
                    res = request_pb.CreateDatasetResponse()
                    res.ParseFromString(response.to_pybytes())
                    return res.dataset_id
        except Exception as e:
            raise RuntimeError("Failed to create dataset") from e

    def update_dataset(self, space_id: str, dataset_id: str, data: pd.DataFrame) -> bool:
        req = request_pb.DoPutRequest(
            update_dataset=request_pb.UpdateDatasetRequest(
                space_id=space_id,
                dataset_id=dataset_id,
            )
        )
        dsc = self._desc_for_request(req)
        flight_client = self.session.connect()
        tbl = validate_df_and_convert_to_arrow(data)
        try:
            writer, metadata_reader = flight_client.do_put(
                dsc, tbl.schema, self.session.call_options
            )
            with writer:
                writer.write_table(tbl)
                writer.done_writing()
                response = metadata_reader.read()
                if response is not None:
                    res = request_pb.UpdateDatasetResponse()
                    res.ParseFromString(response.to_pybytes())
                    return res.dataset_id
        except Exception as e:
            raise RuntimeError("Failed to update dataset") from e

    def get_dataset(
        self, space_id: str, dataset_id: str, dataset_version: str = None
    ) -> pd.DataFrame:
        if dataset_version is None:
            dataset_version = ""
        req = request_pb.DoGetRequest(
            get_dataset=request_pb.GetDatasetRequest(
                space_id=space_id, dataset_id=dataset_id, dataset_version=dataset_version
            )
        )

        flight_client = self.session.connect()
        ticket = self._ticket_for_request(req)
        try:
            reader = flight_client.do_get(ticket, self.session.call_options)
            table = reader.read_all()
            df = table.to_pandas()
            return df
        except Exception as e:
            raise RuntimeError("Failed to get dataset") from e

    def get_dataset_versions(self, space_id: str, dataset_id: str) -> List[Dict[str, Any]]:
        req = request_pb.DoActionRequest(
            get_dataset_versions=request_pb.GetDatasetVersionsRequest(
                space_id=space_id, dataset_id=dataset_id
            )
        )
        act = self._action_for_request("get_dataset_versions", req)
        try:
            flight_client = self.session.connect()
            res = flight_client.do_action(act, self.session.call_options)
            flight_client.close()
            if not res:
                return []
            res = list(res)
            resp_pb = request_pb.GetDatasetVersionsResponse()
            resp_pb.ParseFromString(res[0].body.to_pybytes())
            out = []
            for v in resp_pb.versions:
                out.append(
                    {
                        "dataset_version": v.version_name,
                        "created_at": v.created_at.ToJsonString(),
                        "updated_at": v.updated_at.ToJsonString(),
                    }
                )
            return out
        except Exception as e:
            raise RuntimeError("Failed to get dataset versions") from e

    def list_datasets(self, space_id: str) -> List[Dict[str, Any]]:
        req = request_pb.DoActionRequest(
            list_datasets=request_pb.ListDatasetsRequest(space_id=space_id)
        )
        act = self._action_for_request("list_datasets", req)
        try:
            flight_client = self.session.connect()
            res = flight_client.do_action(act, self.session.call_options)
            flight_client.close()
            resp_pb = request_pb.ListDatasetsResponse()
            res = list(res)
            resp_pb.ParseFromString(res[0].body.to_pybytes())

            out = []
            for dataset in resp_pb.datasets:
                out.append(
                    {
                        "dataset_id": dataset.dataset_id,
                        "dataset_name": dataset.dataset_name,
                        "dataset_type": request_pb.DatasetType.Name(dataset.dataset_type),
                        "created_at": dataset.created_at.ToJsonString(),
                        "updated_at": dataset.updated_at.ToJsonString(),
                    }
                )
            return out
        except Exception as e:
            raise RuntimeError("Failed to get all datasets") from e

    def delete_dataset(self, space_id: str, dataset_id: str) -> bool:
        req = request_pb.DoActionRequest(
            delete_dataset=request_pb.DeleteDatasetRequest(space_id=space_id, dataset_id=dataset_id)
        )
        act = self._action_for_request("delete_dataset", req)
        try:
            flight_client = self.session.connect()
            res = flight_client.do_action(act, self.session.call_options)
            flight_client.close()
            resp_pb = request_pb.DeleteDatasetResponse()
            res = list(res)
            resp_pb.ParseFromString(res[0].body.to_pybytes())
            return resp_pb.success
        except Exception as e:
            raise RuntimeError("Failed to delete dataset") from e

    def _desc_for_request(self, request: message) -> flight.FlightDescriptor:
        data = json_format.MessageToJson(request).encode("utf-8")
        descriptor = flight.FlightDescriptor.for_command(data)
        return descriptor

    def _ticket_for_request(self, request: message) -> flight.Ticket:
        data = json_format.MessageToJson(request).encode("utf-8")
        return flight.Ticket(data)

    def _action_for_request(self, action_key: str, request: message) -> flight.Action:
        req_bytes = json_format.MessageToJson(request).encode("utf-8")
        return flight.Action(action_key, req_bytes)

import os

from camalis.core import BaseCamalisClient
from camalis.event import Event
from camalis.exceptions import CamalisAuthException, CamalisApiException
from camalis.state import State
from camalis.variable import Variable

import io
import zipfile
import pandas as pd

class CamalisVariableClient:
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client

    def get(self, name=None, path=None) -> Variable:
        """
        Get variable by name or path
        :param name: name of the variable
        :param path: path of the variable
        :return: Variable object
        :raises CamalisApiException: if variable not found
        :raises CamalisApiException: if multiple variables found
        :raises CamalisApiException: if name or path is not provided
        """
        if path is None and name is None:
            raise CamalisApiException('Name or path is required')

        if path and name:
            raise CamalisApiException('Only one parameter is allowed')

        response = None

        url = '/variaveis/'
        if name:
            if self._camalis.element_id is None:
                raise CamalisApiException('ElementId is required')

            url = f'{url}buscarPorNome/?nome={name}&elementoId={self._camalis.element_id}'
            response = self._camalis.request_get(url=url)

        if path:
            url = f'{url}buscarPorPath/?path={path}'
            response = self._camalis.request_get(url=url)

        if len(response['ids']) == 0:
            raise CamalisApiException('Variable not found')

        if len(response['ids']) > 1:
            raise CamalisApiException('Multiple variables found, if you want to list use list method')

        return Variable(self._camalis, id=response['ids'][0])

    def list(self, path=None) -> list[Variable]:
        """
        List variables by path
        :param path: path of the variables
        :return: list of Variable objects
        """
        if path is None and self._camalis.element_id is None:
            raise CamalisApiException('Path or element_id is required')

        url = f'/variaveis/buscarPorPath/?path={path}' \
            if path else f'/variaveis/buscarPorNome/?nome=&elementoId={self._camalis.element_id}'
        response = self._camalis.request_get(url=url)
        if len(response['ids']) == 0:
            return []

        result = []
        for variable_id in response['ids']:
            result.append(Variable(self._camalis, id=variable_id))
        return result


class CamalisDatasetClient:
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client

    def download(self, dataset_id):
        """
        Get dataset by id
        :param dataset_id:
        :return: list of datasets
        """
        if dataset_id is None:
            raise CamalisApiException('Dataset ID is required')

        url = 'rotulagem/datasets_versoes'
        response = self._camalis.request_get(
            f'/{url}/download/dataset/{dataset_id}', content_type='application/zip')

        zip_content = response
        datasets = []

        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            for csv_filename in z.namelist():
                if csv_filename.endswith('.csv'):
                    with z.open(csv_filename) as f:
                        df = pd.read_csv(f)
                        datasets.append(df)

        return datasets


class CamalisModelClient:
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client

    def download(self, modelo_id):
        """
        Get model by id
        :param modelo_id: ID of the model to download
        :return: loaded model
        """

        if modelo_id is None:
            raise CamalisApiException('Model ID is required')

        url = 'rotulagem/modelo_especialista'
        response = self._camalis.request_get(f'/{url}/download/{modelo_id}')

        return response

class Camalis(BaseCamalisClient):
    """
    Camalis client
    """
    variable: CamalisVariableClient = None

    def __init__(self, api_url=None, token=None, element_id=None):
        """
        Initialize Camalis client
        :param api_url: URL of the Camalis API
        :param token: Token for the Camalis API
        :param element_id: Element ID for the Camalis API
        """
        request_token = os.environ.get('CAMALIS_TOKEN', token)
        camalis_url = os.environ.get('CAMALIS_API_URL', api_url)
        camalis_element_id = os.environ.get('CAMALIS_ELEMENTO_ID', element_id)

        if request_token is None:
            raise CamalisAuthException('Token is required')

        if camalis_url is None:
            raise CamalisAuthException('API URL is required')

        super().__init__(camalis_url, request_token, camalis_element_id)
        self.variable = CamalisVariableClient(self)
        self.dataset = CamalisDatasetClient(self)
        self.model = CamalisModelClient(self)

    def state(self) -> State:
        return State(self)

    def event(self) -> Event:
        return Event(self)

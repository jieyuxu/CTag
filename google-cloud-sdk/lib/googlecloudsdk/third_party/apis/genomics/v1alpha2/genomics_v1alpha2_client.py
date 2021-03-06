"""Generated client library for genomics version v1alpha2."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.genomics.v1alpha2 import genomics_v1alpha2_messages as messages


class GenomicsV1alpha2(base_api.BaseApiClient):
  """Generated client library for service genomics version v1alpha2."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://genomics.googleapis.com/'
  MTLS_BASE_URL = u''

  _PACKAGE = u'genomics'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform', u'https://www.googleapis.com/auth/compute', u'https://www.googleapis.com/auth/genomics']
  _VERSION = u'v1alpha2'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'GenomicsV1alpha2'
  _URL_VERSION = u'v1alpha2'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new genomics handle."""
    url = url or self.BASE_URL
    super(GenomicsV1alpha2, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.operations = self.OperationsService(self)
    self.pipelines = self.PipelinesService(self)

  class OperationsService(base_api.BaseApiService):
    """Service class for the operations resource."""

    _NAME = u'operations'

    def __init__(self, client):
      super(GenomicsV1alpha2.OperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation.
The server makes a best effort to cancel the operation, but success is not
guaranteed. Clients may use Operations.GetOperation
or Operations.ListOperations
to check whether the cancellation succeeded or the operation completed
despite cancellation.
Authorization requires the following [Google IAM](https://cloud.google.com/iam) permission&#58;

* `genomics.operations.cancel`

      Args:
        request: (GenomicsOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha2/operations/{operationsId}:cancel',
        http_method=u'POST',
        method_id=u'genomics.operations.cancel',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1alpha2/{+name}:cancel',
        request_field=u'cancelOperationRequest',
        request_type_name=u'GenomicsOperationsCancelRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation.
Clients can use this method to poll the operation result at intervals as
recommended by the API service.
Authorization requires the following [Google IAM](https://cloud.google.com/iam) permission&#58;

* `genomics.operations.get`

      Args:
        request: (GenomicsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha2/operations/{operationsId}',
        http_method=u'GET',
        method_id=u'genomics.operations.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1alpha2/{+name}',
        request_field='',
        request_type_name=u'GenomicsOperationsGetRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request.
Authorization requires the following [Google IAM](https://cloud.google.com/iam) permission&#58;

* `genomics.operations.list`

      Args:
        request: (GenomicsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha2/operations',
        http_method=u'GET',
        method_id=u'genomics.operations.list',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'filter', u'pageSize', u'pageToken'],
        relative_path=u'v1alpha2/{+name}',
        request_field='',
        request_type_name=u'GenomicsOperationsListRequest',
        response_type_name=u'ListOperationsResponse',
        supports_download=False,
    )

  class PipelinesService(base_api.BaseApiService):
    """Service class for the pipelines resource."""

    _NAME = u'pipelines'

    def __init__(self, client):
      super(GenomicsV1alpha2.PipelinesService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a pipeline that can be run later. Create takes a Pipeline that.
has all fields other than `pipelineId` populated, and then returns
the same pipeline with `pipelineId` populated. This id can be used
to run the pipeline.

Caller must have WRITE permission to the project.

      Args:
        request: (Pipeline) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Pipeline) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'genomics.pipelines.create',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha2/pipelines',
        request_field='<request>',
        request_type_name=u'Pipeline',
        response_type_name=u'Pipeline',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a pipeline based on ID.

Caller must have WRITE permission to the project.

      Args:
        request: (GenomicsPipelinesDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'DELETE',
        method_id=u'genomics.pipelines.delete',
        ordered_params=[u'pipelineId'],
        path_params=[u'pipelineId'],
        query_params=[],
        relative_path=u'v1alpha2/pipelines/{pipelineId}',
        request_field='',
        request_type_name=u'GenomicsPipelinesDeleteRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Retrieves a pipeline based on ID.

Caller must have READ permission to the project.

      Args:
        request: (GenomicsPipelinesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Pipeline) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'genomics.pipelines.get',
        ordered_params=[u'pipelineId'],
        path_params=[u'pipelineId'],
        query_params=[],
        relative_path=u'v1alpha2/pipelines/{pipelineId}',
        request_field='',
        request_type_name=u'GenomicsPipelinesGetRequest',
        response_type_name=u'Pipeline',
        supports_download=False,
    )

    def GetControllerConfig(self, request, global_params=None):
      r"""Gets controller configuration information. Should only be called.
by VMs created by the Pipelines Service and not by end users.

      Args:
        request: (GenomicsPipelinesGetControllerConfigRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ControllerConfig) The response message.
      """
      config = self.GetMethodConfig('GetControllerConfig')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetControllerConfig.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'genomics.pipelines.getControllerConfig',
        ordered_params=[],
        path_params=[],
        query_params=[u'operationId', u'validationToken'],
        relative_path=u'v1alpha2/pipelines:getControllerConfig',
        request_field='',
        request_type_name=u'GenomicsPipelinesGetControllerConfigRequest',
        response_type_name=u'ControllerConfig',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists pipelines.

Caller must have READ permission to the project.

      Args:
        request: (GenomicsPipelinesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPipelinesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'genomics.pipelines.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'namePrefix', u'pageSize', u'pageToken', u'projectId'],
        relative_path=u'v1alpha2/pipelines',
        request_field='',
        request_type_name=u'GenomicsPipelinesListRequest',
        response_type_name=u'ListPipelinesResponse',
        supports_download=False,
    )

    def Run(self, request, global_params=None):
      r"""Runs a pipeline. If `pipelineId` is specified in the request, then.
run a saved pipeline. If `ephemeralPipeline` is specified, then run
that pipeline once without saving a copy.

The caller must have READ permission to the project where the pipeline
is stored and WRITE permission to the project where the pipeline will be
run, as VMs will be created and storage will be used.

If a pipeline operation is still running after 6 days, it will be canceled.

      Args:
        request: (RunPipelineRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Run')
      return self._RunMethod(
          config, request, global_params=global_params)

    Run.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'genomics.pipelines.run',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha2/pipelines:run',
        request_field='<request>',
        request_type_name=u'RunPipelineRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def SetOperationStatus(self, request, global_params=None):
      r"""Sets status of a given operation. Any new timestamps (as determined by.
description) are appended to TimestampEvents. Should only be called by VMs
created by the Pipelines Service and not by end users.

      Args:
        request: (SetOperationStatusRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('SetOperationStatus')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetOperationStatus.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'PUT',
        method_id=u'genomics.pipelines.setOperationStatus',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha2/pipelines:setOperationStatus',
        request_field='<request>',
        request_type_name=u'SetOperationStatusRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

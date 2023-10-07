from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import ErrorDetail


class ApiRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response_dict = {
            'success': True,
            'status': '',
            'message': '',
            'status_code': status_code,
            'data': None,
            'errors': None,
        }

        if type(data) == dict:
            if 'detail' in data:
                response_dict['message'] = data.get('detail')
            elif 'message' in data:
                response_dict['message'] = data.get('message')
        elif type(data) == ReturnDict and not str(status_code).startswith('2'):
            response_dict['errors'] = []
            if (type(data[list(data.keys())[0]]) == dict):
                response_dict['message'] = "Please make sure all parameteres are valid!"
                response_dict['errors'] = data[list(data.keys())[0]]
            else:
                response_dict['message'] = '{0}: {1}'.format(
                    list(data.keys())[0], data[list(data.keys())[0]][0])
                for field in data:
                    response_dict['errors'].append(
                        {'field_name': field, 'message': data[field][0]})
        elif type(data) == list and len(data) > 0 and type(data[0]) == ErrorDetail:
            response_dict["message"] = str(data[0])
        elif type(data) == list:
            # response_dict['message'] = data[0]
            response_dict['errors'] = []

        response_dict['success'] = False
        response_dict["status"] = "failure"

        if str(status_code).startswith('2'):
            response_dict['success'] = True
            response_dict["status"] = "success"
            response_dict["data"] = data
            # remove data if data only contains the details or message
            if type(data) == dict and len(data) == 1 and ('detail' in data or 'message' in data):
                response_dict["data"] = None

        return super(ApiRenderer, self).render(response_dict, accepted_media_type, renderer_context)

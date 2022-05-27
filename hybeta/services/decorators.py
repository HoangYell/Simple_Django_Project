from functools import wraps

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def response(f):
    """
    Decorator return http response base on stage
    :param f: function

    Example:
        :argument:
            f = DoctorViewSet.list,
        :return:
            Response(DoctorViewSet.list(request), status=200)
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            data = f(*args, **kwargs)
            return Response(data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(dict(message=str(e)), status=status.HTTP_400_BAD_REQUEST)
        except:
            # TODO save this Exception to log, returns header response log_id
            return Response(dict(message="There is an issue processing your request."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper

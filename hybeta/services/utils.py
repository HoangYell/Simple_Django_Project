import re

from hybeta.models import AutoTimeStampedModel, SoftDeleteModel


class Utils:
    @staticmethod
    def get_model_fields(model):
        """
        Get all model fields without meta fields
        :param model: model

        Example:
            :argument:
                model = <class 'jobs.models.doctor.Doctor'>,
            :return:
                ['is_deleted', 'deleted_at', 'created_at', 'updated_at', 'id', 'phone', 'location_id', 'category', 'price', 'available_time']
        """
        model_fields = []
        for field in model._meta.get_fields():
            field_name = getattr(field, "column", "")
            if field_name:
                model_fields.append(field_name)
        return model_fields

    @classmethod
    def get_soft_delete_fields(cls):
        return cls.get_model_fields(SoftDeleteModel)

    @classmethod
    def get_util_fields(cls):
        return [*cls.get_model_fields(SoftDeleteModel), *cls.get_model_fields(AutoTimeStampedModel)]

    @classmethod
    def params_2_queryset(cls, model, data, mandatory_filter=None, sort_prefix="sort", filter_prefix="filter"):
        """
        Convert params into queryset
        :param model: model
        :param data: the query params
        :param mandatory_filter: the highest priority filter, helps to limit the query scope from UI for security
        :param sort_prefix: query params format for sort
        :param filter_prefix: query params format for filter_prefix

        Example:
            :argument:
                model = <class 'jobs.models.doctor.Doctor'>,
                data = {'filter_1__location_id': '1', 'sort_1__price': 'desc', 'sort_2__id': 'asc'},
                mandatory_filter = {'pk': '1'}
            :return:
                Doctor.objects.filter(location_id='1', pk='1'}).sort('-price', 'id')
        """
        sort_data = {}
        filter_data = {}
        model_fields = cls.get_model_fields(model)
        for key, value in data.items():
            # https://regex101.com/r/bt8AVU/1
            query_key = re.search(rf"^({sort_prefix}|{filter_prefix})_(\d)__([a-zA-Z-_]+)$", key)
            if query_key:
                query_type = query_key.group(1)
                priority = query_key.group(2)
                field = query_key.group(3)
                if field in model_fields:
                    if sort_prefix == query_type:
                        sort_data[priority] = ("", "-")[value == "desc"] + field
                    elif filter_prefix == query_type:
                        filter_data[field] = value
        sorts = [sort_data[k] for k in sorted(sort_data)]
        if mandatory_filter:
            filter_data.update(mandatory_filter)
        queryset = model.objects.filter(**filter_data)
        if sorts:
            queryset = queryset.order_by(*sorts)
        return queryset

# encoding: utf-8
"""
@project: djangoModel->thread_category_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 类别api
@created_time: 2022/10/25 14:40
"""
from rest_framework.views import APIView

from ..services.thread_category_service import ThreadCategoryService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, force_transform_type


class ThreadCategoryApis(APIView):
    @request_params_wrapper
    def add(self, *args, request_params=None, **kwargs):
        data, err = ThreadCategoryService.add(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = kwargs.get("pk") or request_params.get("id") or request_params.get("category_id")
        data, err = ThreadCategoryService.delete(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def edit(self, *args, request_params=None, **kwargs):
        pk = kwargs.get("pk") or request_params.get("id") or request_params.get("category_id")
        data, err = ThreadCategoryService.edit(request_params, pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def list(self, *args, request_params=None, **kwargs):
        need_child = request_params.pop("need_child", False)
        need_pagination = request_params.pop("need_pagination", True)
        request_params.setdefault("category_value", kwargs.get("category_value", None))

        data, err = ThreadCategoryService.list(
            params=request_params,
            need_pagination=need_pagination,
            filter_fields=request_params.pop("filter_fields", None),
            need_child=need_child
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

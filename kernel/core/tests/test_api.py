import pytest
from rest_framework.exceptions import APIException, PermissionDenied
from django.http import Http404
from kernel.core.api.responses import success_response, error_response
from kernel.core.api.exceptions import core_exception_handler
from kernel.core.exceptions import BusinessError

def test_success_response():
    resp = success_response(data={"foo": "bar"}, message="Success")
    assert resp.status_code == 200
    assert resp.data['success'] is True
    assert resp.data['code'] == "OK"
    assert resp.data['message'] == "Success"
    assert resp.data['data'] == {"foo": "bar"}

def test_error_response():
    resp = error_response(message="Fail", code="ERR_01", status=400)
    assert resp.status_code == 400
    assert resp.data['success'] is False
    assert resp.data['code'] == "ERR_01"
    assert resp.data['message'] == "Fail"

def test_exception_handler_business_error():
    exc = BusinessError("Invalid logic", code="BIZ_ERR")
    resp = core_exception_handler(exc, {})
    assert resp.status_code == 400
    assert resp.data['success'] is False
    assert resp.data['code'] == "BIZ_ERR"
    assert resp.data['message'] == "Invalid logic"

def test_exception_handler_drf_exception():
    exc = PermissionDenied("No access")
    # core_exception_handler calls DRF handler which handles PermissionDenied
    # But wait, django PermissionDenied needs to be handled by DRF handler first?
    # DRF's exception_handler handles Django's PermissionDenied and Http404.
    
    resp = core_exception_handler(exc, {})
    assert resp.status_code == 403
    assert resp.data['success'] is False
    assert resp.data['code'] == "FORBIDDEN"

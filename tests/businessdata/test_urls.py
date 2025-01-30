import pytest
from django.urls import reverse, resolve
from businessdata.views import (
    addBusinessData,
    updateBusinessData,
    deleteBusinessData,
    businessDataManagement
)

@pytest.mark.parametrize("url_name, view_func, kwargs", [
    ("addbusinessdata", addBusinessData, {}),
    ("updatebusinessdata", updateBusinessData, {"pk": 1}),
    ("deletebusinessdata", deleteBusinessData, {"pk": 1}),
    ("businessdatamanagement", businessDataManagement, {})
])
def test_urls(url_name, view_func, kwargs):
    """Test if the URL resolves to the correct view."""
    url = reverse(f"businessdata:{url_name}", kwargs=kwargs if "pk" in kwargs else None)
    resolved = resolve(url)
    assert resolved.func == view_func

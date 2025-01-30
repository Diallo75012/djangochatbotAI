import pytest
from django import forms
from django.contrib.auth.models import User, Group
from common.templatetags.form_tags import add_class_with_label, has_group
from django.utils.html import format_html


# ✅ Test for `add_class_with_label`
def test_add_class_with_label():
    """Test `add_class_with_label` ensures correct HTML output with CSS classes."""
    
    class TestForm(forms.Form):
        username = forms.CharField(label="Username")
    
    form = TestForm()
    field = form["username"]
    css_class = "custom-input"

    # Expected output format
    expected_html = format_html(
        '<div class="form-group">{}</br>{}</div>',
        field.label_tag(attrs={"class": "form-label"}),
        field.as_widget(attrs={"class": css_class})
    )

    # Assertion
    assert add_class_with_label(field, css_class) == expected_html


# ✅ Test for `has_group`
@pytest.mark.django_db
def test_has_group():
    """Test `has_group` filter correctly checks if a user belongs to a group."""
    
    user = User.objects.create_user(username="testuser", password="securepassword")
    group = Group.objects.create(name="TestGroup")

    assert not has_group(user, "TestGroup")  # User initially not in group

    user.groups.add(group)  # Add user to group
    assert has_group(user, "TestGroup")  # Should return True now

    assert not has_group(user, "NonExistentGroup")  # Group doesn't exist

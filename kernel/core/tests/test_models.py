import pytest
from django.db import models
from kernel.core.models import BaseModel
from datetime import timedelta
from django.utils import timezone

# Define a concrete model for testing
class TestModel(BaseModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'core'

@pytest.mark.django_db
def test_base_model_creation():
    obj = TestModel.objects.create(name="Test")
    assert obj.id is not None
    assert len(str(obj.id)) == 36  # UUID length
    assert obj.created_at is not None
    assert obj.updated_at is not None
    assert obj.is_deleted is False

@pytest.mark.django_db
def test_base_model_update_timestamp():
    obj = TestModel.objects.create(name="Test")
    created_at = obj.created_at
    updated_at = obj.updated_at
    
    # Ensure some time passes (mocking might be better but this is simple)
    # Actually auto_now relies on save(), let's just save again
    import time
    time.sleep(0.001) 
    
    obj.name = "Updated"
    obj.save()
    
    assert obj.updated_at > updated_at
    assert obj.created_at == created_at

from django.db import transaction
from functools import wraps

def atomic(using=None, savepoint=True, durable=False):
    """
    Decorator that wraps a function in an atomic transaction.
    Just a wrapper around django.db.transaction.atomic for consistency.
    """
    return transaction.atomic(using=using, savepoint=savepoint, durable=durable)

def on_commit(func, using=None):
    """
    Register a function to be called after the transaction is committed.
    """
    transaction.on_commit(func, using=using)

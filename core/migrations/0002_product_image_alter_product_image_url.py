# This migration stub exists to resolve a conflict with the Render
# deployment database which has this migration recorded.
# The actual field changes were already present in 0001_initial.py.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # No-op: fields already existed in 0001_initial
    ]

from __future__ import unicode_literals

from django.db import migrations, models

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    List = apps.get_model("quranfal", "List")
    db_alias = schema_editor.connection.alias
    List.objects.using(db_alias).bulk_create([
        List(name="Known Words"),
        List(name="Words to Study"),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    List = apps.get_model("quranfal", "List")
    db_alias = schema_editor.connection.alias
    List.objects.using(db_alias).filter(name="Known Words").delete()
    List.objects.using(db_alias).filter(name="Words to Study").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('quranfal', '0007_auto_20160610_1503'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
import os
from pathlib import Path

from django.db import migrations, models


def record_existing_namespace(apps, schema_editor):
    # Apply before changing the job namespace; existing Job names omit it.
    namespace = os.environ.get("EDA_ACTIVATION_JOB_NAMESPACE", "").strip()
    if not namespace:
        namespace_file = Path(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
        )
        if namespace_file.exists():
            namespace = namespace_file.read_text(encoding="utf-8").strip()
    if namespace:
        apps.get_model("core", "RulebookProcess").objects.using(
            schema_editor.connection.alias
        ).filter(activation_pod_id__isnull=False).update(
            activation_job_namespace=namespace
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0076_rulebookprocess_log_retention_checkpoint"),
    ]

    operations = [
        migrations.AddField(
            model_name="rulebookprocess",
            name="activation_job_namespace",
            field=models.TextField(null=True),
        ),
        migrations.RunPython(
            record_existing_namespace, migrations.RunPython.noop
        ),
    ]

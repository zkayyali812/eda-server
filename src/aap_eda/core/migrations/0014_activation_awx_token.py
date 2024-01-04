# Generated by Django 4.2.7 on 2023-12-21 18:50

import django.db.models.deletion
from django.db import migrations, models


def populate_awx_token(apps, schema_editor):
    """Populate existing activations with AWX tokens.

    Ensure that the awx_token field is populated for all existing
    activations after the migration is applied. If the user has an
    AWX token, use it. Always use the first AWX token, previous
    versions of the code only allowed one AWX token per user.
    """
    Activation = apps.get_model("core", "Activation")  # noqa: N806
    AWXToken = apps.get_model("core", "AWXToken")  # noqa: N806
    for activation in Activation.objects.all():
        user = activation.user
        try:
            awx_token = AWXToken.objects.filter(user=user).first()
            if awx_token:
                activation.awx_token = awx_token
                activation.save()
        except AWXToken.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_auditaction_status_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="activation",
            name="awx_token",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.awxtoken",
            ),
        ),
        migrations.RunPython(
            populate_awx_token,
            reverse_code=migrations.RunPython.noop,
        ),
    ]

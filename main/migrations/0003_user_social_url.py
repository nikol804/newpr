from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_chat_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на соцсеть (VK и др.)'),
        ),
    ]



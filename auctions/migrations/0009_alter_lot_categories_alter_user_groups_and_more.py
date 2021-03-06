# Generated by Django 4.0 on 2022-06-20 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('auctions', '0008_delete_auctions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_lot', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='watchlist_item',
            field=models.ManyToManyField(blank=True, related_name='watchlists', to='auctions.Lot'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

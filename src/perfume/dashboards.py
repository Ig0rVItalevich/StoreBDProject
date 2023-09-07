from django.db import connection
from controlcenter import Dashboard, widgets

from app.models import Order


class ModelItemList(widgets.ItemList):
    def get_my_values_list():
        with connection.cursor() as cursor:
            query = """SELECT * FROM staff_actions();"""
            cursor.execute(query, ())
            result = cursor.fetchall()
        
        return result

    title = "Staff actions"

    my_values_list = get_my_values_list()

    print(my_values_list)

    list_display = ('entity', 'entity_id', 'user_id', 'action', 'action_time')

class MyDashboard(Dashboard):
    ModelItemList.my_values_list = ModelItemList.get_my_values_list()

    widgets = (
        ModelItemList,
    )
from flask import redirect, g

from flask_appbuilder import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from flask_babel import gettext as __
from flask_babel import lazy_gettext as _

from superset import appbuilder
from superset.models.sql_lab import Query, SavedQuery
from .base import SupersetModelView, BaseSupersetView, DeleteMixin


class QueryView(SupersetModelView):
    datamodel = SQLAInterface(Query)

    list_title = _('List Query')
    show_title = _('Show Query')
    add_title = _('Add Query')
    edit_title = _('Edit Query')

    list_columns = ['user', 'database', 'status', 'start_time', 'end_time']

    label_columns = {
        'user': _("User"),
        'database': _("Database"),
        'id': _("ID"),
        'client_id': _("Client ID"),
        'database_id': _("Database ID"),
        'tmp_table_name': _("Tmp Table Name"),
        'user_id': _("User ID"),
        'Integer': _("Integer"),
        'status': _("Status"),
        'tab_name': _("Tab Name"),
        'sql_editor_id': _("SQL Editor ID"),
        'schema': _("Schema"),
        'sql': _("SQL"),
        'select_sql': _("Select SQL"),
        'executed_sql': _("Executed SQL"),
        'limit': _("Limit"),
        'limit_used': _("Limit Used"),
        'select_as_cta': _("Select As Cta"),
        'select_as_cta_used': _("Select As Cta Used"),
        'progress': _("Progress"),
        'rows': _("Rows"),
        'error_message': _("Error Message"),
        'results_key': _("Results Key"),
        'start_time': _("Start Time"),
        'start_running_time': _("Start Running Time"),
        'end_time': _("End Time"),
        'end_result_backend_time': _("End Result Backend Time"),
        'tracking_url': _("Tracking Url"),
        'changed_on': _("Changed On")
    }

appbuilder.add_view(
    QueryView,
    "Queries",
    label=__("Queries"),
    category="Manage",
    category_label=__("Manage"),
    icon="fa-search")


class SavedQueryView(SupersetModelView, DeleteMixin):
    datamodel = SQLAInterface(SavedQuery)

    list_title = _('List Saved Query')
    show_title = _('Show Saved Query')
    add_title = _('Add Saved Query')
    edit_title = _('Edit Saved Query')

    list_columns = [
        'label', 'user', 'database', 'schema', 'description',
        'modified', 'pop_tab_link']
    show_columns = [
        'id', 'label', 'user', 'database',
        'description', 'sql', 'pop_tab_link']
    search_columns = ('label', 'user', 'database', 'schema', 'changed_on')
    add_columns = ['label', 'database', 'description', 'sql']
    edit_columns = add_columns
    base_order = ('changed_on', 'desc')
    label_columns = {
        'id': _("ID"),
        'label': _("Label"),
        'user': _("User"),
        'database': _("Database"),
        'schema': _("Schema"),
        'description': _("Description"),
        'modified': _("Last Modified"),
	'end_time': _('End Time'),
        'pop_tab_link': _("Pop Tab Link"),
        'sql': _("SQL"),
        'changed_on': _("Changed On"),
    }

    def pre_add(self, obj):
        obj.user = g.user

    def pre_update(self, obj):
        self.pre_add(obj)


class SavedQueryViewApi(SavedQueryView):
    show_columns = ['label', 'db_id', 'schema', 'description', 'sql']
    add_columns = show_columns
    edit_columns = add_columns

appbuilder.add_view_no_menu(SavedQueryViewApi)
appbuilder.add_view_no_menu(SavedQueryView)

appbuilder.add_link(
    __('Saved Queries'),
    href='/sqllab/my_queries/',
    icon="fa-save",
    category='SQL Lab')


class SqlLab(BaseSupersetView):
    """The base views for Superset!"""
    @expose("/my_queries/")
    def my_queries(self):
        """Assigns a list of found users to the given role."""
        return redirect(
            '/savedqueryview/list/?_flt_0_user={}'.format(g.user.id))


appbuilder.add_view_no_menu(SqlLab)

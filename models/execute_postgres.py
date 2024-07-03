from odoo import models, fields, api, _
from odoo.exceptions import UserError
import psycopg2

class ExecutePostgres(models.Model):
    _name = "execute.postgres"
    _description = "Execute PostgreSQL"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    HELPFUL_COMMANDS = """
    <p style='color:red;font-size:16px;'><b>Note before executing:<b></p>
    <p class='my-2'>- Uses ' ' instead of " "</p>
    <p>- Add RETURNING * to the end of the query</p>"""
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", required=True, default=True)
    psql_query = fields.Text(string="PSQL Query")
    result = fields.Html(string="Result", readonly=1)
    helpful_commands = fields.Html(string='Helpful Commands', readonly=1, default=HELPFUL_COMMANDS)
    last_execute = fields.Datetime(string="Last Execute", required=True, default=fields.Datetime.now, readonly=1)
    priority = fields.Selection([('0', 'Normal'),('1','Favorite')], string="Favorite")

    def execute_action(self):
        try:
            if self.psql_query:
                self._cr.execute(self.psql_query)
                description = self._cr.description
                result = self._cr.fetchall() if description else []
                self.result = self._create_html_table(result, description)
                self.write({'last_execute': fields.Datetime.now()})
        except Exception as e:
            raise UserError(_('Error executing SQL query: %s ', e))

    def clear_action(self):
        self.psql_query = False
        self.result = False

    def _create_html_table(self, data, description):
        if not description:
            return """
            <div class="alert alert-success" role="alert">
                Successfully executing the query
            </div>
            <div class="alert alert-warning" role="alert">
                If you want to display the executed data in tabular form next time, add 'RETURNING *' at the end of the query
            </div>
            """

        keys = [i[0] for i in description]
        table_header = ''.join(
            f"<th style='border:1px solid black'>{key}</th>" for key in keys
        )
        table_datas = ''.join(
            "<tr>" + ''.join(
                f"<td style='border:1px solid black'>{res}</td>" for res in row
            ) + "</tr>" for row in data
        )

        return f"""
            <div class="alert alert-success" role="alert">
                Successfully executing the query
            </div>
            <div style="overflow:auto;">
                <table class="table text-center table-border table-sm" style="width:max-content;">
                    <thead>
                        <tr style='border:1px solid black;background: lightblue;'>
                        {table_header}
                        </tr>
                    </thead>
                    <tbody>
                        {table_datas}
                    </tbody>
                </table>
            </div>"""


import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ExecutePostgres(models.Model):
    _name = "execute.postgres"
    _description = "Execute PostgreSQL"

    DEFAULT_HELPFUL = """<p style='color: red;'>#Note before executing:<p>
        - Uses ' ' instead of " "
        - Add RETURNING * to the end of the query"""
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", required=True, default=True)
    psql_query = fields.Text(string="PSQL Query")
    result = fields.Html(string="Result", readonly=1)
    helpful_commands = fields.Html(string='Helpful Commands', default=DEFAULT_HELPFUL)

    def execute_action(self):
        try:
            if self.psql_query:
                self._cr.execute(self.psql_query)
                keys = [i[0] for i in self._cr.description]
                table_header = ''
                table_datas = ''
                for key in keys:
                    table_header += (
                            "<th style='border:1px solid black'>%s"
                            "</th>" % key)
                result = self._cr.fetchall()
                for query_res in result:
                    table_datas += "<tr>"
                    for res in query_res:
                        table_datas += (
                            "<td style='border:1px solid black'>{0}"
                            "</td>".format(res))
                    table_datas += "</tr>"
                self.result = """
                <div style="overflow:auto;">
                    <table class="table text-center table-border table-sm" style="width:max-content";>
                        <thead>
                            <tr style='border:1px solid black;background: lightblue;'>
                            """ + str(table_header) + """
                            </tr>
                        </thead>
                        <tbody>
                            """ + str(table_datas) + """
                        </tbody>
                    </table>
                </div>"""
        except Exception as e:
            raise UserError(_('Error executing SQL query: %s ', e))

    def clear_action(self):
        self.psql_query = False
        self.result = False

    def _create_html_table(self, data, description):
        if not description:
            return "<div>No data returned.</div>"

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

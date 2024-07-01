from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64

class ExecutePython(models.Model):
    _name = "execute.python"
    _description = "Execute Python"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    DEFAULT_ENV_VARIABLES = """ #Available variables:
        #  - self: Current Object
        #  - self.env: Odoo Environment on which the action is triggered
        #  - self.env.user: Return the current user (as an instance)
        #  - self.env.is_system: Return whether the current user has group "settings", or is in superuser mode.
        #  - self.env.is_admin: Return whether the current user has group "Access Rights", or is in superuser mode.
        #  - self.env.is_superuser: Return Whether the environment is in superuser mode.
        #  - self.env.company: Return the current company (as an instance)
        #  - self.env.companies: Return a recordset of the enabled companies by the user  
        #  - self.env.lang: Return the current language code"""
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", required=True, default=True)
    python_code = fields.Text(string="Python Code", default=f"{DEFAULT_ENV_VARIABLES}\n\n")
    python_code_file = fields.Binary(string="Python Code File", readonly=1, attachment=True)
    result = fields.Text(string="Result", require=True, readonly=1)
    last_execute = fields.Datetime(string="Last Execute", required=True, default=fields.Datetime.now, readonly=1)
    def execute_action(self):
        local_dict = {'self': self, 'user': self.env.user}
        for record in self:
            try:
                # Execute the Python code in the context of local_dict
                exec(record.python_code, local_dict)
                # Update the result field with the result from local_dict
                if local_dict.get('result', False):
                    record.write({'result': local_dict['result']})
                else:
                    record.write({'result': False})
                record.write({'last_execute': fields.Datetime.now()})
            except Exception as e:
                raise UserError(_('Python code is not able to run ! message : %s' % (e)))

    def clear_action(self):
        self.python_code = f"{self.DEFAULT_ENV_VARIABLES}\n\n"
        self.result = False

    def download_action(self):
        self.ensure_one()
        # Encode the python code in base64
        self.python_code_file = base64.b64encode(self.python_code.encode('utf-8'))
        # Create the download URL
        download_url = '/web/content/?model=execute.python&id=%d&field=python_code_file&filename=%s.py&download=true' % (self.id, self.name)
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'self',
        }


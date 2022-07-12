import odoo
from odoo.api import Environment


def odoo_env() -> Environment:

    config = odoo.tools.config
    config["db_name"] = 'myodoodb'
    config["db_host"] = 'localhost'
    config["db_port"] = 5432
    config["db_user"] = 'odoo'
    config["db_password"] = '123qwe'

    registry = odoo.registry(config["db_name"]).check_signaling()
    with registry.manage_changes():
        with registry.cursor() as cr:
            yield Environment(cr, odoo.SUPERUSER_ID, {})
            
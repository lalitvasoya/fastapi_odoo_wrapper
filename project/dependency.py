import odoo
from odoo.api import Environment


def odoo_env() -> Environment:

    config = odoo.tools.config
    config["db_name"] = 'odoo_test_demo'
    config["db_host"] = 'localhost'
    config["db_port"] = 5432
    config["db_user"] = 'postgres'
    config["db_password"] = 'postgres'

    registry = odoo.registry(config["db_name"]).check_signaling()
    with registry.manage_changes():
        with registry.cursor() as cr:
            yield Environment(cr, odoo.SUPERUSER_ID, {})

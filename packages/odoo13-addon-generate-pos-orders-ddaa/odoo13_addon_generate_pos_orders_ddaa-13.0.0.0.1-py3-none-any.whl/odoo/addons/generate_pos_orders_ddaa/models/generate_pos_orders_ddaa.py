from odoo import models


class GeneratePOSOrdersDDAAWizard(models.TransientModel):
    """ Wizard: *** """
    _name = 'generate.pos.orders.ddaa.wizard'
    _description = "Wizard para generar DDAA de antiguos pedidos realizados desde POS"

    def generate_pos_orders_ddaa(self):
        print("******** POS ORDERS DDAA **********")

        ddaa_modified_products = {}
  
        pos_orders = self.env['pos.order'].search([('state', '!=', 'draft')])
        print(f"*** TOTAL POS ORDERS: {len(pos_orders)} ")
        for pos_order in pos_orders:
            for order_line in pos_order.lines:
                ddaa_modified_products[order_line.product_id.product_tmpl_id] = ddaa_modified_products.get(order_line.product_id.product_tmpl_id, 0) + order_line.qty
            #pos_order.generate_pos_ddaa()

        for product_template, qty in ddaa_modified_products.items():
            if(product_template.genera_ddaa):
                print(f"### PRODUCT ID: {(product_template.id)} - PRODUCT NAME: {(product_template.name)} - GENERATED DDAA: {(qty)} ")
                product_template.generate_ddaa(qty)
            
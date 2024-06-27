# -*- coding: utf-8 -*-
######################################################################################
#
#         License**
#
########################################################################################
{
    'name': 'Generar DDAA para pedidos POS',
    'version': '13.0.0.0.1',
    'summary': 'Módulo para generar DDAA para antiguos pedidos realizados desde POS.',
    'description': 'Módulo para generar DDAA para antiguos pedidos realizados desde POS.',
    'category': 'Industries',
    'author': 'Colectivo DEVCONTROL',
    'author_email': 'devcontrol@sindominio.net',
    'maintainer': 'Colectivo DEVCONTROL',
    'company': 'Colectivo DEVCONTROL',
    'website': 'https://framagit.org/devcontrol',
    'depends': ['gestion_editorial', 'point_of_sale'],
    'data': [
        'views/generate_pos_orders_ddaa_view.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'price': 0,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}

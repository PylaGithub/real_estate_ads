{
    "name": "Real Estate Ads",
    "version": "1.0",
    "summary": "Manage Real Estate Properties, Offers, Types, and Tags",
    "description": """
        A simple Real Estate module to manage properties, offers, property types, and property tags.
    """,
    "author": "Phani",
    "website": "https://yourwebsite.com",
    "category": "Real Estate",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/property_offer_views.xml',
        'views/estate_menus.xml',
        'data/property_type.xml',
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}

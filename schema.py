
# coding: utf-8

# In[ ]:

#!/usr/bin/env python


"""enables correct translation between XML tags and SQLITE3 data fields of tables.

.. module:: schema
   :platform: Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Udacity


"""

schema = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}
"""
schema defines and ensures which data and their data types shall be given for database transfer:

:param dict node: contains in it's attribute following information
    'id': {'required': True, 'type': 'integer', 'coerce': int},
    'lat': {'required': True, 'type': 'float', 'coerce': float},
    'lon': {'required': True, 'type': 'float', 'coerce': float},
    'user': {'required': True, 'type': 'string'},
    'uid': {'required': True, 'type': 'integer', 'coerce': int},
    'version': {'required': True, 'type': 'string'},
    'changeset': {'required': True, 'type': 'integer', 'coerce': int},
    'timestamp': {'required': True, 'type': 'string'}

:param list node_tags: contains in it's attribute following information
    'id': {'required': True, 'type': 'integer', 'coerce': int},
    'key': {'required': True, 'type': 'string'},
    'value': {'required': True, 'type': 'string'},
    'type': {'required': True, 'type': 'string'}

:param dict way: contains in it's attribute following information
    'id': {'required': True, 'type': 'integer', 'coerce': int},
    'user': {'required': True, 'type': 'string'},
    'uid': {'required': True, 'type': 'integer', 'coerce': int},
    'version': {'required': True, 'type': 'string'},
    'changeset': {'required': True, 'type': 'integer', 'coerce': int},
    'timestamp': {'required': True, 'type': 'string'}

:param list way_nodes: contains in it's attribute following information
    'id': {'required': True, 'type': 'integer', 'coerce': int},
    'node_id': {'required': True, 'type': 'integer', 'coerce': int},
    'position': {'required': True, 'type': 'integer', 'coerce': int}

:param list way_tags:  contains in it's attribute following information
    'id': {'required': True, 'type': 'integer', 'coerce': int},
    'key': {'required': True, 'type': 'string'},
    'value': {'required': True, 'type': 'string'},
    'type': {'required': True, 'type': 'string'}


"""


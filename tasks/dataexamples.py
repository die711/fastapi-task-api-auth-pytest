from tasks.schemas import StatusType

task_with_orm = {
    'normal 1': {
        'summary': 'A normal example',
        'description': 'A normal example',
        'value': {
            'name': 'Salvar el mundo',
            'description': 'Hola mundo Desc',
            'status': StatusType.PENDING,
            'category_id': 1,
            'user_id': 1
        }
    },

    'normal 2': {
        'summary': 'A normal example',
        'description': 'A normal example',
        'value': {
            'name': 'Sacar la basura',
            'description': 'Hola mundo Desc',
            'status': StatusType.PENDING,
            'category_id': 1,
            'user_id': 1
        }
    },

    'invalid': {
        'summary': 'Invalid data is rejected with an error',
        'description': 'A normal example',
        'value': {
            'name': 'Salvar el mundo',
            'description': 'Hola mundo Desc',
            'status': StatusType.PENDING,
            'user_id': {
                'id': 1,
                'name': 'admin@admin.com',
                'email': 'admin@admin.com',
                'surname': 'Cruz',
                'website': 'https://desarrollo.net'
            }
        }
    },
}

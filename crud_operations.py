from tasks.database.database import get_database_session
from tasks.database import models

db = next(get_database_session())
user = db.query(models.User).get(1)

print('---------------User---------------')

print(f'id: {user.id}')
print(f'name: {user.name}')
print(f'surname: {user.surname}')
print(f'email: {user.email}')
print(f'website: {user.website}')
print(f'hashed_password: {user.hashed_password}')

for task in user.tasks:
    print(f'task: {task.name}')

print('--------------Category-----------------')
category = db.query(models.Category).get(1)

print(f'id: {category.id}')
print(f'name: {category.name}')

print('---------------Tag-------')

tag = models.Tag(name='Tag test')
print(f'id: {tag.id}')
print(f'name: {tag.name}')

# db.add(tag)
# db.commit()
# db.refresh(tag)
print(f'id: {tag.id}')
print(f'name: {tag.name}')

print('-------------Task---------------')

task = db.query(models.Task).get(1)
print(f'id: {task.id}')
print(f'name: {task.name}')
print(f'description: {task.description}')
print(f'status: {task.status}')
print(f'category.name: {task.category.name}')
print(f'user.name: {task.user.name}')

for tag in task.tags:
    print(f'tag: {tag.name}')

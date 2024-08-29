from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import time

from tasks.routes.annotated import annotated_router
from tasks.routes.basic import basic_router
from tasks.routes.user import user_router
from tasks.routes.myupload import upload_router
from tasks.routes.task import task_router
from tasks.routes.auth import auth_router
from tasks.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(annotated_router, tags=['annotated'])
app.include_router(task_router, prefix='/tasks', tags=['tasks'])
app.include_router(upload_router, prefix='/upload', tags=['upload'])
app.include_router(basic_router, prefix='/basic', tags=['basic'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(user_router)


@app.middleware('http')
async def add_process_time_to_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


def background_task_function(message=''):
    print('Heavy Task start ' + message)
    time.sleep(3)
    print('Heavy Task end')
    time.sleep(3)
    print('Heavy Task end')


@app.get('/background')
async def send_notification(background_task: BackgroundTasks):
    background_task.add_task(background_task_function, message='some message')
    return {
        'message': 'Send Message'
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

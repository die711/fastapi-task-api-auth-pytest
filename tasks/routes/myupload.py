from fastapi import APIRouter, File, UploadFile
from typing import List
import shutil

upload_router = APIRouter()


@upload_router.post('/file')
def upload_file(file: bytes = File()):
    return {
        'file_size': len(file)
    }


@upload_router.post('/uploadfile1')
def upload_file2(file: UploadFile):
    return {
        'filename': file.filename,
        'content-type': file.content_type
    }


@upload_router.post('/uploadfile2')
def upload_file3(file: UploadFile):
    with open('tasks/img/image.jpg', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {
            'filename': file.filename
        }


@upload_router.post('/uploadfile3')
def upload_file4(images: List[UploadFile]):
    for image in images:
        with open('tasks/img/' + image.filename, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {
        'files': len(images)
    }

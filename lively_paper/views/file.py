import json

from django.core.files import File
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from langchain.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from lively_paper.service.magic import magic
from lively_paper.vector import stores
from lively_paper.views.json_response import JsonObjectResponse


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    file: File = request.FILES['file']
    if not file:
        return HttpResponse()
    tmp_file_path = '/tmp/' + file.name
    with open(tmp_file_path, 'wb+') as destination:
        for chunks in file.chunks():
            destination.write(chunks)
    pdf_loader = PyPDFium2Loader(tmp_file_path)
    pages = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len
    )

    documents = text_splitter.split_documents(pages)
    stores.vector_store.add_documents(documents)
    return HttpResponse('保存成功')


@require_POST
def fetch_url(request: HttpRequest) -> JsonObjectResponse:
    data = json.loads(request.body)
    docs = magic['url'](data)
    return JsonObjectResponse(docs, safe=False)


@require_GET
def list() -> HttpResponse:
    return HttpResponse()

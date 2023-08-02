from django.core.files import File
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from lively_paper.vector import stores


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    file: File = request.FILES['file']
    if not file:
        return HttpResponse()
    tmp_file_path = '/tmp/' + file.name
    with open(tmp_file_path, 'wb+') as destination:
        for chunks in file.chunks():
            destination.write(chunks)
    pdf_loader = PyPDFLoader(tmp_file_path)
    pages = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len
    )

    documents = text_splitter.split_documents(pages)
    stores.vectorStore.add_documents(documents)
    return HttpResponse('保存成功')

@require_GET
def list() -> HttpResponse:
    return HttpResponse()

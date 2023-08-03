import json
from queue import SimpleQueue
from threading import Thread
from typing import Sequence

from django.http import HttpRequest, StreamingHttpResponse, HttpResponseBase, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.schema import Document

from lively_paper.model.llms import openai
from lively_paper.scalar import stores
from lively_paper.vector.stores import vector_store
from lively_paper.views.json_response import JsonObjectResponse
from lively_paper.views.response_callback import ResponseCallback, job_done


@require_POST
def chat(request: HttpRequest) -> HttpResponseBase:
    data = json.loads(request.body)
    query: str = data['query']
    mode: str = data.get('mode', 'streaming')

    if mode == 'streaming':
        qa = RetrievalQA.from_chain_type(llm=openai, chain_type="stuff",
                                         retriever=vector_store.as_retriever(search_type='similarity_score_threshold',
                                                                             search_kwargs={'score_threshold': 0.07,
                                                                                            'k': 5}),
                                         return_source_documents=True)
        queue = SimpleQueue()
        callback = ResponseCallback(queue)
        thread = Thread(target=qa, kwargs={'inputs': {'query': query},
                                           'callbacks': [StreamingStdOutCallbackHandler(), callback]})
        thread.start()

        def pull_token():
            while True:
                next_token = queue.get(block=True)
                if next_token is job_done:
                    if callback.documents:
                        yield '\n***'
                        documents = merge_document(callback.documents)
                        for document in documents:
                            yield f'\n* `{document}`'
                    break
                yield next_token
            thread.join()

        def merge_document(documents: Sequence[Document]):
            return set(map(lambda document: document.metadata['source'], documents))

        return StreamingHttpResponse(pull_token())
    else:
        qa = RetrievalQA.from_chain_type(llm=openai, chain_type="stuff", retriever=vector_store.as_retriever(),
                                         return_source_documents=True)
        result = qa({'query': query})
        return JsonObjectResponse(result)


@require_POST
def new_chat(request: HttpRequest) -> JsonObjectResponse:
    body = json.loads(request.body)
    stores.insert('history', body)
    return JsonObjectResponse(body)


@require_POST
def rename_chat(request: HttpRequest) -> JsonObjectResponse:
    body = json.loads(request.body)



@require_GET
def histories(request: HttpRequest) -> HttpResponse:
    return HttpResponse('1')

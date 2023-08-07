import json
from queue import SimpleQueue
from threading import Thread
from typing import Sequence

from django.http import HttpRequest, StreamingHttpResponse, HttpResponseBase, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.memory import MongoDBChatMessageHistory, ConversationBufferMemory
from langchain.schema import Document, BaseChatMessageHistory

from lively_paper.chain.memory_retrieval_qa import MemoryRetrievalQA
from lively_paper.chain.prompt import PROMPT
from lively_paper.model.llms import openai
from lively_paper.scalar.stores import scalar_store
from lively_paper.vector.stores import vector_store
from lively_paper.views.json_response import JsonObjectResponse
from lively_paper.views.response_callback import ResponseCallback, job_done


@require_POST
def chat(request: HttpRequest) -> HttpResponseBase:
    data = json.loads(request.body)
    query: str = data['query']
    mode: str = data.get('mode', 'streaming')
    session_id: str = data['id']

    chat_memory: BaseChatMessageHistory = MongoDBChatMessageHistory(connection_string=scalar_store.connection,
                                                                    session_id=session_id)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer',
                                      chat_memory=chat_memory)
    qa = MemoryRetrievalQA.from_llm(llm=openai, chain_type="stuff", memory=memory, return_source_documents=True,
                                    retriever=vector_store.as_retriever(
                                        search_type='similarity_score_threshold',
                                        search_kwargs={'score_threshold': 0.07, 'k': 5}),
                                    combine_docs_chain_kwargs={'prompt': PROMPT})
    if mode == 'streaming':
        queue = SimpleQueue()
        callback = ResponseCallback(queue)
        thread = Thread(target=qa, kwargs={'inputs': {'question': query},
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
        result = qa(inputs={'question': query})
        return JsonObjectResponse(result)


@require_POST
def new_chat(request: HttpRequest) -> JsonObjectResponse:
    body = json.loads(request.body)
    scalar_store.insert('history', {'SessionId': body['id'], 'Title': body['title']})
    return JsonObjectResponse(body)


@require_GET
def delete_history(request: HttpRequest, session_id: str) -> JsonObjectResponse:
    scalar_store.delete('history', {'SessionId': session_id})
    return JsonObjectResponse({})


@require_GET
def find_history(request: HttpRequest, session_id: str) -> JsonObjectResponse:
    history_item = scalar_store.find('history', {'SessionId': session_id})
    return JsonObjectResponse(history_item, safe=False)


@require_POST
def rename_chat(request: HttpRequest) -> JsonObjectResponse:
    body = json.loads(request.body)


@require_GET
def histories(request: HttpRequest) -> JsonObjectResponse:
    return JsonObjectResponse(scalar_store.list('history'), safe=False)


@require_GET
def history(request: HttpRequest, session_id: str) -> JsonObjectResponse:
    store_list = scalar_store.list('message_store', {'SessionId': session_id})

    result = []
    for index in range(0, len(store_list), 2):
        human = json.loads(store_list[index]['History'])
        ai = json.loads(store_list[index + 1]['History'])
        result_item = {
            'question': human['data']['content'],
            'answer': ai['data']['content']
        }
        result.append(result_item)
    return JsonObjectResponse(result, safe=False)

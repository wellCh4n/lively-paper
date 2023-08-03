
const BASE_URL = 'http://127.0.0.1:8000'

const get = (path) => {
  return fetch(BASE_URL + path, {
    method: 'GET',
  })
}

const postData = (path, data) => {
  return fetch(BASE_URL + path, {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

const postForm = (path, form) => {
  return fetch(BASE_URL + path, {
    method: 'POST',
    body: form
  })
}

export {
  get, postData
}
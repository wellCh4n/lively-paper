import {ElMessage} from 'element-plus'
import {nextTick} from 'vue'
import {postData} from '@/utils/request'

const magic = {
  new: {
    ready: (that) => {
      that.emit('new-chat', '')
      ElMessage({message: 'Create a new Chat~'})
    },
    name: 'New Chat',
    description: 'New Chat',
    paramKeys: ['title'],
    clear: true
  },
  file: {
    ready: (that) => {},
    name: 'Upload File',
    description: 'Upload File To Repository',
    paramKeys: ['file'],
    clear: false
  },
  url: {
    ready: (that, params, event) => {
      if ((!params.preview || params.preview === 'false') && !event) {
        return
      }

      that.exposed.setDrawerShow(true)
      nextTick(() => {
        that.exposed.getDrawerInner().value.innerHTML = ''
        postData('/file/url', {
          url: params.url
        }).then((res) => {
          that.exposed.getDrawerInner().value.innerHTML = `<p>${res[0].page_content}</p>`
        })
      })
    },
    name: 'Fetch content from URL',
    description: 'Fetch content from URL',
    paramKeys: ['url', 'preview'],
    clear: false
  },
  clear: {
    ready: (that, params) => {},
    name: 'New Chat',
    description: 'New Chat',
    paramKeys: [],
    clear: true
  }
}

const parseParams = (prompt, paramKeys) => {
  const promptCommand = prompt.split(' ')
  const commandArr = promptCommand.slice(1, promptCommand.length)
  const param = {}
  paramKeys.forEach((key, index) => {
    param[key] = commandArr[index]
  })
  return param
}

const matchMagic = (prompt) => {
  const magicKey = prompt.slice(1, prompt.length)
  const magicObject = magic[magicKey]
  if (magicObject) {
    magicObject['key'] = magicKey
    return magicObject
  }
}

export {
  magic, matchMagic, parseParams
}
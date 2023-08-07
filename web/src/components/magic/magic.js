import {ElMessage} from 'element-plus'
import {nextTick} from 'vue'
import {postData} from '@/utils/request'

const magic = {
  new: {
    ready: (that) => {
      that.emit('new-chat', '')
      ElMessage({ message: 'Create a new Chat~'})
    },
    submit: () => {},
    name: 'New Chat',
    description: 'New Chat',
    paramKeys: ['title'],
  },
  file: {
    ready: (that) => {},
    submit: () => {},
    name: 'Upload File',
    description: 'Upload File To Repository',
    paramKeys: ['file']
  },
  url: {
    ready: (that, params) => {
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
    submit: (that, params, context) => {
      console.log(params)
    },
    name: 'Fetch content from URL',
    description: 'Fetch content from URL',
    paramKeys: ['url']
  }
}

const inputClean = (that) => {
  that.refs.promptInput.clear()
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
    return magicObject
  }
}

export {
  magic, matchMagic, parseParams
}
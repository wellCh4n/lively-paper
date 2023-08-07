const magic = {
  new: {
    fn: (that) => {
      that.emit('new-chat', '')
    },
    name: 'New Chat',
    description: 'New Chat',
    params: ['title']
  },
  upload: {
    fn: (that) => {
      console.log('上传文件')
    },
    name: 'Upload File',
    description: 'Upload File To Repository',
    params: ['file']
  }
}

const inputClean = (that) => {
  that.refs.promptInput.clear()
}

const matchMagic = (prompt) => {
  const magicKey = prompt.slice(1, prompt.length)
  const magicObject = magic[magicKey]
  if (magicObject) {
    return magicObject
  }
}

export {
  magic, matchMagic
}
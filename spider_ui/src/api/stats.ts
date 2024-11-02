import request from '@/utils/request'

const getWebsiteCount = () => {
  return request({
    url: '/getWebsiteCount',
    method: 'get',
  })
}

const getWordCloud = () => {
  return request({
    url: '/getWordCloud',
    method: 'get',
  })
}

const getRanked = () => {
  return request({
    url: '/getRanked',
    method: 'get',
  })
}

const getReadCount = () => {
  return request({
    url: '/getReadCount',
    method: 'get',
  })
}

const getBlogDiggNum = () => {
  return request({
    url: '/getBlogDiggNum',
    method: 'get',
  })
}

const getCollectCount = () => {
  return request({
    url: '/getCollectCount',
    method: 'get',
  })
}

const getDataCounts = () => {
  return request({
    url: '/getDataCounts',
    method: 'get',
  })
}
export {
  getWebsiteCount,
  getWordCloud,
  getRanked,
  getReadCount,
  getBlogDiggNum,
  getCollectCount,
  getDataCounts,
}

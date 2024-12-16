import request from '@/utils/request'
const prefix = '/csdn'
const getWebsiteCount = () => {
  return request({
    url: `${prefix}/getWebsiteCount`,
    method: 'get',
  })
}

const getWordCloud = () => {
  return request({
    url: `${prefix}/getWordCloud`,
    method: 'get',
  })
}

const getRanked = () => {
  return request({
    url: `${prefix}/getRanked`,
    method: 'get',
  })
}

const getReadCount = () => {
  return request({
    url: `${prefix}/getReadCount`,
    method: 'get',
  })
}

const getBlogDiggNum = () => {
  return request({
    url: `${prefix}/getBlogDiggNum`,
    method: 'get',
  })
}

const getCollectCount = () => {
  return request({
    url: `${prefix}/getCollectCount`,
    method: 'get',
  })
}

const getDataCounts = () => {
  return request({
    url: `${prefix}/getDataCounts`,
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

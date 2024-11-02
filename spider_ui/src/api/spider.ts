import request from '@/utils/request'

const getSpiderList = () => {
  return request({
    url: '/spider/list',
    method: 'get',
  })
}

interface stopSpiderRequest {
  spider_id: string
}
const stopSpider = (data: stopSpiderRequest) => {
  return request({
    url: '/spider/stop',
    method: 'post',
    data: data,
  })
}

interface startSpiderRequest {
  spider_name: string
}
const startSpider = (data: startSpiderRequest) => {
  return request({
    url: '/spider/start',
    method: 'post',
    data: data,
  })
}

const getSpiderSupport = () => {
  return request({
    url: '/spider/support',
    method: 'get',
  })
}

export { getSpiderList, stopSpider, startSpider, getSpiderSupport }

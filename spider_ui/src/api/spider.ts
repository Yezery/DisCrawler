import request from '@/utils/request'

const getSpiderList = () => {
  return request({
    url: '/system/spider/list',
    method: 'get',
  })
}

interface stopSpiderRequest {
  spider_id: string
}
const stopSpider = (data: stopSpiderRequest) => {
  return request({
    url: '/system/spider/stop',
    method: 'post',
    data: data,
  })
}

interface startSpiderRequest {
  spider_name: string
  spider_args: Record<string, string>
  description:string
}
const startSpider = (data: startSpiderRequest) => {
  return request({
    url: '/system/spider/start',
    method: 'post',
    data: data,
  })
}

const getSpiderSupport = () => {
  return request({
    url: '/system/spider/support',
    method: 'get',
  })
}

export { getSpiderList, stopSpider, startSpider, getSpiderSupport }

import request from '@/utils/request'

interface SearchRequest {
  query: string
}

const searchAPI = (data: SearchRequest) => {
  return request({
    url: '/search',
    method: 'post',
    data: data,
  })
}

export { searchAPI }

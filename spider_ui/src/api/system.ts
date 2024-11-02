import request from '@/utils/request'

const getSystemInfo = () => {
  return request({
    url: '/system_info',
    method: 'get',
  })
}

export { getSystemInfo }

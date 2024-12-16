import request from '@/utils/request'

const getSystemInfo = () => {
  return request({
    url: '/system/system_info',
    method: 'get',
  })
}

export { getSystemInfo }

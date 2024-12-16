import request from '@/utils/request'
const prefix = '/boss'
const getJobDistribution = () => {
  return request({
    url: `${prefix}/job/distribution`,
    method: 'get',
  })
}
const getJobDegree = () => {
  return request({
    url: `${prefix}/job/degree`,
    method: 'get',
  })
}
const getJobSkills = () => {
  return request({
    url: `${prefix}/job/skills`,
    method: 'get',
  })
}
const getJobExperience = () => {
  return request({
    url: `${prefix}/job/experience`,
    method: 'get',
  })
}

const getCompanyFinance = () => {
  return request({
    url: `${prefix}/company/finance`,
    method: 'get',
  })
}
const getCompanySize = () => {
  return request({
    url: `${prefix}/company/size`,
    method: 'get',
  })
}
const getCompanyIndustry = () => {
  return request({
    url: `${prefix}/company/industry`,
    method: 'get',
  })
}
const getJobSalaryAll = () => {
  return request({
    url: `${prefix}/job/salary/all`,
    method: 'get',
  })
}
const getDataCount = () => {
  return request({
    url: `${prefix}/count/data`,
    method: 'get',
  })
}
const getCityCount = () => {
  return request({
    url: `${prefix}/count/city`,
    method: 'get',
  })
}
const getLatestData = () => {
  return request({
    url: `${prefix}/latest/data`,
    method: 'get',
  })
}
const getCompanyCount = () => {
  return request({
    url: `${prefix}/count/company`,
    method: 'get',
  })
}
const getAnalysisJobkey = () => {
  return request({
    url: `${prefix}/analysis/jobkey`,
    method: 'get',
  })
}
const getSalaryBrand = () => {
  return request({
    url: `${prefix}/analysis/salary_brand`,
    method: 'get',
  })
}
const getSalaryByCompanySize = () => {
  return request({
    url: `${prefix}/analysis/salary_companySize`,
    method: 'get',
  })
}
const getSalaryByDegree = () => {
  return request({
    url: `${prefix}/analysis/salary_degree`,
    method: 'get',
  })
}
const getSalaryByExperience = () => {
  return request({
    url: `${prefix}/analysis/salary_experience`,
    method: 'get',
  })
}
export {
  getJobDistribution,
  getJobDegree,
  getJobSkills,
  getJobExperience,
  getCompanyFinance,
  getCompanySize,
  getCompanyIndustry,
  getJobSalaryAll,
  getDataCount,
  getCityCount,
  getLatestData,
  getCompanyCount,
  getAnalysisJobkey,
  getSalaryBrand,
  getSalaryByCompanySize,
  getSalaryByDegree,
  getSalaryByExperience,
}

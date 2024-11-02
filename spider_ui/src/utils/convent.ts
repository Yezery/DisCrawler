const covent_time = (time: string) => {
  // 秒级时间戳格式化 YYYM/MM/DD HH:mm:ss
  const date = new Date(Number(time) * 1000)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()
  return `${year}-${month.toString().padStart(2, '0')}-${day} ${hour}:${minute}:${second}`
}
export { covent_time }

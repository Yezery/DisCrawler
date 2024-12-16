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

function applyStyles(el: HTMLElement, cssString: string) {
  const styles: Record<string, string> = {}
  cssString = cssString.replace(/[{}]/g, '').replace(/\n/g, '').trim()
  cssString
    .trim()
    .split(';')
    .forEach(style => {
      if (style) {
        const [key, value] = style.split(':').map(s => s.trim())
        if (key && value) {
          const camelCaseKey = key.replace(/-([a-z])/g, (_, letter) =>
            letter.toUpperCase(),
          )
          styles[camelCaseKey] = value
        }
      }
    })
  Object.entries(styles).forEach(([key, value]) => {
    el.style.setProperty(key.replace(/([A-Z])/g, '-$1').toLowerCase(), value)
  })
}
export { covent_time, applyStyles }

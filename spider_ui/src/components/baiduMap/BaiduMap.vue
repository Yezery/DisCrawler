<template>
  <div class="all">
    <div id="allmap"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let map: any = null
onMounted(() => {
  loadMapScript() // 加载百度地图资源
})
// 初始化地图
const init = () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const { BMap } = window as any // 注意要带window，不然会报错（注意官方api,会有改动，之前是Bmap,后面3.0版本改为了BMap,最好查文档或者打印一下window）
  map = new BMap.Map('allmap') // allmap必须和dom上的id一直
  map.centerAndZoom(new BMap.Point(118.43093852790834, 29.876613529599215), 15) // 初始化地图,设置中心点坐标和地图级别
  map.setCurrentCity('成都')
  map.enableScrollWheelZoom(true)
}
const loadMapScript = () => {
  // 此处在所需页面引入资源就是，不用再public/index.html中引入
  const script = document.createElement('script')
  script.type = 'text/javascript'
  script.className = 'loadmap' // 给script一个类名
  script.src = 'https://api.map.baidu.com/getscript?v=3.0&ak=你的ak'
  // 此处需要注意：申请ak时，一定要应用类别一定要选浏览器端，不能选服务端，不然地图会报ak无效
  script.onload = () => {
    // 使用script.onload，待资源加载完成，再初始化地图
    init()
  }
  const loadmap = document.getElementsByClassName('loadmap')
  if (loadmap) {
    // 每次append script之前判断一下，避免重复添加script资源标签
    for (let i = 0; i < loadmap.length; i++) {
      document.body.removeChild(loadmap[i])
    }
  }

  document.body.appendChild(script)
}
</script>
<style lang="less" scoped>
.all {
  width: 100%;
  height: 100%;
  #allmap {
    // 注意给dom宽高，不然地图不出来
    width: 100%;
    height: 100%;
  }
}
</style>

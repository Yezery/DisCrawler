<template>
  <div v-loading="loading" class="h-full w-full rounded-[1rem] overflow-hidden">
    <div id="charts-content" class="w-full h-full"></div>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

import * as echarts from 'echarts'
import 'echarts-wordcloud'
import {
  // onBeforeMount,
  onMounted,
  ref,
  watch,
  // onBeforeUnmount,
  // onUnmounted,
} from 'vue'
interface WordCloudData {
  name: string
  value: number
}
const props = defineProps({
  data: {
    type: Array<WordCloudData>,
    default: () => [],
  },
})
const { data } = toRefs(props)

const mychart = ref()
function DrawWordCloud() {
  // 词云
  if (mychart.value == undefined) {
    mychart.value = echarts.init(document.getElementById('charts-content'))
  }
  // mychart.getDom().style.backgroundColor = '#EEEDEB'
  mychart.value.setOption({
    series: {
      type: 'wordCloud',
      /**
       * 绘制词云的形状, 值为回调函数 或 关键字, 默认 circle
       *  关键字:
       *
       * circle（圆形）  词的数量不太多的时候，效果不明显，它会趋向于画一个椭圆
       * cardioid（苹果形或心形曲线）
       * diamond（菱形 正方形）
       * triangle-forward（三角形-向前）
       * triangle（三角形-直立）
       * pentagon（五边形）
       * star（星形）
       */
      shape: 'star',
      // 保持 maskImage 的纵横比或形状的纵横比为 1：1
      keepAspect: true,
      /**
       * 词云轮廓图，支持为 HTMLImageElement, HTMLCanvasElement，不支持路径字符串, 不包含白色区域; 可选选项
       * shape选项将随着云的形状增长而继续应用
       * 有形状限制的时候，最好用背景图来实现，而且这个背景图一定要放base64的，不然词云画不出来
       */
      // maskImage: maskImage,

      // 词云整个图表放置的位置 和 尺寸大小
      left: 'center',
      top: 'center',
      width: '100%',
      height: '100%',
      right: null,
      bottom: null,
      // 词云文本大小范围,  默认为最小12像素，最大60像素
      sizeRange: [15, 70],
      // 词云文字旋转范围和步长。 文本将通过旋转在[-90，90]范围内随机旋转步骤45
      // 如果都设置为 0 , 则是水平显示
      rotationRange: [-90, 90],
      rotationStep: 45,
      /**
       * 词间距, 距离越大，单词之间的间距越大, 单位像素
       * 这里间距太小的话，会出现大词把小词套住的情况，比如一个大的口字，中间会有比较大的空隙，这时候他会把一些很小的字放在口字里面，这样的话，鼠标就无法选中里面的那个小字
       */
      gridSize: 8,
      // 设置为true可以使单词部分在画布之外绘制, 允许绘制大于画布大小的单词
      drawOutOfBound: false,
      /**
       * 布局的时候是否有动画
       * 注意：禁用时，当单词较多时，将导致UI阻塞。
       */
      layoutAnimation: true,
      // 这是全局的文字样式，相对应的还可以对每个词设置字体样式
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        // 颜色可以用一个函数来返回字符串
        color: function () {
          // 随机颜色
          return (
            'rgb(' +
            [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
            ].join(',') +
            ')'
          )
        },
      },
      // 鼠标hover的特效样式
      emphasis: {
        focus: 'self',
        textStyle: {
          textShadowBlur: 10,
        },
      },

      /**
       * 词云数据，必须是一个数组，每个数组项必须有name和value属性
       * 设置单个文本的样式：  textStyle
       */
      data: data.value,
    },
  })
  loading.value = false
}
const loading = ref(false)
// const interval = ref()
onMounted(() => {
  loading.value = true
})
watch(data, () => {
  DrawWordCloud()
})

// onBeforeMount(() => {
//   interval.value = setInterval(() => {
//     getWordCloud().then(res => {
//       data.value = res.data.data
//       DrawWordCloud()
//       loading.value = false
//     })
//   }, 10000)
// })
// onBeforeUnmount(() => {
//   clearInterval(interval.value)
// })
// onUnmounted(() => {
//   clearInterval(interval.value)
// })
</script>

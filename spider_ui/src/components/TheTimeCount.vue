<template>
  <div v-loading="loading" class="w-full h-full rounded-[1rem] overflow-hidden">
    <div id="charts-test" class="w-full h-full"></div>
  </div>
</template>

<script lang="ts" setup>
import { getDataCounts } from '@/api/stats'
import * as echarts from 'echarts'
import { onMounted, onBeforeUnmount, ref, onUnmounted } from 'vue'
const loading = ref(false)
const xData = ref([])
const chartOptions = ref({
  // title: {
  //   text: '',
  //   subtext: '过去爬取的数据量',
  //   left: 'center',
  //   top: '10%',
  //   color: '#A1A2AF',
  //   fontFamily: 'Gilroy-Medium',
  //   fontSize: 20,
  //   lineHeight: 24,
  //   fontWeight: 'bold',
  //   subtextStyle: {
  //     color: '#ffffff',
  //     fontSize: 28,
  //     fontFamily: 'Gilroy-Bold',
  //     fontWeight: 'bold',
  //     lineHeight: 36,
  //   },
  // },
  grid: [
    {
      top: '10%',
    },
  ],
  xAxis: {
    type: 'category',
    data: xData,
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    axisLabel: {
      color: '#2E335B', //坐标值的具体的颜色
      // fontSize: window.innerHeight * 0.02 + '',
      // 加粗
      fontWeight: 'bold',
      fontFamily: 'Gilroy-Medium',
    },
    boundaryGap: true, // 坐标轴两侧留白策略
  },
  yAxis: {
    splitLine: {
      show: true,
      lineStyle: {
        color: '#2E335B', // 水平分割线颜色
        width: 0.3, // 水平分割线宽度
      },
    },
    show: true,
  },
  series: [
    {
      type: 'line',
      smooth: true,
      data: [],
      itemStyle: {
        color: '#2E335B', //改变折线点的颜色
        lineStyle: {
          width: 6,
        },
      },
      emphasis: {
        itemStyle: {
          color: 'white',
        },
        label: {
          show: true, // 显示提示标签
          padding: [15, 25, 15, 25], // 标签内边距
          formatter: '{b} 内 {c} 条', // 标签内容格式
          fontWeight: 'bolder',
          borderRadius: [10, 10, 10, 10], // 设置
          borderColor: 'white',
          backgroundColor: '#1e1e2c', // 标签背景色
          position: 'bottom',
          fontSize: 14,
          color: 'white',
        },
      },
      symbol: 'emptyCircle', // 空心圆作为转折点标志
      symbolSize: 12, // 转折点标志大小
      lineStyle: {
        type: 'solid', // 折线类型为实线
      },
      areaStyle: {
        // 折线图区域填充样式
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 1,
              color: 'rgba(46, 51, 91, 0.00)', // 折线图填充色的起始颜色和透明度
            },
            {
              offset: 0,
              color: 'rgba(46, 51, 91, 0.50)', // 折线图填充色的结束颜色和透明度
            },
          ],
          globalCoord: false, // 缺省为 false
        },
      },
    },
  ],
})
const mychart = ref()
function DrawWordCloud() {
  if (mychart.value == undefined) {
    mychart.value = echarts.init(document.getElementById('charts-test'))
  }
  // mychart.getDom().style.backgroundColor = '#EEEDEB'
  mychart.value.setOption(chartOptions.value)
}
const interval = ref()
onMounted(() => {
  loading.value = true
  getDataCounts().then(re => {
    xData.value = re.data.xAxis
    chartOptions.value.series[0].data = re.data.data
    DrawWordCloud()
    loading.value = false
  })

  interval.value = setInterval(() => {
    getDataCounts().then(re => {
      xData.value = re.data.xAxis
      chartOptions.value.series[0].data = re.data.data
      DrawWordCloud()
    })
  }, 5000)
})

onBeforeUnmount(() => {
  clearInterval(interval.value)
})
onUnmounted(() => {
  clearInterval(interval.value)
})
</script>

<style></style>

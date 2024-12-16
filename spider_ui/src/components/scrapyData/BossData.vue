<template>
  <div className="divider"></div>
  <div class="col-span-2 grid grid-cols-4 grid-rows-1 mt-10 mb-10 pl-10 pr-10">
    <div>
      <div class="pl-5 text-sm text-left text-[#2E335B]">招聘岗位</div>
      <div>
        <span
          v-loading="loading5"
          class="mt-3 mb-3 pl-5 text-left font-medium text-3xl tracking-tight text-gray-900"
          >{{ dataCount }}</span
        >
        <span class="text-sm"> 个</span>
      </div>
    </div>

    <div>
      <div class="pl-5 text-sm text-left text-[#2E335B]">招聘公司</div>
      <div>
        <span
          v-loading="loading6"
          class="mt-3 mb-3 pl-5 text-left font-medium text-3xl tracking-tight text-gray-900"
          >{{ Company_count }}</span
        >
        <span class="text-sm"> 个</span>
      </div>
    </div>

    <div>
      <div class="pl-5 text-sm text-left text-[#2E335B]">招聘城市</div>
      <div>
        <span
          v-loading="loading8"
          class="mt-3 mb-3 pl-5 text-left font-medium text-3xl tracking-tight text-gray-900"
          >{{ cityCount }}</span
        >
        <span class="text-sm"> 个</span>
      </div>
    </div>
    <div>
      <div class="pl-5 text-sm text-left text-[#2E335B]">数据更新时间</div>
      <div>
        <span
          v-loading="loading7"
          class="mt-3 mb-3 pl-5 text-left font-medium text-2xl tracking-tight text-gray-900"
          >{{ latestData }}</span
        >
      </div>
    </div>

  </div>
  <div className="divider"></div>
  <div
    class="grid grid-cols-2 mt-12 grid-rows-9 pl-5 pr-5 pt-2 w-full h-full bg-white animate__animated animate__fadeIn"
  >
    <div class="w-full h-full">
      <div class="w-full h-[36rem]" v-loading="loading" id="map"></div>
    </div>
    <div class="w-full h-full">
      <WordCloud :data="Skill_data" />
    </div>
    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div
        v-loading="loading10"
        class="w-full h-full"
        id="analysisJobKey"
      ></div>
    </div>

    <div
      :class="[
        'col-span-2 grid grid-cols-2 gap-10 grid-rows-1',
        !loading1 ? 'skeleton' : '',
      ]"
    >
      <div v-loading="loading1" class="w-full h-full" id="jobDegree"></div>
      <div v-loading="loading3" class="w-full h-full" id="jobExperience"></div>
    </div>

    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div v-loading="loading9" class="w-full h-full" id="salary"></div>
    </div>

    <div class="col-span-2 grid grid-cols-2 gap-10 grid-rows-1 mt-20">
      <div v-loading="loading2" class="w-full h-full" id="companySize"></div>
      <div v-loading="loading4" class="w-full h-full" id="companyFinance"></div>
    </div>
    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div
        v-loading="loading11"
        class="w-full h-full"
        id="analysisSalaryBrand"
      ></div>
    </div>
    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div
        v-loading="loading12"
        class="w-full h-full"
        id="analysisSalaryCompanySize"
      ></div>
    </div>
    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div
        v-loading="loading13"
        class="w-full h-full"
        id="analysisSalaryDegree"
      ></div>
    </div>
    <div class="col-span-2 grid grid-cols-1 gap-10 grid-rows-1 mt-20">
      <div
        v-loading="loading14"
        class="w-full h-full"
        id="analysisSalaryExperience"
      ></div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { getCurrentInstance } from 'vue'
const instance = getCurrentInstance()
const $dayjs = instance?.appContext.config.globalProperties.$dayjs
import { defineAsyncComponent } from 'vue'
import { onMounted } from 'vue'
import * as echarts from 'echarts'
import '../../assets/china'
import {
  getJobDistribution,
  getJobDegree,
  getJobSkills,
  getJobExperience,
  getCompanyFinance,
  getCompanySize,
  getDataCount,
  getCityCount,
  getLatestData,
  getJobSalaryAll,
  getCompanyCount,
  getAnalysisJobkey,
  getSalaryBrand,
  getSalaryByCompanySize,
  getSalaryByDegree,
  getSalaryByExperience,
} from '@/api/boss'
import { getCityPositionByName } from '@/assets/cityPostion.js'
import { ref } from 'vue'
const Map_data = ref()
const Degree_data = ref()
const Skill_data = ref()
const Experience_data = ref()
const Company_finance = ref()
const Company_size = ref()
const Company_count = ref()
const loading = ref(true)
const loading1 = ref(true)
const loading2 = ref(true)
const loading3 = ref(true)
const loading4 = ref(true)
const loading5 = ref(true)
const loading6 = ref(true)
const loading7 = ref(true)
const loading8 = ref(true)
const loading9 = ref(true)
const loading10 = ref(true)
const loading11 = ref(true)
const loading12 = ref(true)
const loading13 = ref(true)
const loading14 = ref(true)
const WordCloud = defineAsyncComponent(
  () => import('@/components/WordCloud.vue'),
)
const dataCount = ref('')
const cityCount = ref('')
const latestData = ref('')
onMounted(async () => {
  await getDataCount().then(res => {
    dataCount.value = res.data.data
    loading5.value = false
    loading6.value = false
  })
  await getCityCount().then(res => {
    cityCount.value = res.data.data
    loading8.value = false
  })
  await getLatestData().then(res => {
    latestData.value = $dayjs(res.data.data + 0).format('YYYY-MM-DD HH:mm:ss')
    loading7.value = false
  })
  await getJobDistribution().then(res => {
    try {
      Map_data.value = res.data.data.map(
        (i: { name: string; value: string }) => {
          const cityPosition = getCityPositionByName(i.name).value
          return {
            name: i.name,
            value: cityPosition.concat(i.value),
            count: i.value,
          }
        },
      )
      initMap()
    } catch (error) {
      console.log(error)
    }
  })
  await getJobDegree().then(res => {
    try {
      Degree_data.value = res.data.data
      initJobDegree()
    } catch (error) {
      console.log(error)
    }
  })
  await getJobSkills().then(res => {
    try {
      Skill_data.value = res.data.data
      // initJobSkills()
    } catch (error) {
      console.log(error)
    }
  })
  await getJobExperience().then(res => {
    try {
      Experience_data.value = res.data.data
      initJobExperience()
    } catch (error) {
      console.log(error)
    }
  })
  await getCompanyFinance().then(res => {
    try {
      Company_finance.value = res.data.data
      initCompanyFinance()
    } catch (error) {
      console.log(error)
    }
  })
  await getCompanySize().then(res => {
    try {
      Company_size.value = res.data.data
      initCompanySize()
    } catch (error) {
      console.log(error)
    }
  })
  await getJobSalaryAll().then(res => {
    try {
      const keys = Object.keys(res.data.data)
      const values: string[] = Object.values(res.data.data)
      initSalary(keys, values)
    } catch (error) {
      console.log(error)
    }
  })
  await getCompanyCount().then(res => {
    Company_count.value = res.data.data
  })
  await getAnalysisJobkey().then(res => {
    const data = res.data.data
    initAnalysisJobKey(data.yAxis,data.series)
  })
  await getSalaryBrand().then(res => {
    const data = res.data.data
    initAnalysisBy('#analysisSalaryBrand',data)
  })

  await getSalaryByCompanySize().then(res => {
    const data = res.data.data
    initAnalysisBy('#analysisSalaryCompanySize',data)
  })
  await getSalaryByDegree().then(res => {
    const data = res.data.data
    initAnalysisBy('#analysisSalaryDegree',data)
  })
  await getSalaryByExperience().then(res => {
    const data = res.data.data
    initAnalysisBy('#analysisSalaryExperience',data)
  })
})
function initMap() {
  const data = Map_data.value
  const initMap = echarts.init(document.querySelector('#map') as HTMLDivElement)
  initMap.setOption({
    backgroundColor: 'transparent', // 设置背景色透明
    // 必须设置
    tooltip: {
      show: false,
    },
    // 地图阴影配置
    geo: {
      map: 'china',
      // 这里必须定义，不然后面series里面不生效
      tooltip: {
        show: false,
      },
      label: {
        show: false,
      },
      // zoom: 1.03,
      silent: true, // 不响应鼠标时间
      show: true,
      roam: false, // 地图缩放和平移
      aspectScale: 0.75, // scale 地图的长宽比
      itemStyle: {
        // borderColor: '#0FA3F0',
        // borderWidth: 1,
        // areaColor: '#070f71',
        // shadowColor: 'rgba(1,34,73,0.48)',
        // shadowBlur: 10,
        // shadowOffsetX: -10,
        // shadowOffsetY: 10,
      },
      select: {
        disabled: true,
      },
      emphasis: {
        disabled: true,
        // areaColor: '#00F1FF',
      },
      // 地图区域的多边形 图形样式 阴影效果
      // z值小的图形会被z值大的图形覆盖
      top: '10%',
      left: 'center',
      // 去除南海诸岛阴影 series map里面没有此属性
      regions: [
        {
          name: '南海诸岛',
          selected: false,
          emphasis: {
            disabled: true,
          },
          itemStyle: {
            // areaColor: '#00000000',
            // borderColor: '#00000000',
          },
        },
      ],
      z: 1,
    },
    series: [
      // 地图配置
      {
        type: 'map',
        map: 'china',
        zoom: 1,
        tooltip: {
          show: false,
        },
        label: {
          show: false, // 显示省份名称
          color: '#ffffff',
          align: 'center',
        },
        top: '10%',
        left: 'center',
        // aspectScale: 0.75,
        roam: false, // 地图缩放和平移
        itemStyle: {
          // borderColor: '#3ad6ff', // 省分界线颜色  阴影效果的
          // borderWidth: 1,
          areaColor: '#ffffff',
          opacity: 1,
        },
        // 去除选中状态
        select: {
          disabled: true,
        },
        // 控制鼠标悬浮上去的效果
        emphasis: {
          // 聚焦后颜色
          disabled: false, // 开启高亮
          label: {
            align: 'center',
            color: '#000000',
          },
          itemStyle: {
            areaColor: '#F40002', // 阴影效果 鼠标移动上去的颜色
          },
        },
        z: 2,
        data: data,
      },
      // {
      //   type: 'scatter',
      //   coordinateSystem: 'geo',
      //   symbol: 'pin',
      //   symbolSize: [50, 50],
      //   label: {
      //     show: true,
      //     color: '#fff',
      //     formatter(value) {
      //       return value.data.value[2]
      //     },
      //   },
      //   itemStyle: {
      //     color: '#e30707', //标志颜色
      //   },
      //   z: 2,
      //   data: data,
      // },
      {
        name: '',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: data, //传入的地图点数据
        symbolSize: 6, //涟漪大小
        showEffectOn: 'render',
        //涟漪效应
        rippleEffect: {
          brushType: 'stroke',
          color: '#F40002',
          period: 10, //周期
          scale: 10, //规模
        },
        hoverAnimation: true, //悬停动画
        //地图点样式
        label: {
          formatter: '{b}',
          position: 'top',
          show: true,
          fontSize: '10',
        },
        itemStyle: {
          color: '#F40002',
          shadowBlur: 2,
          shadowColor: '#333',
        },
        //鼠标点击散点的下弹框
        tooltip: {
          show: true,
          trigger: 'item', // 确保触发方式正确，默认为 'item'
          triggerOn: 'mousemove|click', // 鼠标移入和点击时都触发
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          formatter: (params: { data: any }) => {
            // params 是当前点的数据对象
            const data = params.data // 获取数据
            return `
                <div>
                    <b>${data.name}</b><br>
                    <p>岗位数量: ${data.value[2]} 个</p>
                </div>
            `
          },
        },
      },
    ],
  })
}
function initJobDegree() {
  const initMap = echarts.init(
    document.querySelector('#jobDegree') as HTMLDivElement,
  )
  initMap.setOption({
    title: {
      text: '学历占比图',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      // orient: 'vertical',
      bottom: 'bottom',
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '40%',
        data: Degree_data.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  })
}
// function initJobSkills() {
//   const initMap = echarts.init(document.querySelector('#jobSkill') as HTMLDivElement)
//   initMap.setOption({
//     title: {
//       text: '技能要求占比图',
//       left: 'center',
//     },
//     tooltip: {
//       trigger: 'item',
//     },
//     legend: {
//       // orient: 'vertical',
//       bottom: 'bottom',
//     },
//     series: [
//       {
//         name: '技能要求',
//         type: 'pie',
//         radius: '40%',
//         data: Skill_data.value,
//         emphasis: {
//           itemStyle: {
//             shadowBlur: 10,
//             shadowOffsetX: 0,
//             shadowColor: 'rgba(0, 0, 0, 0.5)',
//           },
//         },
//       },
//     ],
//   })
// }
function initJobExperience() {
  const initMap = echarts.init(
    document.querySelector('#jobExperience') as HTMLDivElement,
  )
  initMap.setOption({
    title: {
      text: '工作经验占比图',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      // orient: 'vertical',
      bottom: 'bottom',
    },
    series: [
      {
        name: '技能要求',
        type: 'pie',
        radius: '40%',
        data: Experience_data.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  })
}
function initCompanyFinance() {
  const initMap = echarts.init(
    document.querySelector('#companyFinance') as HTMLDivElement,
  )
  initMap.setOption({
    title: {
      text: '公司融资占比图',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      // orient: 'vertical',
      bottom: 'bottom',
    },
    series: [
      {
        name: '技能要求',
        type: 'pie',
        radius: '40%',
        data: Company_finance.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  })
}
function initCompanySize() {
  const initMap = echarts.init(
    document.querySelector('#companySize') as HTMLDivElement,
  )
  initMap.setOption({
    title: {
      text: '公司规模占比图',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      // orient: 'vertical',
      bottom: 'bottom',
    },
    series: [
      {
        name: '技能要求',
        type: 'pie',
        radius: '40%',
        data: Company_size.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  })
}
function initSalary(x: string[], y: string[]) {
  const initMap = echarts.init(
    document.querySelector('#salary') as HTMLDivElement,
  )
  initMap.setOption({
    title: {
      text: '薪资分布',
      subtext: '',
      left: 'center',
    },
    xAxis: {
      type: 'category',
      data: x,
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
        data: y,
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
            formatter: '{b} 有 {c} 个', // 标签内容格式
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
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function initAnalysisJobKey(yAxis:any,series:any) {
  const initMap = echarts.init(
    document.querySelector('#analysisJobKey') as HTMLDivElement,
  )
  const option = {
    title: {
      text: '主要行业招聘需求',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    legend: {},
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.001],
    },
    yAxis:{},
    series:{}
  }
  option['yAxis'] = yAxis
  option['series'] = series
  initMap.setOption(option)
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function initAnalysisBy(selector:string,option: any) {
  const initMap = echarts.init(
    document.querySelector(selector) as HTMLDivElement,
  )
  initMap.setOption(option)
}

</script>
<style scoped></style>

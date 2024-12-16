<template>
  <div
    class="grid grid-cols-2 lg:grid-cols-5 pl-5 pr-5 pt-2 overflow-hidden rounded-[3rem] bg-white animate__animated animate__fadeIn"
  >
    <div class="col-span-3">
      <div class="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
        <div
          class="-ml-4 -mt-2 flex flex-wrap items-center justify-between sm:flex-nowrap"
        >
          <div class="ml-4 mt-2">
            <h3 class="text-base font-semibold text-gray-900">数据榜单</h3>
          </div>
          <div class="ml-4 mt-2 flex-shrink-0">
            <select
              class="w-full rounded-md focus-visible:border-none border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-gray-300 sm:text-sm/6"
              v-model="currentSelect"
            >
              <option
                v-for="option in options"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div class="pt-6 grid grid-cols-1">
        <div class="col-span-4 row-span-4 h-[44rem] overflow-scroll pl-5 pr-5">
          <TheRank :rank_type="currentSelect"></TheRank>
        </div>
      </div>
    </div>
    <div
      class="col-span-2 mt-5 ml-12 rounded-[1rem] overflow-scroll bg-white flex justify-center items-center"
    >
      <div
        class="h-full w-full overflow-hidden rounded-[2rem] flex items-center flex-col"
      >
        <div class="pl-5 text-sm w-full text-left text-[#2E335B]">
          收集的网页数量
        </div>
        <div
          class="w-full mt-3 mb-3 pl-5 text-left font-medium text-3xl tracking-tight text-gray-900"
        >
          {{ WebsiteCount }} <span class="text-sm">个</span>
        </div>
        <div class="w-96 h-80">
          <TheTimeCount></TheTimeCount>
        </div>
        <div class="w-96 h-80 mt-3">
          <WordCloud :data="data" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'
import { getWebsiteCount } from '@/api/csdn'
import WordCloud from '@/components/WordCloud.vue'
import TheRank from '@/components/TheRank.vue'
import TheTimeCount from '@/components/TheTimeCount.vue'
import { getWordCloud } from '@/api/csdn'
const WebsiteCount = ref(0)
const interval = ref()
const currentSelect = ref(0)
const data = ref([])
const options = [
  {
    value: 0,
    label: '综合排名',
  },
  {
    value: 1,
    label: '点赞量排名',
  },
  {
    value: 2,
    label: '阅读量排名',
  },
  {
    value: 3,
    label: '收藏量排名',
  },
]
onMounted(() => {
  getWebsiteCount().then(re => {
    WebsiteCount.value = re.data.data
  })
  interval.value = setInterval(() => {
    getWebsiteCount().then(re => {
      WebsiteCount.value = re.data.data
    })
  }, 5000)
  getWordCloud().then(res => {
    data.value = res.data.data
  })
})
onBeforeUnmount(() => {
  clearInterval(interval.value)
})
</script>

<style></style>

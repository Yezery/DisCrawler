<template>
  <div
    class="mx-auto max-w-2xl lg:max-w-7xl p-5 animate__animated animate__fadeIn"
  >
    <di class="w-full flex justify-center items-center">
      <div
        class="pt-10 pb-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 w-4/5 gap-16"
      >
        <div
          class="radial-progress"
          :style="`--size:10rem; --thickness:3px; --value:${_memory_usage}`"
          role="progressbar"
        >
          内存: {{ _memory_usage }}%
        </div>
        <div
          class="radial-progress"
          :style="`--size:10rem; --thickness:3px; --value:${_cpu_usage}`"
          role="progressbar"
        >
          CPU: {{ _cpu_usage }}%
        </div>
        <div
          class="radial-progress"
          :style="`--size:10rem; --thickness:3px; --value:${_disk_usage}`"
          role="progressbar"
        >
          磁盘: {{ _disk_usage }}%
        </div>
      </div>
    </di>
    <div class="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
      <div
        class="-ml-4 -mt-2 flex flex-wrap items-center justify-between sm:flex-nowrap"
      >
        <div class="ml-4 mt-2">
          <h3 class="text-base font-semibold text-gray-900">正在运行的任务</h3>
        </div>
        <div class="ml-4 mt-2 flex-shrink-0">
          <button
            type="button"
            class="rounded-md px-10 py-2 text-sm font-semibold text-white ring-1 bg-black ring-gray-300 hover:bg-gray-70"
            @click="openStartView"
          >
            任务 +
          </button>
        </div>
      </div>
    </div>
    <ul
      v-if="spiders.length > 0"
      role="list"
      class="divide-y divide-white/5 animate__animated animate__fadeIn"
    >
      <li
        v-for="spider in spiders"
        :key="spider.spider_id"
        class="relative flex items-center space-x-4 py-4"
      >
        <div class="min-w-0 flex-auto">
          <div class="flex items-center gap-x-3">
            <div
              :class="[
                spider.status ? statuses['online'] : statuses['error'],
                'flex-none rounded-full p-1',
              ]"
            >
              <div class="h-2 w-2 rounded-full bg-current" />
            </div>
            <h2 class="min-w-0 text-sm/6 font-semibold text-black">
              <div class="flex gap-x-2">
                <span class="truncate">{{ spider.spider_name }}</span>
                <span class="text-gray-400">/</span>
                <span class="whitespace-nowrap">{{ spider.spider_id }}</span>
              </div>
            </h2>
          </div>
          <div class="mt-3 flex items-center gap-x-2.5 text-xs/5 text-gray-400">
            <p class="truncate">{{ spider.description }}</p>
            <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 flex-none fill-gray-300">
              <circle cx="1" cy="1" r="1" />
            </svg>
            <p class="whitespace-nowrap">
              {{ covent_time(spider.start_time) }}
            </p>
          </div>
        </div>
        <button
          type="button"
          class="rounded-md px-10 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-70 cursor-pointer"
          @click="toStopSpider(spider.spider_id)"
        >
          取消任务
        </button>
      </li>
    </ul>
    <div
      v-else
      class="text-center text-gray-900 flex justify-center items-center h-96"
    >
      暂无任务
    </div>
  </div>
  <div
    v-if="showStartView"
    class="absolute top-0 left-0 w-full h-screen bg-gray-300/90 z-50"
  >
    <div
      class="flex justify-center items-center h-full"
      @click.self="showStartView = false"
    >
      <div class="bg-white shadow sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-base font-semibold text-gray-900">选择任务</h3>
          <div
            v-for="supportSpider in supportSpiders"
            :key="supportSpider.spider_name"
            class="mt-5"
          >
            <div
              class="rounded-md bg-gray-50 px-6 py-5 sm:flex sm:items-start sm:justify-between"
            >
              <h4 class="sr-only">{{ supportSpider.spider_name }}</h4>
              <div class="sm:flex sm:items-start">
                <svg
                  class="h-8 w-auto sm:h-6 sm:flex-shrink-0"
                  xmlns="http://www.w3.org/2000/svg"
                  x="0px"
                  y="0px"
                  width="100"
                  height="100"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M6.217 13.408c.447.18 1.379.359 2.132.359.812 0 1.264-.247 1.3-.632.033-.35-.299-.398-1.216-.637-1.267-.342-2.075-.871-1.996-1.717.092-.982 1.286-1.724 3.118-1.724.893 0 1.759.069 2.208.231l-.154 1.238c-.291-.112-1.406-.266-2.16-.266-.765 0-1.16.265-1.188.555-.034.367.363.385 1.356.676 1.345.376 1.933.905 1.856 1.725C11.382 14.18 10.308 15 8.163 15 7.27 15 6.5 14.821 6.076 14.641L6.217 13.408 6.217 13.408zM18.821 9.366c4.884-1.017 5.305.811 5.154 2.428l-.284 2.992h-1.55l.259-2.729c.056-.601.405-1.776-1.281-1.732-.584.016-.873.104-.873.104s-.051.726-.112 1.263l-.294 3.095h-1.52l.302-3.05C18.622 11.736 18.821 9.366 18.821 9.366zM12.653 9.224c.349-.042.884-.084 1.621-.084 1.23 0 2.225.236 2.841.734.553.464.921 1.214.819 2.302-.094 1.012-.57 1.721-1.264 2.159-.635.413-1.434.59-2.637.59-.709 0-1.385-.042-1.9-.126L12.653 9.224 12.653 9.224zM13.669 13.69c.119.025.274.051.582.051 1.231 0 2.098-.668 2.185-1.607.127-1.358-.643-1.832-1.94-1.824-.168 0-.401 0-.525.025L13.669 13.69 13.669 13.69zM5.335 14.813C5.043 14.924 4.439 15 3.595 15c-2.427 0-3.737-1.254-3.583-2.913C.198 10.112 2.139 9 4.264 9c.823 0 1.308.073 1.762.195L5.88 10.526c-.302-.112-1.01-.215-1.583-.215-1.25 0-2.312.41-2.434 1.707-.109 1.16.637 1.714 2.044 1.714.49 0 1.212-.077 1.545-.189C5.452 13.544 5.335 14.813 5.335 14.813z"
                  ></path>
                </svg>
                <div class="mt-3 sm:ml-4 sm:mt-0">
                  <div class="text-sm font-medium text-gray-900">
                    {{ supportSpider.spider_name }}
                  </div>
                  <div
                    class="mt-1 text-sm text-gray-600 sm:flex sm:items-center"
                  >
                    <div>V {{ supportSpider.version }}</div>
                    <span class="hidden sm:mx-2 sm:inline" aria-hidden="true"
                      >&middot;</span
                    >
                    <div class="mt-1 sm:mt-0">
                      {{ supportSpider.description }}
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-4 sm:ml-6 sm:mt-0 sm:flex-shrink-0">
                <button
                  type="button"
                  class="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  @click="toStartSpider(supportSpider.spider_name)"
                >
                  选择
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { covent_time } from '@/utils/convent'
import {
  getSpiderList,
  stopSpider,
  getSpiderSupport,
  startSpider,
} from '@/api/spider'
import { getSystemInfo } from '@/api/system'
import { onBeforeMount, onMounted, onUnmounted, ref, type Ref } from 'vue'
const showStartView = ref(false)
const toStopSpider = (spider_id: string) => {
  stopSpider({ spider_id: spider_id }).then(re => {
    console.log(re.data)
    resfashSpiderList()
  })
}
const statuses: { [key: string]: string } = {
  online: 'text-green-400 bg-green-400/10',
  error: 'text-rose-400 bg-rose-400/10',
}
interface Spider {
  spider_name: string
  spider_id: string
  status: boolean
  start_time: string
  description: string
}
interface SupportSpider {
  spider_name: string
  version: string
  description: string
}
const supportSpiders: Ref<SupportSpider[]> = ref([])
const openStartView = () => {
  getSpiderSupport().then(re => {
    console.log(re.data)
    supportSpiders.value = re.data
  })
  showStartView.value = true
}
const toStartSpider = (spider_name: string) => {
  // SystemInfo()
  // if (Number(_memory_usage.value) > 80) {
  //   return alert('内存使用率过高，请稍后再试')
  // }
  startSpider({ spider_name: spider_name }).then(() => {
    resfashSpiderList()
  })

  showStartView.value = false
}
function resfashSpiderList() {
  getSpiderList().then(re => {
    spiders.value = re.data.spiders
  })
}
const spiders: Ref<Spider[]> = ref([])
const _cpu_usage = ref('0')
const _memory_usage = ref('0')
const _disk_usage = ref('0')
const interval = ref()
onMounted(() => {
  resfashSpiderList()
  SystemInfo()
  interval.value = setInterval(() => {
    SystemInfo()
  }, 10000)
})
onBeforeMount(() => {
  clearInterval(interval.value)
})
onUnmounted(() => {
  clearInterval(interval.value)
})
const SystemInfo = () => {
  getSystemInfo().then(re => {
    const { cpu_usage, memory_usage, disk_usage } = re.data
    _cpu_usage.value = cpu_usage.toString()
    _memory_usage.value = memory_usage.toString()
    _disk_usage.value = disk_usage.toString()
  })
}
</script>

<style></style>

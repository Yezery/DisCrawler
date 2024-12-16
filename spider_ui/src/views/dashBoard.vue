<template>
  <div>
    <div
      class="mx-auto max-w-2xl lg:max-w-7xl p-5 animate__animated animate__fadeIn"
    >
      <div class="w-full flex justify-center items-center">
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
      </div>
      <div class="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
        <div
          class="-ml-4 -mt-2 flex flex-wrap items-center justify-between sm:flex-nowrap"
        >
          <div class="ml-4 mt-2">
            <h3 class="text-base font-semibold text-gray-900">
              正在运行的任务
            </h3>
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
            <div
              class="mt-3 flex items-center gap-x-2.5 text-xs/5 text-gray-400"
            >
              <p class="truncate">{{ spider.description }}</p>
              <svg
                viewBox="0 0 2 2"
                class="h-0.5 w-0.5 flex-none fill-gray-300"
              >
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
      class="absolute top-0 left-0 w-full h-screen bg-gray-300/70 z-50"
    >
      <div
        class="flex justify-center items-center h-full animate__animated animate__fadeIn"
        @click.self="(showStartView = false), (verifyArgsSum = 0)"
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
                  <img
                    class="h-8 w-auto sm:h-6 sm:flex-shrink-0"
                    :src="supportSpider.icon"
                  />
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
                    @click="toStartSpider(supportSpider)"
                  >
                    选择
                  </button>
                </div>
              </div>
              <div
                v-if="startConfirmView"
                class="absolute top-0 left-0 w-full h-screen bg-gray-300/30 z-[51]"
              >
                <div
                  class="flex justify-center items-center h-full animate__animated animate__fadeIn"
                  @click.self="(startConfirmView = false), (verifyArgsSum = 0)"
                >
                  <div class="bg-white shadow sm:rounded-lg">
                    <div class="px-4 py-5 sm:p-6">
                      <h3 class="text-base font-semibold text-gray-900">
                        任务参数
                      </h3>
                      <div
                        v-for="(arg, index) in supportSpider.args"
                        :key="arg"
                        class="mt-5"
                      >
                        <div class="rounded-md bg-gray-50 px-6 py-5">
                          <label
                            for="username"
                            class="block text-sm/6 font-medium text-gray-900"
                            >{{ Object.keys(arg)[0] }}</label
                          >
                          <div class="mt-2">
                            <div
                              class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                            >
                              <input
                                type="text"
                                class="input input-bordered w-full max-w-xs input-md focus:ring-0"
                                v-model="inputValues[Object.values(arg)[0]]"
                                :placeholder="` 参数${index + 1}`"
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="flex justify-center items-center mt-5">
                        <button
                          type="button"
                          class="btn-wide disabled:btn-disabled btn btn-sm bg-black text-white hover:bg-black/70"
                          @click="toConfirmStartSpider(supportSpider)"
                          :disabled="!isFormValid"
                        >
                          开始
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
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
import {
  onBeforeMount,
  onMounted,
  onUnmounted,
  ref,
  watch,
  type Ref,
} from 'vue'
const showStartView = ref(false)
const startConfirmView = ref(false)
const inputValues = ref<Record<string, string>>({})
const toStopSpider = (spider_id: string) => {
  stopSpider({ spider_id: spider_id }).then(() => {
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
  icon: string
  args: string[]
}
const supportSpiders: Ref<SupportSpider[]> = ref([])
const openStartView = () => {
  getSpiderSupport().then(re => {
    supportSpiders.value = re.data
  })
  showStartView.value = true
}
const toStartSpider = (spider: SupportSpider) => {
  // SystemInfo()
  // if (Number(_memory_usage.value) > 80) {
  //   return alert('内存使用率过高，请稍后再试')
  // }
  if (spider.args.length > 0) {
    startConfirmView.value = true
    verifyArgsSum.value = spider.args.length
  } else {
    startSpider({ spider_name: spider.spider_name, spider_args: {},description:spider.description }).then(
      () => {
        resfashSpiderList()
      },
    )
    showStartView.value = false
  }
}
const toConfirmStartSpider = (spider: SupportSpider) => {
  // 遍历 inputValues 检查是否有任何值为空
  for (const key in inputValues.value) {
    if (inputValues.value[key] === '') {
      return
    }
  }
  startSpider({
    spider_name: spider.spider_name,
    spider_args: inputValues.value,
    description: spider.description,
  }).then(() => {
    resfashSpiderList()
    showStartView.value = false
    startConfirmView.value = false
  })
}
function resfashSpiderList() {
  getSpiderList().then(re => {
    spiders.value = re.data.spiders
    for (let index = 0; index < spiders.value.length; index++) {
      if (!spiders.value[index].status) {
        toStopSpider(spiders.value[index].spider_id)
      }
    }
  })
}
const isFormValid = ref(false)
const verifyArgsSum = ref()
watch(
  inputValues,
  n => {
    isFormValid.value =
      Object.keys(n).length === verifyArgsSum.value &&
      Object.values(n).every(value => value !== '')
  },
  {
    deep: true,
  },
)
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
    resfashSpiderList()
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

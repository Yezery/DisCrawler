<template>
  <div class="w-full h-full" v-loading="loading">
    <div
      v-for="(rank, rankIdx) in ranks"
      :key="rankIdx"
      class="overflow-hidden"
    >
      <a
        :href="rank.link"
        target="_blank"
        :class="[
          'mb-5 relative block cursor-pointer rounded-lg border bg-white px-6 py-4 shadow-sm focus:outline-none sm:flex sm:justify-between',
        ]"
      >
        <span class="flex items-center">
          <span class="flex flex-col text-sm">
            <span class="font-medium text-gray-900">{{ rank.title }}</span>
            <span class="text-gray-500 mt-2">
              <span class="block sm:inline text-sm"
                >点赞量 {{ rank.blog_digg_num }}</span
              >
              {{ ' ' }}
              <span class="hidden sm:mx-1 sm:inline text-sm" aria-hidden="true"
                >&middot; 收藏量 {{ rank.collection }}</span
              >
              <span class="hidden sm:mx-1 sm:inline text-sm" aria-hidden="true"
                >&middot; 阅读量 {{ rank.read_count }}</span
              >
              <span class="hidden sm:mx-1 sm:inline text-sm" aria-hidden="true"
                >&middot; 数据更新时间 {{ covent_time(rank.crawl_time) }}</span
              >
              {{ ' ' }}
            </span>
          </span>
        </span>
        <span
          class="mt-2 flex justify-center items-center text-sm sm:ml-4 sm:mt-0 sm:flex-col sm:text-right"
        >
          <span class="font-medium text-gray-900">{{ rankIdx + 1 }}</span>
        </span>
        <span
          :class="['pointer-events-none absolute -inset-px rounded-lg']"
          aria-hidden="true"
        />
      </a>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { covent_time } from '@/utils/convent'
import {
  getRanked,
  getCollectCount,
  getReadCount,
  getBlogDiggNum,
} from '@/api/csdn'
import { ref, toRefs, watch } from 'vue'
const loading = ref(false)
const props = defineProps({
  rank_type: {
    type: Number,
    default: 0,
  },
})
const { rank_type } = toRefs(props)
const ranks = ref()

watch(
  rank_type,
  n => {
    loading.value = true
    switch (n) {
      case 0:
        getRanked().then(re => {
          ranks.value = re.data.data
          loading.value = false
        })
        break
      case 1:
        getBlogDiggNum().then(re => {
          ranks.value = re.data.data
          loading.value = false
        })
        break
      case 2:
        getReadCount().then(re => {
          ranks.value = re.data.data
          loading.value = false
        })
        break
      case 3:
        getCollectCount().then(re => {
          ranks.value = re.data.data
          loading.value = false
        })
        break

      default:
        break
    }
  },
  {
    immediate: true,
  },
)
</script>

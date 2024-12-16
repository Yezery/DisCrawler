<template>
  <TransitionRoot :show="_open" as="template" @after-leave="query = ''" appear>
    <Dialog class="relative z-10" @close="close">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-25 transition-opacity"
        />
      </TransitionChild>

      <div
        class="fixed inset-0 z-10 w-screen overflow-y-auto p-36 sm:p-36 md:p-36"
      >
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <DialogPanel
            class="mx-auto max-w-3xl transform divide-y divide-gray-100 overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 transition-all"
          >
            <Combobox v-slot="{ activeOption }">
              <div class="relative">
                <MagnifyingGlassIcon
                  class="pointer-events-none absolute left-4 top-3.5 h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
                <ComboboxInput
                  class="h-12 w-full border-0 bg-transparent pl-11 pr-4 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                  placeholder="搜索网站..."
                  @change="query = $event.target.value"
                  @blur="query = ''"
                />
              </div>

              <ComboboxOptions
                v-if="query === '' || results.length > 0"
                class="flex transform-gpu divide-x divide-gray-100"
                as="div"
                static
                hold
              >
                <div
                  v-if="query !== ''"
                  :class="[
                    'max-h-96 min-w-0 flex-auto scroll-py-4 overflow-y-auto px-6 py-4',
                    activeOption && 'sm:h-96',
                  ]"
                >
                  <h2 class="mb-4 mt-2 text-xs font-semibold text-gray-500">
                    当前搜索结果
                  </h2>
                  <div hold class="-mx-2 text-sm text-gray-700">
                    <ComboboxOption
                      v-for="result in results"
                      :key="result.link"
                      :value="result"
                      as="template"
                      v-slot="{ active }"
                    >
                      <div
                        :class="[
                          'group flex cursor-default select-none items-center rounded-md p-2',
                          active && 'bg-gray-100 text-gray-900 outline-none',
                        ]"
                      >
                        <span class="ml-3 flex-auto truncate">{{
                          result.title
                        }}</span>
                      </div>
                    </ComboboxOption>
                  </div>
                </div>

                <div
                  v-if="activeOption"
                  class="hidden h-96 w-1/2 flex-none flex-col divide-y divide-gray-100 overflow-y-auto sm:flex"
                >
                  <div class="flex-none p-6 text-center">
                    <!-- <img
                      :src="activeOption.imageUrl"
                      alt=""
                      class="mx-auto h-16 w-16 rounded-full"
                    /> -->
                    <h2 class="mt-3 font-semibold text-gray-900">
                      {{ activeOption.title }}
                    </h2>
                    <p class="text-sm/6 text-gray-500">
                      {{ covent_time(activeOption.create_time) }}
                    </p>
                  </div>
                  <div class="flex flex-auto flex-col justify-between p-6">
                    <dl
                      class="grid grid-cols-1 gap-x-6 gap-y-3 text-sm text-gray-700"
                    >
                      <dt class="col-end-1 font-semibold text-gray-900">
                        点赞
                      </dt>
                      <dd>{{ activeOption.blog_digg_num }}</dd>
                      <dt class="col-end-1 font-semibold text-gray-900">
                        收藏
                      </dt>
                      <dd>{{ activeOption.collection }}</dd>
                      <dt class="col-end-1 font-semibold text-gray-900">
                        观看
                      </dt>
                      <dd class="truncate">
                        {{ activeOption.read_count }}
                      </dd>

                      <dt class="col-end-1 font-semibold text-gray-900">
                        链接
                      </dt>
                      <dd class="truncate">
                        <a
                          :target="'_blank'"
                          :href="activeOption.link"
                          class="text-indigo-600 underline"
                        >
                          {{ activeOption.link }}
                        </a>
                      </dd>
                    </dl>
                  </div>
                </div>
              </ComboboxOptions>

              <div
                v-if="query !== '' && results.length === 0"
                class="px-6 py-14 text-center text-sm sm:px-14"
              >
                <p class="mt-4 font-semibold text-gray-900">无数据</p>
                <p class="mt-2 text-gray-500">请更换关键词,再重试.</p>
              </div>
            </Combobox>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script lang="ts" setup>
import { searchAPI } from '../../api/test'
import { ref, toRefs, watch, type Ref } from 'vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/20/solid'
import { covent_time } from '@/utils/convent'
import {
  Combobox,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption,
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
const props = defineProps({
  _open: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['update:_open'])
function close() {
  emit('update:_open', false)
}
const { _open } = toRefs(props)
const timer = ref(0)
const query = ref('')
interface Result {
  link: string
  title: string
  read_count: number
  collection: number
  blog_digg_num: number
  crawl_time: string
  create_time: string
}
const results: Ref<Result[]> = ref([])
watch(query, n => {
  results.value = []
  if (n != '') {
    clearTimeout(timer.value)
    timer.value = setTimeout(() => {
      // #函数防抖
      searchAPI({ query: n }).then(res => {
        results.value = res.data.data
      })
    }, 200)
  }
})
</script>

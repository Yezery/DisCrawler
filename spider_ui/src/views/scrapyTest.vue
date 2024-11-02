<template>
  <div
    class="mx-auto max-w-2xl px-4 py-8 sm:px-6 sm:py-16 lg:max-w-7xl lg:px-8 animate__animated animate__fadeIn"
  >
    <div class="flex items-center justify-between space-x-4">
      <h2 class="text-lg font-medium text-gray-900">测试用例</h2>
    </div>
    <ul
      role="list"
      class="grid mt-10 grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8"
    >
      <li
        v-for="test in tests"
        :key="test.id"
        class="overflow-hidden rounded-xl border border-gray-200"
      >
        <div
          class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6"
        >
          <img
            :src="test.imageUrl"
            :alt="test.name"
            class="h-12 w-12 flex-none rounded-lg bg-white object-cover ring-1 ring-gray-900/10"
          />
          <div class="text-sm/6 font-medium text-gray-900">
            {{ test.name }}
          </div>
          <Menu as="div" class="relative ml-auto">
            <MenuButton
              class="-m-2.5 block p-2.5 text-gray-400 hover:text-gray-500"
            >
              <span class="sr-only">打开选项</span>
              <EllipsisHorizontalIcon class="h-5 w-5" aria-hidden="true" />
            </MenuButton>
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems
                class="absolute right-0 z-10 mt-0.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none"
              >
                <MenuItem v-slot="{ active }">
                  <div
                    @click="open"
                    v-if="test.testInf.status === 'open'"
                    :class="[
                      active ? 'bg-gray-50' : '',
                      'block px-3 py-1 text-sm/6 text-gray-900 text-center',
                    ]"
                  >
                    测试
                  </div>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>
        <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm/6">
          <div class="flex justify-between gap-x-4 py-3">
            <dt class="text-gray-500">用例名称</dt>
            <dd class="text-gray-700">
              {{ test.testInf.type }}
            </dd>
          </div>
          <div class="flex justify-between gap-x-4 py-3">
            <dt class="text-gray-500">状态</dt>
            <dd class="flex items-start gap-x-2">
              <div
                :class="[
                  statuses[test.testInf.status],
                  'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset',
                ]"
              >
                {{ test.testInf.status }}
              </div>
            </dd>
          </div>
        </dl>
      </li>
    </ul>
  </div>
  <TheSearchTest :_open="toOpen" @update:_open="close" />
</template>

<script lang="ts" setup>
import TheSearchTest from '@/components/test/TheSearchTest.vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'
import { ref } from 'vue'
const statuses: { [key: string]: string } = {
  open: 'text-green-700 bg-green-50 ring-green-600/20',
  close: 'text-red-700 bg-red-50 ring-red-600/10',
}
const toOpen = ref(false)
const open = () => {
  toOpen.value = true
}
const close = (value: boolean) => {
  toOpen.value = value
}
const tests = [
  {
    id: 1,
    name: '搜索栏',
    imageUrl:
      'https://img.icons8.com/?size=1000&id=HWlRx_egk4PX&format=png&color=000000',
    testInf: {
      type: '搜索引擎爬虫',
      status: 'open',
    },
  },
]
</script>

<style></style>

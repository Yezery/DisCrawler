<template>
  <div
    class="mx-auto max-w-2xl px-4 py-8 sm:px-6 sm:py-16 lg:max-w-7xl lg:px-8 animate__animated animate__fadeIn"
  >
    <div class="flex items-center justify-between space-x-4">
      <h2 class="text-lg font-medium text-gray-900">应用</h2>
    </div>
    <ul
      role="list"
      class="grid mt-10 grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8"
    >
      <li
        v-for="application in applications"
        :key="application.id"
        class="overflow-hidden rounded-xl border border-gray-200"
      >
        <div
          class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6"
        >
          <img
            :src="application.imageUrl"
            :alt="application.name"
            class="h-12 w-12 flex-none rounded-lg bg-white object-cover ring-1 ring-gray-900/10"
          />
          <div class="text-sm/6 font-medium text-gray-900">
            {{ application.name }}
          </div>
          <Menu
            as="div"
            v-if="application.applicationInf.status === 'open'"
            class="relative ml-auto"
          >
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
                    @click="open(application.componentName)"
                    :class="[
                      active ? 'bg-gray-50' : '',
                      'block px-3 py-1 text-sm/6 text-gray-900 text-center',
                    ]"
                  >
                    查看
                  </div>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>
        <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm/6">
          <div class="flex justify-between gap-x-4 py-3">
            <dt class="text-gray-500">应用描述</dt>
            <dd class="text-gray-700">
              {{ application.applicationInf.description }}
            </dd>
          </div>
          <div class="flex justify-between gap-x-4 py-3">
            <dt class="text-gray-500">状态</dt>
            <dd class="flex items-start gap-x-2">
              <div
                :class="[
                  statuses[application.applicationInf.status],
                  'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset',
                ]"
              >
                {{ application.applicationInf.status }}
              </div>
            </dd>
          </div>
        </dl>
      </li>
    </ul>
  </div>
  <component
    :is="currentComponent"
    v-bind="currentSelectProps"
    v-on="currentSelectEvents"
  ></component>
</template>

<script lang="ts" setup>
import csdnSearch from '@/components/application/csdnSearch.vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'
import { ref } from 'vue'
const statuses: { [key: string]: string } = {
  open: 'text-green-700 bg-green-50 ring-green-600/20',
  close: 'text-red-700 bg-red-50 ring-red-600/10',
}
const toOpen = ref(false)
const open = (component_name: string) => {
  currentComponent.value = component_name
  toOpen.value = true
}
const close = (value: boolean) => {
  toOpen.value = value
}
const applications = [
  {
    id: 1,
    name: '深度搜索',
    componentName: 'csdnSearch',
    imageUrl:
      'https://img.icons8.com/?size=1000&id=HWlRx_egk4PX&format=png&color=000000',
    applicationInf: {
      description: '深度查询 CSDN 文章内容信息',
      status: 'open',
    },
  },
  {
    id: 1,
    name: '职位方圆搜索',
    componentName: 'csdnSearch',
    imageUrl:
      'https://ts1.cn.mm.bing.net/th/id/R-C.7cb4bb3fc18ef32ab594c14eb070a54e?rik=cm2qfVwyVcwEZA&riu=http%3a%2f%2fwww.kuaipng.com%2fUploads%2fpic%2fw%2f2021%2f11-15%2f112916%2fwater_112916_698_698_.png&ehk=JtG6sCVyeVJSwlPY5c%2bAXLxOl%2fdwkxHlugBejEXX%2fqU%3d&risl=&pid=ImgRaw&r=0',
    applicationInf: {
      description: '根据用户输入的求职地点进行方圆搜索',
      status: 'close',
    },
  },
  {
    id: 1,
    name: '最佳岗位匹配',
    componentName: 'csdnSearch',
    imageUrl:
      'https://ts1.cn.mm.bing.net/th/id/R-C.7cb4bb3fc18ef32ab594c14eb070a54e?rik=cm2qfVwyVcwEZA&riu=http%3a%2f%2fwww.kuaipng.com%2fUploads%2fpic%2fw%2f2021%2f11-15%2f112916%2fwater_112916_698_698_.png&ehk=JtG6sCVyeVJSwlPY5c%2bAXLxOl%2fdwkxHlugBejEXX%2fqU%3d&risl=&pid=ImgRaw&r=0',
    applicationInf: {
      description: '根据用户情况进行最佳岗位匹配',
      status: 'close',
    },
  },
]

const currentComponent = ref()
const currentSelectProps = ref({
  _open: toOpen,
  /* 其他 props */
})
const currentSelectEvents = ref({
  'update:_open': close,
  /* 可以继续添加其他事件 */
})
defineOptions({
  components: {
    csdnSearch,
  },
})
</script>

<style></style>

<template>
  <div
    class="mt-5 flex justify-center items-center animate__animated animate__fadeIn"
  >
    <div class="w-[95%] rounded-lg sm:grid sm:grid-cols-2 sm:gap-5">
      <div
        v-for="(action, actionIdx) in actions"
        :key="action.title"
        :class="[
          actionIdx === 0
            ? 'rounded-tl-lg rounded-tr-lg sm:rounded-tr-none'
            : '',
          actionIdx === 1 ? 'sm:rounded-tr-lg' : '',
          actionIdx === actions.length - 2 ? 'sm:rounded-bl-lg' : '',
          actionIdx === actions.length - 1
            ? 'rounded-bl-lg rounded-br-lg sm:rounded-bl-none'
            : '',
          'group mt-3 relative bg-white p-6 border border-gray-200',
        ]"
      >
        <div>
          <span
            :class="[
              action.iconBackground,
              action.iconForeground,
              'inline-flex rounded-lg p-3 ring-4 ring-white',
            ]"
          >
            <component :is="action.icon" class="h-6 w-6" aria-hidden="true" />
          </span>
        </div>
        <div class="mt-8">
          <h3 class="text-base font-semibold text-gray-900">
            <RouterLink :to="action.href" class="focus:outline-none">
              <!-- Extend touch target to entire panel -->
              <span class="absolute inset-0" aria-hidden="true" />
              {{ action.title }}
            </RouterLink>
          </h3>
          <p class="mt-2 text-sm text-gray-500">
            {{ action.description }}
          </p>
        </div>
        <span
          class="pointer-events-none absolute right-6 top-6 text-gray-300 group-hover:text-gray-400"
          aria-hidden="true"
        >
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
            <path
              d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z"
            />
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  ChartPieIcon,
  ClipboardDocumentCheckIcon,
} from '@heroicons/vue/24/outline'
const actions = [
  {
    title: 'CSDN 数据',
    href: '/home/csdnData',
    icon: ClipboardDocumentCheckIcon,
    iconForeground: 'text-white',
    iconBackground: 'bg-orange-500',
    description: 'CSDN 推荐文章数据统计分析',
  },
  {
    title: 'BOSS直聘 数据',
    href: '/home/bossData',
    icon: ChartPieIcon,
    iconForeground: 'text-white',
    iconBackground: 'bg-teal-300',
    description: 'BOSS直聘 岗位数据统计分析',
  },
]
</script>

<style></style>

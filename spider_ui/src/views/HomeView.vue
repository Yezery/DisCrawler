<script setup lang="ts">
import { ref, watch, type Ref } from 'vue'
import { useRoute } from 'vue-router'
import { upperCase } from 'lodash'

const route = useRoute()
interface Tab {
  name: string
  href: string
}
const tabs: Ref<Tab[]> = ref([])
watch(
  route,
  () => {
    const routerList = route.fullPath.split('/')
    routerList.shift()
    tabs.value = routerList.map((item, index) => {
      return {
        name: item,
        href: '/' + routerList.slice(0, index + 1).join('/'),
      }
    })
  },
  {
    immediate: true,
  },
)
</script>

<template>
  <div class="mx-auto max-w-2xl lg:max-w-7xl animate__animated animate__fadeIn">
    <div class="flex p-px lg:col-span-4 justify-center items-center">
      <div class="w-full h-full">
        <div class="breadcrumbs text-sm mt-5 ml-10 mb-5">
          <ul>
            <li v-for="tab in tabs" :key="tab.href">
              <RouterLink :to="tab.href">{{ upperCase(tab.name) }}</RouterLink>
            </li>
          </ul>
        </div>
        <RouterView></RouterView>
      </div>
    </div>
  </div>
</template>
<style scoped></style>

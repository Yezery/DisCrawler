<template>
  <TheNav></TheNav>
  <main class="lg:pl-60">
    <RouterView></RouterView>
  </main>
</template>

<script lang="ts" setup>
import TheNav from './components/TheNav.vue'
</script>

<script setup>
import { /*RouterLink,*/ RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
import Layout from './components/layouts/Layout.vue'
</script>

<template>
  <Layout/>
  <!-- <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav class="text-green-600">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header> -->


</template>

<style scoped>
@import "flowbite/src/themes/default";
@plugin "flowbite/plugin";
@source "../node_modules/flowbite";
</style>

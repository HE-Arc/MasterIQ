<script setup>
import { RouterLink } from 'vue-router'
import IconLogo from '@/components/icons/IconLogo.vue'

const props = defineProps({
  isConnected: Boolean
})

</script>

<template>
  <header>
    <div class="header-wrapper container">
      <RouterLink id="main-title" to="/"><IconLogo class="header-logo"/></RouterLink>
      <nav>
        <RouterLink to="/categories" v-show="isConnected">Categories</RouterLink>
        <RouterLink to="/add-question" v-show="isConnected">Add question</RouterLink>
        <RouterLink to="/login" v-show="!isConnected">Login</RouterLink>
        <RouterLink to="/logout" v-show="isConnected">Logout</RouterLink>
        <RouterLink to="/register" v-show="!isConnected">Register</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped style="scss">
header {
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.25);
  line-height: 1.5;
  min-height: 10vh;
}

.header-logo {
  width: 50px;
  height: 50px;
}

.header-wrapper {
  display: flex;
  flex-direction: column;
  padding: 1.3rem 0;
  height: 100%;
}

#main-title {
  font-family: 'Bevan', cursive;
  font-style: italic;
  color: var(--color-heading);
  font-size: 2.2rem;
  text-align: center;
  margin-bottom: .5rem;

  &:hover {
    text-decoration: none;
    cursor: pointer;
  }
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;

  a {
    display: inline-block;
    padding: 1rem;
    font-size: .75rem;

    &.router-link-exact-active {
      transform: scale(1.1);
      font-weight: bold;
    }
  }
}

@media (min-width: 481px) {
  #main-title
  {
    margin-bottom: 0;
    line-height: 0;
  }
  .header-wrapper {
    flex-direction: row;
    padding: 1rem;
  }
  header {
    nav
    {
      justify-content: flex-end;
      margin-top: 0;
      padding: 0;
      text-align: right;
      a
      {
        font-size: .9rem;
      }
    }
  }
  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>
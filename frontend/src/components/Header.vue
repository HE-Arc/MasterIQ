<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <RouterLink id="main-title" to="/">MasterIQ</RouterLink>
      <nav>
        <RouterLink to="/">Categories</RouterLink>
        <RouterLink to="/add-question">Add question</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/logout">Logout</RouterLink>
        <RouterLink to="/signup">SignUp</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped style="scss">
header {
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.25);
  line-height: 1.5;
}

.wrapper
{
  display: flex;
  flex-direction: column;
  padding: 1.3rem 0;
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

@media (min-width: 1024px) {
  #main-title
  {
    margin-bottom: 0;
  }
  .wrapper {
    flex-direction: row;
    max-width: 1100px;
    margin: 0 auto;
    padding: 1rem;
  }
  header {
    nav
    {
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
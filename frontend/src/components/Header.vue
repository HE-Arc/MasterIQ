<script setup>
import { RouterLink } from 'vue-router'
import { ref, computed } from 'vue';
import APIClient from '@/api_client.js';

const isLoggedIn = ref(false);

const checkLoggedIn = async () => {
    try {
        const response = await APIClient.checkUserLoggedIn();
        isLoggedIn.value = response.isLoggedIn;
    } catch (error) {
        console.error('Error checking user login status:', error);
    }
};

checkLoggedIn();
</script>

<template>
  <header>
    <div class="wrapper">
      <RouterLink id="main-title" to="/">MasterIQ</RouterLink>
      <nav>
        <RouterLink to="/">Categories</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/login">Login</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/register">Register</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/add-question">Add question</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/logout">Logout</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script>
import { onUnmounted } from 'vue';

export default {
    setup() {
        const isLoggedIn = ref(false);

        const checkLoggedIn = async () => {
            try {
                const response = await APIClient.checkUserLoggedIn();
                isLoggedIn.value = response.isLoggedIn;
            } catch (error) {
                console.error('Error checking user login status:', error);
            }
        };

        const handleLogout = async () => {
            try {
                await APIClient.logoutUser();
                isLoggedIn.value = false;
            } catch (error) {
                console.error('Error logging out:', error);
            }
        };

        checkLoggedIn();

        onUnmounted(() => {
            // Clean-up actions if needed
        });

        return {
            isLoggedIn,
            handleLogout
        };
    }
};
</script>

<style scoped style="scss">
header {
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.25);
  line-height: 1.5;
}

.wrapper {
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
  #main-title {
    margin-bottom: 0;
  }
  .wrapper {
    flex-direction: row;
    max-width: 1100px;
    margin: 0 auto;
    padding: 1rem;
  }
  header {
    nav {
      margin-top: 0;
      padding: 0;
      text-align: right;
      a {
        font-size: .9rem;
      }
    }
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>

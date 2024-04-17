<template>
    <section class="not-found container form-wrapper">
        <div>
            <p class="info box">What HTTP status code indicates that the requested resource was not found on the server?</p>
            <h1 class="title box">404 Not Found</h1>
            <div class="button-wrapper">
                <router-link to="/" class="btn">Go to Main Page</router-link>
            </div>
        </div>
    </section>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 80vh;
}

.title, .info {
    text-align: center;
}

@media (min-width: 576px) {
    .form-wrapper {
        max-width: 90%;
    }
}

@media (min-width: 1024px) {
    .form-wrapper {
        max-width: 70%;
    }
}
</style>

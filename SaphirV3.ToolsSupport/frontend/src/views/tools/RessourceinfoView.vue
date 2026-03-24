<script>
export default {

}
</script>

<template>
  <div class="w-full p-4  bg-gray-200">
    <div
      class="w-[100%] p-4 mt-5 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-8 dark:bg-gray-800 dark:border-gray-700">
      <h5 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">
        Environnements et tests à choisir
      </h5>
      <br>
      <form class="max-w-sm mx-auto">


        <div class="grid grid-cols-2 md:grid-cols-6">
          <label for="organisations" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Sélectionner une
          organisation</label>
        <select id="organisations" v-model="selectedOrganisation" @change="onOrganisationChange"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <option value="">Sélectionner une organisation</option>

          <option v-for="organisation in organisations" :key="organisation.OrganisationId"
            :value="organisation.OrganisationId">
            {{ organisation.Nom }}
          </option>
        </select>
        </div>
      </form>
    </div>

  </div>

</template>
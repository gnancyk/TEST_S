<script>
import { RouterLink, RouterView } from 'vue-router'

</script>
<template>
  <div class="w-full p-4 flex items-stretch">
    <div
      class="max-w-sm p-6 m-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">


      <h5 class="mb-2 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white"><i
          class="fa-solid fa-sliders text-3xl"></i> &nbsp; Checklist</h5>

      <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">
        L'outil <strong>Checklist</strong> vérifie des configurations.
        <br>
        La configuration des environnements optimise les performances, assure la sécurité, facilite le déploiement et
        garantit une gestion efficace des ressources."
      </p>
      <RouterLink to="/tools/checklist">
        <a href="#" class="inline-flex font-medium items-center text-blue-600 hover:underline">
          Accèder à l'outil
          <svg class="w-3 h-3 ms-2.5 rtl:rotate-[270deg]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 18 18">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11v4.833A1.166 1.166 0 0 1 13.833 17H2.167A1.167 1.167 0 0 1 1 15.833V4.167A1.166 1.166 0 0 1 2.167 3h4.618m4.447-2H17v5.768M9.111 8.889l7.778-7.778" />
          </svg>
        </a>
      </RouterLink>
    </div>
    <!-- <div
      class="max-w-sm p-6 m-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">


      <h5 class="mb-2 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white">
        <i
          class="fa fa-info text-3xl"></i> &nbsp; Ressource info</h5>

      <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">
        L'outil <strong>Ressource Info</strong> permet d'avoir des informations sur les ressources d'un environnement.
        Les informations récupérées sont la dernière modification, l'auteur de la modification, ...
      </p>
      <RouterLink to="/tools/ressource-info">
        <a href="#" class="inline-flex font-medium items-center text-blue-600 hover:underline">
          Accèder à l'outil
          <svg class="w-3 h-3 ms-2.5 rtl:rotate-[270deg]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 18 18">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11v4.833A1.166 1.166 0 0 1 13.833 17H2.167A1.167 1.167 0 0 1 1 15.833V4.167A1.166 1.166 0 0 1 2.167 3h4.618m4.447-2H17v5.768M9.111 8.889l7.778-7.778" />
          </svg>
        </a>
      </RouterLink>

    </div> -->
    <!-- <div
      class="max-w-sm p-6 m-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">


      <h5 class="mb-2 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white"><i
          class="fa-solid fa-sliders text-3xl"></i> &nbsp; Sous gride editable</h5>

      <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">
        L'outil <strong>Sous gride editable</strong> permet de faire la migration des sous grides ainsi que les champs associés à ces sous grides.
        Il suffit de faire la configuratin des environnements et lancer l'outil pour faire la migration
      </p>
      <RouterLink to="/tools/sous-grid">
        <a href="#" class="inline-flex font-medium items-center text-blue-600 hover:underline">
          Accèder à l'outil
          <svg class="w-3 h-3 ms-2.5 rtl:rotate-[270deg]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 18 18">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11v4.833A1.166 1.166 0 0 1 13.833 17H2.167A1.167 1.167 0 0 1 1 15.833V4.167A1.166 1.166 0 0 1 2.167 3h4.618m4.447-2H17v5.768M9.111 8.889l7.778-7.778" />
          </svg>
        </a>
      </RouterLink>

    </div> -->

    <!-- <div
      class="max-w-sm p-6 m-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">


      <h6 class="mb-2 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white"><i
          class="fa-solid fa-sliders text-3xl"></i> &nbsp; Migration de données</h6>

      <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">
        L'outil <strong>Migration de données</strong> permet de faire la migration des données sur une table précise tout en faisant un différentiel des donnés.
        <br>
        <br>
      </p>
      <RouterLink to="/tools/checklist">
        <a href="#" class="inline-flex font-medium items-center text-blue-600 hover:underline">
          Accèder à l'outil
          <svg class="w-3 h-3 ms-2.5 rtl:rotate-[270deg]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 18 18">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11v4.833A1.166 1.166 0 0 1 13.833 17H2.167A1.167 1.167 0 0 1 1 15.833V4.167A1.166 1.166 0 0 1 2.167 3h4.618m4.447-2H17v5.768M9.111 8.889l7.778-7.778" />
          </svg>
        </a>
      </RouterLink>

    </div> -->
    <!--
    <div
      class="max-w-sm p-6 m-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
      <i class="fa fa-loader"></i>
      <a href="#">
        <h5 class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Need a help in Claim?</h5>
      </a>
      <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">Go to this step by step guideline process on how to
        certify for your weekly benefits:</p>
      <a href="#" class="inline-flex font-medium items-center text-blue-600 hover:underline">
        See our guideline
        <svg class="w-3 h-3 ms-2.5 rtl:rotate-[270deg]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
          fill="none" viewBox="0 0 18 18">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15 11v4.833A1.166 1.166 0 0 1 13.833 17H2.167A1.167 1.167 0 0 1 1 15.833V4.167A1.166 1.166 0 0 1 2.167 3h4.618m4.447-2H17v5.768M9.111 8.889l7.778-7.778" />
        </svg>
      </a>
    </div> -->


  </div>
</template>
<style></style>

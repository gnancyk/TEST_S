<script>

export default {

  data() {
    return {
      show_result: false,
      organisations: [], // La liste des organisations
      organisation: '', // La liste des organisations
      selectedOrganisation: '', // L'organisation sélectionnée
      parametres: {},
      catalogues: {},
      result_section: false,
      result_section_disponibilite_serveur: false,
      result_section_verification_crm: false,
      result_section_verification_bd: false,
      result_section_historique: false,
      result_section_recuperation_catalogues: false,
      result_section_verification_catalogues: false,
      section_verification_fontion_generale: false,
      result_section_verification_fontion_generale: '',
      result_ps_function_par_catalogues: [],
      nombre_serveur: '',
      disponibilite_instance_bd: '',
      disponibilite_crm: '',
      mscrmPattern: '_mscrm',
      catalogues_mscrm: {},
      check_organisationId: '',
      catalogues_function: 0,
      catalogues_ps: 0,
      serveurs: {
        frontend: { etat: '', os_name: '', os_version: '' },
        backend: { etat: '', os_name: '', os_version: '' },
        bd: { etat: '', os_name: '', os_version: '' },
        batch: { etat: '', os_name: '', os_version: '' },
        report: { etat: '', os_name: '', os_version: '' },
        caisse: { etat: '', os_name: '', os_version: '' },
      },
      check_param: { etape: 0, status: false, message: '' },
      check_server: { etape: 0, status: false, message: '' },
      check_instance_bd: { etape: 0, status: false, message: '' },
      check_crm: { etape: 0, status: false, message: '' },
      check_catalogue: { etape: 0, status: false, message: '' },
      check_fonction_generale: { etape: 0, status: false, message: '' },
      check_organizationID: { etape: 0, status: false, message: '' },
      check_ps_funtion: { etape: 0, status: false, message: '' },
      check_service_windows: { etape: 0, status: false, message: '' },

    };
  },
  mounted() {
    this.getOrganisations(); // Charger les organisations dès que le composant est monté
  },
  // watch: {
  //   selectedOrganisation(OrganisationId) {
  //     if (OrganisationId) {
  //       this.fetchOrganisationDetails(OrganisationId); // Si une organisation est sélectionnée, appeler l'API
  //     }
  //   },
  // },
  methods: {

    async getOrganisations() {
      try {
        const response = await fetch('http://127.0.0.1:5000/organisations');
        const data = await response.json();
        this.organisations = data.response; // Assurez-vous que 'response' contient les organisations


      } catch (error) {
        console.error("Erreur lors de l'appel API", error);
      }
    },


    onOrganisationChange() {
      // this.startChrono();
      // this.result_section = false;
      // this.result_section_disponibilite_serveur = false;
      // this.nombre_serveur = '';
      // this.disponibilite_instance_bd = '';
      // this.catalogues = {};
      // this.disponibilite_crm = '';
      // this.selectedOrganisation = ''; // L'organisation sélectionnée
      this.show_result = false;
      this.parametres = {};
      this.catalogues = {};
      this.organisation = '';
      this.result_section = false;
      this.catalogues_ps = 0;
      this.catalogues_function = 0;
      this.result_section_disponibilite_serveur = false;
      this.result_section_verification_crm = false;
      this.result_section_verification_bd = false;
      this.result_section_historique = false;
      this.result_section_recuperation_catalogues = false;
      this.result_section_verification_catalogues = false;
      this.section_verification_fontion_generale = false;
      this.result_section_verification_fontion_generale = '';
      this.result_ps_function_par_catalogues = [];
      this.nombre_serveur = '';
      this.disponibilite_instance_bd = '';
      this.disponibilite_crm = '';
      this.check_organisationId = '';
      this.mscrmPattern = '_mscrm';
      this.catalogues_mscrm = {};

      this.serveurs = {
        frontend: { etat: '', os_name: '', os_version: '' },
        backend: { etat: '', os_name: '', os_version: '' },
        bd: { etat: '', os_name: '', os_version: '' },
        batch: { etat: '', os_name: '', os_version: '' },
        report: { etat: '', os_name: '', os_version: '' },
        caisse: { etat: '', os_name: '', os_version: '' },
      };

      this.check_param = { etape: 0, status: false, message: '' };
      this.check_server = { etape: 0, status: false, message: '' };
      this.check_instance_bd = { etape: 0, status: false, message: '' };
      this.check_crm = { etape: 0, status: false, message: '' };
      this.check_catalogue = { etape: 0, status: false, message: '' };
      this.check_fonction_generale = { etape: 0, status: false, message: '' };
      this.check_organizationID = { etape: 0, status: false, message: '' };
      this.check_ps_funtion = { etape: 0, status: false, message: '' };
      this.check_service_windows = { etape: 0, status: false, message: '' };


      if (this.selectedOrganisation) {
        this.fetchOrganisationDetails(this.selectedOrganisation);
      }
    },

    async fetchOrganisationDetails(organisationId) {
      try {
        this.check_param.etape = 1;
        this.check_param.status = false;
        const response = await fetch(`http://127.0.0.1:5000/organisation/${organisationId}`);
        const data = await response.json();
        this.parametres = data.response.parametres[0]
        this.result_section = true;
        console.log(data);

        this.check_param.etape = 2;
        this.check_param.status = true;
        console.log(this.check_param);

        this.organisation = data.response.organisation[0]
        console.log(this.parametres);


        this.check_server.etape = 1; // { etape: 0, status: false, message: '' };
        this.check_server.status = false; // { etape: 0, status: false, message: '' };

        const liste_serveur = await fetch(`http://127.0.0.1:5000/organisation/${organisationId}/verification/serveur`);
        const res = await liste_serveur.json();



        // console.log(res);
        this.serveurs.frontend.etat = res.response.find(item => item.role == "serveur_crm").etat;
        this.serveurs.frontend.os_name = res.response.find(item => item.role == "serveur_crm").os_name;
        this.serveurs.frontend.os_version = res.response.find(item => item.role == "serveur_crm").os_version;

        this.serveurs.backend.etat = res.response.find(item => item.role == "serveur_backend").etat;
        this.serveurs.backend.os_name = res.response.find(item => item.role == "serveur_backend").os_name;
        this.serveurs.backend.os_version = res.response.find(item => item.role == "serveur_backend").etat;


        this.serveurs.bd.etat = res.response.find(item => item.role == "serveur_sql").etat;
        this.serveurs.bd.os_name = res.response.find(item => item.role == "serveur_sql").os_name;
        this.serveurs.bd.os_version = res.response.find(item => item.role == "serveur_sql").os_version;


        this.serveurs.caisse.etat = res.response.find(item => item.role == "serveur_caisse").etat;
        this.serveurs.caisse.os_name = res.response.find(item => item.role == "serveur_caisse").os_name;
        this.serveurs.caisse.os_version = res.response.find(item => item.role == "serveur_caisse").os_version;

        this.serveurs.report.etat = res.response.find(item => item.role == "serveur_raport").etat;
        this.serveurs.report.os_name = res.response.find(item => item.role == "serveur_raport").os_name;
        this.serveurs.report.os_version = res.response.find(item => item.role == "serveur_raport").os_version;

        this.serveurs.batch.etat = res.response.find(item => item.role == "serveur_batch").etat;
        this.serveurs.batch.os_name = res.response.find(item => item.role == "serveur_batch").os_name;
        this.serveurs.batch.os_version = res.response.find(item => item.role == "serveur_batch").os_version;

        this.result_section_disponibilite_serveur = true;
        const Disponible = res.response.filter(state => state.etat == 'En ligne')
        this.nombre_serveur = Disponible.length + ' /6 En ligne'

        this.check_server.etape = 2; // { etape: 0, status: false, message: '' };
        this.check_server.status = true; // { etape: 0, status: false, message: '' };


        const params_sql = {
          username: this.parametres.login_sql,
          password: this.parametres.password_sql,
          instance_sql: this.parametres.serveur_sql,
        };

        this.check_instance_bd.etape = 1 //{ etape: 0, status: false, message: '' };
        const db_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/serveur-sql?${new URLSearchParams(params_sql)}`);
        const db_response = await db_query.json();


        if (db_response.response == true) {
              this.disponibilite_instance_bd = 'Opérationnel'
              this.check_instance_bd.etape = 2 //{ etape: 0, status: false, message: '' };
              this.check_instance_bd.status = true //{ etape: 0, status: false, message: '' };
          } else {
              this.disponibilite_instance_bd = 'Pas disponible'
              this.check_instance_bd.etape = 2 //{ etape: 0, status: false, message: '' };
              this.check_instance_bd.status = false //{ etape: 0, status: false, message: '' };
        }


        const params_crm = {
          username: this.parametres.login_crm,
          password: this.parametres.password_crm,
          crm_url: this.parametres.lien_crm,
        };

        this.check_crm.etape = 1;

        this.check_crm.etape = 1; // = { etape: 0, status: false, message: '' };
        const crm_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/frontend-crm?${new URLSearchParams(params_crm)}`);
        const crm_response = await crm_query.json();
        this.result_section_verification_crm = true;




        if (crm_response.response == true) {
          this.check_crm.etape = 2; // = { etape: 0, status: false, message: '' };
          this.check_crm.status = true; // = { etape: 0, status: false, message: '' };
          this.disponibilite_crm = 'Accessible'
        } else {
          this.check_crm.etape = 2; // = { etape: 0, status: false, message: '' };
          this.check_crm.status = false; // = { etape: 0, status: false, message: '' };
          this.disponibilite_crm = 'Pas accessible'
        }

        const catalogues_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/serveur-sql/recuperation/catalogue?${new URLSearchParams(params_sql)}`);
        const catalogues_response = await catalogues_query.json();
        this.result_section_verification_bd = true;

        this.check_catalogue.etape = 1; // { etape: 0, status: false, message: '' };

        if (catalogues_response.status == 200) {
          this.result_section_recuperation_catalogues = true
          this.catalogues = catalogues_response.response.filter(item => item !== 'master' && item !== 'tempdb' && item != 'model' && item != 'msdb')


          const mscrm = this.catalogues.filter(item => item.toLowerCase().includes('_mscrm')); // Filtrage des items
          this.catalogues_mscrm = this.catalogues.filter(item => item.toLowerCase().includes('_mscrm')); // Filtrage des items

          this.check_catalogue.etape = 2; // { etape: 0, status: false, message: '' };
          this.check_catalogue.status = true; // { etape: 0, status: false, message: '' };

        } else {
          this.result_section_recuperation_catalogues = false
          this.check_catalogue.etape = 2; // { etape: 0, status: false, message: '' };
          this.check_catalogue.status = false; // { etape: 0, status: false, message: '' };
        }



      this.check_fonction_generale.etape = 1;

      const verification_fg = this.catalogues_mscrm.map(async (item) => {
        const params_sql2 = {
          username: this.parametres.login_sql,
          password: this.parametres.password_sql,
          instance_sql: this.parametres.serveur_sql,
          lien_crm: this.parametres.lien_crm,
          serveur_batch: this.parametres.serveur_batch,
          database: item,
        };
        const fn_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/crm/fonction_generale?${new URLSearchParams(params_sql2)}`);
        const fn_response = await fn_query.json();

        return fn_response;
      });

      this.section_verification_fontion_generale = true
      this.result_section_verification_fontion_generale = await Promise.all(verification_fg)
      this.check_fonction_generale.etape = 2;
      this.check_fonction_generale.status = true;

      this.check_organizationID.etape = 1;


      const verification_organisationId = this.catalogues_mscrm.map(async (item) => {
        const params_sql2 = {
          username: this.parametres.login_sql,
          password: this.parametres.password_sql,
          instance_sql: this.parametres.serveur_sql,
          lien_crm: this.parametres.lien_crm,
            serveur_batch: this.parametres.serveur_batch,
            database: item,
          };
          const fn_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/serveur-sql/recuperation/organisation-id?${new URLSearchParams(params_sql2)}`);
          const fn_response = await fn_query.json();

          return fn_response;
        });
        const liste_organisationId = await Promise.all(verification_organisationId)
        this.check_organisationId = liste_organisationId[0]
        this.check_organizationID.etape = 2;
        this.check_organizationID.status = true;

        console.log(this.check_organisationId);

        this.check_ps_funtion.etape = 1;

        const ps_fun = this.catalogues.map(async (item) => {
          const params_sql2 = {
            username: this.parametres.login_sql,
            password: this.parametres.password_sql,
            instance_sql: this.parametres.serveur_sql,
            lien_crm: this.parametres.lien_crm,
            serveur_batch: this.parametres.serveur_batch,
            database: item,
          };
          const ps_function_query = await fetch(`http://127.0.0.1:5000/organisation/disponibilite/serveur-sql/recuperation/ps-functions?${new URLSearchParams(params_sql2)}`);
          const ps_function_response = await ps_function_query.json();
          // console.log(ps_function_response);

          return ps_function_response

        })
        this.check_ps_funtion.etape = 2;
        this.check_ps_funtion.etape = true;


        // console.log(ps_fun);
        this.result_ps_function_par_catalogues = await Promise.all(ps_fun)
        // console.log("liste cat : " + this.result_ps_function_par_catalogues);
        this.result_ps_function_par_catalogues.map(item => {
          this.catalogues_ps = this.catalogues_ps + item.response.ps_probleme.length
          this.catalogues_function = this.catalogues_function + item.response.func_probleme.length
          // console.log(item);

        })

        this.check_service_windows.etape = 1;
        const params_service_batch = {
          username: this.parametres.login_crm,
          password: this.parametres.password_crm,
          server: this.parametres.serveur_batch,
          role: 'batch',
        };
        const batch_service_query = await fetch(`http://127.0.0.1:5000/organisation/recuperation/service/windows?${new URLSearchParams(params_service_batch)}`);
        const batch_service_response = await batch_service_query.json();

        this.check_service_windows.etape = 2;
        this.check_service_windows.status = true;
        console.log(batch_service_response);

        this.show_result = true

      } catch (error) {
        console.error("Erreur lors de l'appel API pour les détails de l'organisation", error);
      }
    },
  },
};
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
      </form>
    </div>




    <!--

<div class="mb-4 border-b border-gray-200 dark:border-gray-700">
    <ul class="flex flex-wrap -mb-px text-sm font-medium text-center" id="default-tab" data-tabs-toggle="#default-tab-content" role="tablist">
        <li class="me-2" role="presentation">
            <button class="inline-block p-4 border-b-2 rounded-t-lg" id="profile-tab" data-tabs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">Profile</button>
        </li>
        <li class="me-2" role="presentation">
            <button class="inline-block p-4 border-b-2 rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300" id="dashboard-tab" data-tabs-target="#dashboard" type="button" role="tab" aria-controls="dashboard" aria-selected="false">Dashboard</button>
        </li>
        <li class="me-2" role="presentation">
            <button class="inline-block p-4 border-b-2 rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300" id="settings-tab" data-tabs-target="#settings" type="button" role="tab" aria-controls="settings" aria-selected="false">Settings</button>
        </li>
        <li role="presentation">
            <button class="inline-block p-4 border-b-2 rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300" id="contacts-tab" data-tabs-target="#contacts" type="button" role="tab" aria-controls="contacts" aria-selected="false">Contacts</button>
        </li>
    </ul>
</div>
<div id="default-tab-content">
    <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="profile" role="tabpanel" aria-labelledby="profile-tab">
        <p class="text-sm text-gray-500 dark:text-gray-400">This is some placeholder content the <strong class="font-medium text-gray-800 dark:text-white">Profile tab's associated content</strong>. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling.</p>
    </div>
    <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="dashboard" role="tabpanel" aria-labelledby="dashboard-tab">
        <p class="text-sm text-gray-500 dark:text-gray-400">This is some placeholder content the <strong class="font-medium text-gray-800 dark:text-white">Dashboard tab's associated content</strong>. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling.</p>
    </div>
    <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="settings" role="tabpanel" aria-labelledby="settings-tab">
        <p class="text-sm text-gray-500 dark:text-gray-400">This is some placeholder content the <strong class="font-medium text-gray-800 dark:text-white">Settings tab's associated content</strong>. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling.</p>
    </div>
    <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="contacts" role="tabpanel" aria-labelledby="contacts-tab">
        <p class="text-sm text-gray-500 dark:text-gray-400">This is some placeholder content the <strong class="font-medium text-gray-800 dark:text-white">Contacts tab's associated content</strong>. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling.</p>
    </div>
</div> -->



    <div v-if="result_section && show_result"
      class="w-[100%] p-4 mt-5 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-8 dark:bg-gray-800 dark:border-gray-700">
      <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="mb-8">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-800">Vérification de l'Environnement : <strong> {{
                organisation.Nom }}</strong> </h1>
              <p class="text-gray-600">Vérification en temps réel de l'état des services</p>
            </div>
            <!-- <div class="flex items-center">
              <span id="last-update" class="text-sm text-gray-500 mr-4">Dernière mise à jour: 08/03/2025 10:35</span>
              <button id="refresh-btn"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center">
                <i class="fas fa-sync-alt mr-2"></i> Actualiser
              </button>
            </div> -->
          </div>
        </header>

        <!-- Résumé des statuts -->
        <div class="mb-8 grid grid-cols-1 md:grid-cols-5 gap-4">
          <div class="bg-white p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-2">Serveurs</h3>
            <div class="flex items-center">
              <span class="status-indicator status-up"></span>
              <span>{{ nombre_serveur }} </span>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-2">Base de données</h3>
            <div class="flex items-center">
              <span class="status-indicator status-up"
                v-if="disponibilite_instance_bd && disponibilite_instance_bd == 'Opérationnel'"></span>
              <span class="status-indicator status-warning"
                v-if="disponibilite_instance_bd && disponibilite_instance_bd != 'Opérationnel'"></span>
              <span>{{ disponibilite_instance_bd }}</span>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-2">CRM</h3>
            <div class="flex items-center">
              <span class="status-indicator status-up"
                v-if="disponibilite_crm && disponibilite_crm == 'Accessible'"></span>
              <span class="status-indicator status-warning"
                v-else-if="disponibilite_crm && disponibilite_crm != 'Accessible'"></span>

              <span> {{ disponibilite_crm }} </span>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-2">Catalogues</h3>
            <div class="flex items-center">
              <span class="status-indicator status-warning"></span>
              <span>Attention requise</span>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold mb-2">Web Functions</h3>
            <div class="flex items-center">
              <span class="status-indicator status-up"></span>
              <span>Opérationnel</span>
            </div>
          </div>
        </div>

        <!-- Détails des vérifications -->
        <div class="grid grid-cols-1 gap-8" v-if="result_section_disponibilite_serveur">
          <!-- Disponibilité des serveurs -->
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="bg-gray-50 px-4 py-3 border-b">
              <h2 class="text-xl font-semibold">Disponibilité des Serveurs</h2>
            </div>
            <div class="p-4">
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Serveur
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Informations sur le système</th>
                    <!--         <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dernière vérification</th> -->
                    <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions
                    </th> -->
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-desktop text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur Frontend</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.frontend && serveurs.frontend.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.frontend && serveurs.frontend.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.frontend.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">

                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.frontend.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.frontend.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-server text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur Backend</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.backend && serveurs.backend.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.backend && serveurs.backend.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.backend.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">

                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.backend.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.backend.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-database text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur Base de Données</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.bd && serveurs.bd.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.bd && serveurs.bd.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.bd.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.bd.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.bd.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--             <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-cogs text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur Batch</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.batch && serveurs.batch.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.batch && serveurs.batch.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.batch.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.batch.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.batch.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--             <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-cogs text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur Caisse</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.caisse && serveurs.caisse.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.caisse && serveurs.caisse.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.caisse.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.caisse.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.caisse.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <i class="fas fa-chart-bar text-gray-400 mr-2"></i>
                        <div class="text-sm font-medium text-gray-900">Serveur de Rapport</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="serveurs.report && serveurs.report.etat == 'En ligne'"></span>
                        <span class="status-indicator status-warning"
                          v-if="serveurs.report && serveurs.report.etat != 'En ligne'"></span>
                        <span class="text-sm text-gray-900">{{ serveurs.report.etat }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">

                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nom de l'OS : <strong>{{ serveurs.report.os_name }} </strong>
                          </span>
                        </li>
                        <li class="flex space-x-2 rtl:space-x-reverse items-center">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Version de l'OS : <strong>{{ serveurs.report.os_version }} </strong>
                          </span>
                        </li>

                      </ul>
                    </td>
                    <!--            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    Il y a 2 minutes
                                </td> -->
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button class="text-blue-600 hover:text-blue-900 mr-3">Détails</button>
                      <button class="text-blue-600 hover:text-blue-900">Tester</button>
                    </td> -->
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Tests CRM et Base de données -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Vérifications CRM -->
            <div class="bg-white rounded-lg shadow-md overflow-hidden" v-if="result_section_verification_crm">
              <div class="bg-gray-50 px-4 py-3 border-b">
                <h2 class="text-xl font-semibold">Vérifications CRM</h2>
              </div>
              <div class="p-4">
                <ul class="divide-y divide-gray-200">
                  <!-- <li class="py-3">
                                <div class="flex justify-between items-center">
                                    <div class="flex items-center">
                                        <span class="status-indicator status-up"></span>
                                        <span class="text-sm font-medium text-gray-900">Disponibilité du lien CRM</span>
                                    </div>
                                    <button class="text-sm text-blue-600 hover:text-blue-900"  v-if="disponibilite_crm =='Accessible' ">
                                      <i class="fa fa-check"></i>
                                    </button>
                                    <button class="text-sm text-red-600 hover:text-blue-900"  v-else>
                                      <i class="fa fa-times"></i>
                                    </button>
                                    <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                                </div>
                                <div class="mt-1 text-sm text-gray-500">
                                    Dernière vérification: Il y a 2 minutes
                                </div>
                            </li> -->
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="disponibilite_crm && disponibilite_crm == 'Accessible'"></span>
                        <span class="status-indicator status-warning"
                          v-if="disponibilite_crm && disponibilite_crm != 'Accessible'"></span>
                        <span class="text-sm font-medium text-gray-900">Connexion à CRM</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="disponibilite_crm == 'Accessible'">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i>
                      </button>
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">
                                    Dernière vérification: Il y a 2 minutes
                                </div> -->
                  </li>
                  <li class="py-3"
                    v-if="disponibilite_crm && disponibilite_crm == 'Accessible' && section_verification_fontion_generale">
                    <!-- <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"></span>
                        <span class="text-sm font-medium text-gray-900">Ressource Web: Fonctions générales</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      Dernière vérification: Il y a 3 minutes
                    </div> -->


                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Ressource Web: Fonctions générales</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="result_section_verification_fontion_generale.length > 0">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i>
                        <a href="" class="text-sm text-blue-600 hover:text-blue-900"> &nbsp; Détails</a>
                      </button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500"
                      v-for="(fn, index) in result_section_verification_fontion_generale" :key="index">
                      <strong>{{ fn.response.catalogue }}</strong> <br>
                      {{ fn.message }}
                      <blockquote
                        class="p-4 my-4 border-s-4 border-gray-300 bg-gray-50 dark:border-gray-500 dark:bg-gray-800"
                        v-if="fn.status == 200">
                        <p class="text italic font-medium leading-relaxed text-gray-900 dark:text-white">
                          {{ fn.response.portion }}
                        </p>
                      </blockquote>
                    </div>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Vérifications Base de données -->
            <div class="bg-white rounded-lg shadow-md overflow-hidden">
              <div class="bg-gray-50 px-4 py-3 border-b">
                <h2 class="text-xl font-semibold">Vérifications Base de Données</h2>
              </div>
              <div class="p-4">
                <ul class="divide-y divide-gray-200">
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"></span>
                        <span class="text-sm font-medium text-gray-900">Disponibilité de l'instance</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="disponibilite_instance_bd = 'Opérationnel'">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i> <a href="#"> De</a>
                      </button>
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">
                                    Dernière vérification: Il y a 2 minutes result_section_recuperation_catalogues
                                </div> -->
                  </li>
                  <li class="py-3" v-if="check_organisationId">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-down"
                          v-if="check_organisationId.response.length > 0"></span>
                        <span class="status-indicator status-up"
                          v-if="check_organisationId.response.length == 0"></span>
                        <span class="text-sm font-medium text-gray-900">OrganisationID dans les tables : {{
                          check_organisationId.response.length }} table(s)</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="check_organisationId.response.length == 0">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i>
                        <a href="#" class=" text-blue-600 hover:text-blue-900"> Details</a>
                      </button>
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">

                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400"
                        >
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center"
                        v-for="tb in check_organisationId.response" :key="tb">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <strong>{{tb}}</strong> a des données avec une mauvaise OrganisationID

                          </span>
                        </li>
                      </ul>
                    </div> -->
                    <!-- <div class="mt-1 text-sm text-gray-500">
                                    Dernière vérification: Il y a 2 minutes result_section_recuperation_catalogues
                                </div> -->
                  </li>
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-down"
                          v-if="result_section_recuperation_catalogues == 'Opérationnel' && (catalogues_ps > 0 || catalogues_function > 0)"></span>
                        <span class="status-indicator status-up" v-else></span>
                        <span class="text-sm font-medium text-gray-900">Vérification des catalogues</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="result_section_recuperation_catalogues == 'Opérationnel' && catalogues_ps == 0 && catalogues_function == 0">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900"
                        v-if="result_section_recuperation_catalogues == 'Opérationnel' && (catalogues_ps > 0 || catalogues_function > 0)">
                        <i class="fa fa-times"></i>
                        <a href="" class="text-sm text-blue-600 hover:text-blue-900"> Détails</a>
                      </button>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900"  v-if="result_section_recuperation_catalogues = 'Opérationnel'">Détails</button> -->
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">
                      Récupération des catalogues
                    </div> -->
                    <!-- <div class="mt-2 text-sm text-green-600 bg-green-50 p-2 rounded"
                      v-if="result_section_recuperation_catalogues = 'Opérationnel'"> -->
                    <!-- {{ catalogues.length }} catalogues trouvés: <strong v-for="cat in catalogues" :key="cat"> {{ cat
                      }} ,</strong> -->




                    <!-- <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex space-x-2 rtl:space-x-reverse items-center" v-for="cat in catalogues" :key="cat">
                          <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                          </svg>
                          <span class="leading-tight">{{ cat }}</span>
                        </li>
                      </ul> -->
                    <!-- </div> -->
                    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
                      <ul role="list" class="space-y-4 pt-2 text-gray-500 dark:text-gray-400">
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nombre de PS ayant un souci de catalogues : {{ catalogues_ps }}
                          </span>
                        </li>
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            Nombre de fonction ayant un souci de catalogues : {{ catalogues_function }}
                          </span>
                        </li>
                      </ul>
                      <!-- <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"
                        v-if="result_section_recuperation_catalogues = 'Opérationnel'">
                        <thead class="text-xs text-gray-700 uppercase dark:text-gray-400">
                          <tr>
                            <th scope="col" class="px-6 py-3 bg-gray-50 dark:bg-gray-800">
                              Catalogues
                            </th>
                            <th scope="col" class="px-6 py-3">
                              P.S.
                            </th>
                            <th scope="col" class="px-6 py-3 bg-gray-50 dark:bg-gray-800">
                              Fonctions {{catalogues_function}}
                            </th>

                          </tr>
                        </thead>
                        <tbody>
                          <tr class="border-b border-gray-200 dark:border-gray-700"
                            v-for="cat in result_ps_function_par_catalogues" :key="cat">
                            <th scope="row"
                              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">

                              {{ cat.catalogue }}
                            </th>
                            <td class="px-6 py-4">
                              <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                                <li class="flex space-x-2 rtl:space-x-reverse items-center">
                                  <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                      d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                                  </svg>
                                  <span class="leading-tight">Total : {{ cat.response.ps }}</span>
                                </li>
                                <li class="flex space-x-2 rtl:space-x-reverse items-center">
                                  <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                      d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                                  </svg>
                                  <span class="leading-tight">Souci de catalogues : {{ cat.response.ps_probleme.length
                                    }}</span>
                                </li>

                              </ul>
                            </td>
                            <td class="px-6 py-4 bg-gray-50 dark:bg-gray-800">
                              <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                                <li class="flex space-x-2 rtl:space-x-reverse items-center">
                                  <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                      d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                                  </svg>
                                  <span class="leading-tight">Total : {{ cat.response.fonction }}</span>
                                </li>
                                <li class="flex space-x-2 rtl:space-x-reverse items-center">
                                  <svg class="shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                      d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
                                  </svg>
                                  <span class="leading-tight">Souci de catalogues : {{ cat.response.func_probleme.length
                                    }}</span>
                                </li>

                              </ul>
                            </td>

                          </tr>

                        </tbody>
                      </table> -->
                    </div>
                    <!-- <div class="mt-2 text-sm text-amber-600 bg-amber-50 p-2 rounded">
                                    2 catalogues manquants: CAT_USERS, CAT_PRODUCTS
                                </div> -->
                  </li>

                </ul>
              </div>
            </div>
          </div>
          <!-- Tests CRM et Base de données -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Vérifications CRM -->
            <div class="bg-white rounded-lg shadow-md overflow-hidden" v-if="result_section_verification_crm">
              <div class="bg-gray-50 px-4 py-3 border-b">
                <h2 class="text-xl font-semibold">Vérifications sur les services Windows et Web</h2>
              </div>
              <div class="p-4">
                <ul class="divide-y divide-gray-200">

                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"
                          v-if="disponibilite_crm && disponibilite_crm == 'Accessible'"></span>
                        <span class="status-indicator status-warning"
                          v-if="disponibilite_crm && disponibilite_crm != 'Accessible'"></span>
                        <span class="text-sm font-medium text-gray-900">Connexion à CRM</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="disponibilite_crm == 'Accessible'">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i>
                      </button>
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">
                                    Dernière vérification: Il y a 2 minutes
                                </div> -->
                  </li>
                  <li class="py-3"
                    v-if="disponibilite_crm && disponibilite_crm == 'Accessible' && section_verification_fontion_generale">
                    <!-- <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-up"></span>
                        <span class="text-sm font-medium text-gray-900">Ressource Web: Fonctions générales</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      Dernière vérification: Il y a 3 minutes
                    </div> -->


                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Ressource Web: Fonctions générales</span>
                      </div>
                      <!-- <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button> -->
                      <button class="text-sm text-blue-600 hover:text-blue-900"
                        v-if="result_section_verification_fontion_generale.length > 0">
                        <i class="fa fa-check"></i>
                      </button>
                      <button class="text-sm text-red-600 hover:text-blue-900" v-else>
                        <i class="fa fa-times"></i>
                        <a href="" class="text-sm text-blue-600 hover:text-blue-900"> &nbsp; Détails</a>
                      </button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500"
                      v-for="(fn, index) in result_section_verification_fontion_generale" :key="index">
                      <strong>{{ fn.response.catalogue }}</strong> <br>
                      {{ fn.message }}
                      <blockquote
                        class="p-4 my-4 border-s-4 border-gray-300 bg-gray-50 dark:border-gray-500 dark:bg-gray-800"
                        v-if="fn.status == 200">
                        <p class="text italic font-medium leading-relaxed text-gray-900 dark:text-white">
                          {{ fn.response.portion }}
                        </p>
                      </blockquote>
                    </div>
                  </li>
                </ul>
              </div>
            </div>


          </div>
          <!-- Vérifications des catalogues -->
          <div class="bg-white rounded-lg shadow-md overflow-hidden"
            v-if="result_section_recuperation_catalogues = 'Opérationnel'">
            <div class="bg-gray-50 px-4 py-3 border-b">
              <h2 class="text-xl font-semibold">Vérifications des Catalogues</h2>
            </div>
            <div class="p-4">
              <!-- <div class="mb-4">
                <div class="flex items-center mb-2">
                  <span class="status-indicator status-warning"></span>
                  <span class="text-sm font-medium text-gray-900">État global des catalogues</span>
                </div>
                <div class="text-sm text-amber-600 bg-amber-50 p-2 rounded">
                  Certains catalogues nécessitent votre attention
                </div>
              </div> -->
              <div>
                <ul class="divide-y divide-gray-200">
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Vérification des catalogues dans les PS</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      <!-- 36/36 procédures stockées vérifiées -->
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400"
                        v-for="cat in result_ps_function_par_catalogues" :key="cat">
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center"
                          v-for="ps in cat.response.ps_probleme" :key="ps">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            <strong>{{ ps.nom }}</strong> sur <strong>{{ ps.source }}</strong> semble avoir <strong>{{
                              ps.catalogue_detecte }}</strong> qui n'est pas sur cette instance de base données
                          </span>
                        </li>
                      </ul>
                    </div>
                  </li>
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Vérification des catalogues dans les
                          fonctions</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      <!-- 36/36 procédures stockées vérifiées -->
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400"
                        v-for="cat in result_ps_function_par_catalogues" :key="cat">
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center"
                          v-for="ps in cat.response.func_probleme" :key="ps">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <!-- {{ps}} -->
                            <strong>{{ ps.nom }}</strong> sur <strong>{{ ps.source }}</strong> semble avoir <strong>{{
                              ps.catalogue_detecte }}</strong> qui n'est pas sur cette instance de base données
                          </span>
                        </li>
                      </ul>
                    </div>
                    <!-- <div class="mt-1 text-sm text-gray-500">
                      42/44 fonctions vérifiées
                    </div> -->
                    <!-- <div class="mt-2 text-sm text-amber-600 bg-amber-50 p-2 rounded">
                      Problèmes détectés: Fonction fn_GetUserRights, fn_GetProductPrice
                    </div> -->
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-md overflow-hidden"
            v-if="result_section_recuperation_catalogues = 'Opérationnel'">
            <div class="bg-gray-50 px-4 py-3 border-b">
              <h2 class="text-xl font-semibold">Vérifications des données</h2>
            </div>
            <div class="p-4">
              <!-- <div class="mb-4">
                <div class="flex items-center mb-2">
                  <span class="status-indicator status-warning"></span>
                  <span class="text-sm font-medium text-gray-900">État global des catalogues</span>
                </div>
                <div class="text-sm text-amber-600 bg-amber-50 p-2 rounded">
                  Certains catalogues nécessitent votre attention
                </div>
              </div> -->
              <div>
                <ul class="divide-y divide-gray-200">
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Vérification de OrganisationID</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      <!-- 36/36 procédures stockées vérifiées -->
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center"
                          v-for="tb in check_organisationId.response" :key="tb">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <strong>{{ tb }}</strong> a des données avec une mauvaise OrganisationID

                          </span>
                        </li>
                      </ul>
                    </div>
                  </li>

                </ul>
              </div>
            </div>
          </div>


          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="bg-gray-50 px-4 py-3 border-b">
              <h2 class="text-xl font-semibold">Services windows sur le serveur Batch</h2>
            </div>
            <div class="p-4">
              <!-- <div class="mb-4">
                <div class="flex items-center mb-2">
                  <span class="status-indicator status-warning"></span>
                  <span class="text-sm font-medium text-gray-900">État global des catalogues</span>
                </div>
                <div class="text-sm text-amber-600 bg-amber-50 p-2 rounded">
                  Certains catalogues nécessitent votre attention
                </div>
              </div> -->
              <div>
                <ul class="divide-y divide-gray-200">
                  <li class="py-3">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center">
                        <span class="status-indicator status-warning"></span>
                        <span class="text-sm font-medium text-gray-900">Litse des services windows</span>
                      </div>
                      <button class="text-sm text-blue-600 hover:text-blue-900">Tester</button>
                    </div>
                    <div class="mt-1 text-sm text-gray-500">
                      <!-- 36/36 procédures stockées vérifiées -->
                      <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                        <li class="flex text-red-700 space-x-2 rtl:space-x-reverse items-center"
                          v-for="tb in check_organisationId.response" :key="tb">
                          <i class="fa fa-times"></i>
                          <span class="text-black">
                            <strong>{{ tb }}</strong> a des données avec une mauvaise OrganisationID

                          </span>
                        </li>
                      </ul>
                    </div>
                  </li>

                </ul>
              </div>
            </div>
          </div>
        </div>


        <!-- Historique des vérifications -->
        <div class="mt-8 bg-white rounded-lg shadow-md overflow-hidden" v-if="result_section_historique">
          <div class="bg-gray-50 px-4 py-3 border-b flex justify-between items-center">
            <h2 class="text-xl font-semibold">Historique des Vérifications</h2>
            <div>
              <button class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">Dernières
                24h</button>
            </div>
          </div>
          <div class="p-4 overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date/Heure
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Résultat
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Détails
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    08/03/2025 10:30
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Vérification complète
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      Attention requise
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button class="text-blue-600 hover:text-blue-900">Voir détails</button>
                  </td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    08/03/2025 08:15
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Vérification complète
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Succès
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button class="text-blue-600 hover:text-blue-900">Voir détails</button>
                  </td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    07/03/2025 18:45
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Vérification complète
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Succès
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button class="text-blue-600 hover:text-blue-900">Voir détails</button>
                  </td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    07/03/2025 12:30
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Vérification complète
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Succès
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button class="text-blue-600 hover:text-blue-900">Voir détails</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="result_section && !show_result"
      class="w-[100%] p-4 mt-5 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-8 dark:bg-gray-800 dark:border-gray-700">

      <div id="detailed-pricing" class="w-full overflow-x-auto">
        <div class="overflow-hidden min-w-max">
          <div
            class="grid grid-cols-2 p-4 text-sm font-medium text-gray-900 bg-gray-100 border-t border-b border-gray-200 gap-x-16 dark:bg-gray-800 dark:border-gray-700 dark:text-white">
            <div class="flex items-center">Vérification à effectuer</div>
            <!-- <div>Durée</div> -->
            <div>Status</div>
            <!-- <div>Designer Edition</div> -->
          </div>

          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Récupération des données depuis le help
            </div>


            <!-- <div>
              00:00:00
            </div> -->
            <div>
              <div role="status" v-if="check_param.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_param.etape == 2 && check_param.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_param.etape == 2 && check_param.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>

          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Disponibilité et caractéristiques des serveurs
            </div>

            <!-- <div>
              00:00:00
            </div> -->
            <div>
              <div>
              <div role="status" v-if="check_server.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_server.etape == 2 && check_server.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_server.etape == 2 && check_server.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
            </div>
          </div>

          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Disponibilité de l'instance de base de données
            </div>

            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_instance_bd.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_instance_bd.etape == 2 && check_instance_bd.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_instance_bd.etape == 2 && check_instance_bd.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>

          </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Accessibilité à l'application CRM
            </div>


            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_crm.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_crm.etape == 2 && check_crm.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_crm.etape == 2 && check_crm.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Récupération des catalogues sur l'instance
            </div>


            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_catalogue.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_catalogue.etape == 2 && check_catalogue.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_catalogue.etape == 2 && check_catalogue.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Vérification de la fonction générale
            </div>


            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_fonction_generale.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_fonction_generale.etape == 2 && check_fonction_generale.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_fonction_generale.etape == 2 && check_fonction_generale.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Vérification des champs OrganizationId dans les tables CRM
            </div>

            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_organizationID.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_organizationID.etape == 2 && check_organizationID.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_organizationID.etape == 2 && check_organizationID.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Vérification des catalogues dans les PS et Fontions
            </div>
<!--
            <div>
              00:00:00
            </div> -->
            <div>


              <div role="status" v-if="check_ps_funtion.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_ps_funtion.etape == 2 && check_ps_funtion.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_ps_funtion.etape == 2 && check_ps_funtion.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>
          <div
            class="grid grid-cols-2 px-4 py-5 text-sm text-gray-700 border-b border-gray-200 gap-x-16 dark:border-gray-700">
            <div class="text-gray-500 dark:text-gray-400">
              Récupération des services windows
            </div>

            <!-- <div>
              00:00:00
            </div> -->
            <div>

              <div role="status" v-if="check_service_windows.etape == 1">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
              <div role="status" v-if="check_service_windows.etape == 2 && check_service_windows.status != true">
                <svg class="w-3 h-3 text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
              </div>

              <div role="status" v-if="check_service_windows.etape == 2 && check_service_windows.status">
                <svg class="w-3 h-3 text-green-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 16 12">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5.917 5.724 10.5 15 1.5" />
                </svg>
              </div>
            </div>
          </div>

        </div>
      </div>




<!--

      <div class="container mx-auto px-4 py-8">
        <div class="text-center">
          <div role="status">
            <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor" />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill" />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>
    </div>
  </div> -->

</template>



<style></style>

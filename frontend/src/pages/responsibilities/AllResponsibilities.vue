<template>
  <div>
    <q-table
      title="All Responsibilities"
      :data="allResponsibilities()"
      :columns="tableColumns"
      :pagination="initialTablePagination"
      :filter="tableFilter"
      :filter-method="tableFilterMethod"
      row-key="pk"
      :dense="$q.screen.lt.xl"
      :grid="$q.screen.lt.lg"
    >
      <template v-slot:top-right>
        <q-input borderless dense clearable debounce="300" v-model="tableFilter" placeholder="Search">
          <template v-slot:prepend>
            <q-icon name="search">
              <q-tooltip>
                Type to search on Name, Description, Tag name, or Employee Name
              </q-tooltip>
            </q-icon>
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props">
            {{ props.row.name }}
          </q-td>
          <q-td key="description" :props="props">
            {{ props.row.description }}
          </q-td>
          <q-td key="link" :props="props">
            <a :href="props.row.link">{{ props.row.link }}</a>
          </q-td>
          <q-td key="tags" :props="props">
            <q-chip v-for="tag of props.row.tags" :key="tag.name" clickable @click="navigateToTag(tag.pk)" color="secondary" text-color="white">{{ tag.name }}</q-chip>
          </q-td>
          <q-td key="primary_employee_name" :props="props">
            <router-link v-if="props.row.primary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.primary_employee_pk} }">
              {{ props.row.primary_employee_name }}
            </router-link>
          </q-td>
          <q-td key="secondary_employee_name" :props="props">
            <router-link v-if="props.row.secondary_employee_pk" :to="{ name: 'employee-secondary-responsibilities', params: { pk: props.row.secondary_employee_pk} }">
              {{ props.row.secondary_employee_name }}
            </router-link>
          </q-td>
          <q-td key="actions" :props="props">
            <q-btn class="col edit-button" dense round flat color="grey" @click="showEditDialog(props.row)" icon="edit"></q-btn>
            <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props.row)" icon="delete"></q-btn>
          </q-td>
        </q-tr>
      </template>
      <!-- For grid mode, we need to specify everything in order for our action buttons to render -->
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 grid-style-transition">
          <q-card class="q-py-sm">
            <q-list dense>
              <q-item v-for="col in props.cols" :key="col.name">
                <div class="q-table__grid-item-row">
                  <div class="q-table__grid-item-title">{{ col.label }}</div>
                  <div class="q-table__grid-item-value" v-if="['name', 'description'].includes(col.name)">
                    {{ col.value }}
                  </div>
                  <div class="q-table__grid-item-value" v-else-if="col.name == 'link'">
                    <a :href="col.value">{{ col.value }}</a>
                  </div>
                  <div class="q-table__grid-item-value" v-else-if="col.name == 'tags'">
                    <q-chip v-for="tag of col.value" :key="tag.name" clickable @click="navigateToTag(tag.pk)" color="secondary" text-color="white">{{ tag.name }}</q-chip>
                  </div>
                  <div class="q-table__grid-item-value" v-else-if="col.name == 'primary_employee_name'">
                    <router-link v-if="props.row.primary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.primary_employee_pk} }">
                      {{ props.row.primary_employee_name }}
                    </router-link>
                  </div>
                  <div class="q-table__grid-item-value" v-else-if="col.name == 'secondary_employee_name'">
                    <router-link v-if="props.row.secondary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.secondary_employee_pk} }">
                      {{ props.row.secondary_employee_name }}
                    </router-link>
                  </div>
                  <div class="q-table__grid-item-value row q-gutter-sm" v-else>
                    <q-btn class="col edit-button" dense round flat color="grey" @click="showEditDialog(props.row)" icon="edit"></q-btn>
                    <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props.row)" icon="delete"></q-btn>
                  </div>
                </div>
              </q-item>
            </q-list>
          </q-card>
        </div>
      </template>
    </q-table>
  </div>
</template>

<style lang="scss">
.q-table {
  .table-description {
    white-space: normal;
  }
  .table-link {
    white-space: normal;
  }
  .table-tags {
    white-space: normal;
  }
}


 @media only screen and (max-width: 1600px) {
  .q-table td {
    white-space: normal;
  }
 }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import { Responsibility, VuexStoreGetters } from '../../store/types'
import shared from './shared'


@Component
export default class AllResponsibilities extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public tableFilter = ''

  public allResponsibilities(): Array<Responsibility> {
    return this.getters['responsibilityModule/allResponsibilities'].results
  }
  
  public tableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'description', required: false, label: 'Description', field: 'description', sortable: false, align: 'left', classes: 'table-description', headerClasses: 'table-description' },
    { name: 'link', required: false, label: 'Link', field: 'link', sortable: false, align: 'left', classes: 'table-link', headerClasses: 'table-link' },
    { name: 'tags', required: false, label: 'Tags', field: 'tags', sortable: false, align: 'left', classes: 'table-tags', headerClasses: 'table-tags' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    { name: 'actions', label: 'Actions', },
  ]

  public initialTablePagination = {
    rowsPerPage: 50
  }

  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  public tableFilterMethod(rows: Array<Responsibility>, term: string) {
    return shared.tableFilterMethod(rows, term, ['name', 'description', 'tags', 'primaryEmployee', 'secondaryEmployee'])
  }

  public navigateToTag(tagPk: string): void {
    this.$router.push({ name: 'tagged-responsibilities', params: { pk: tagPk }})
      .catch(e => {
        console.error('Error navigating to tag detail:', e)
      })
  }

  public showEditDialog(row: Responsibility): void {
    bus.$emit('emitOpenEditDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  public showDeleteDialog(row: Responsibility): void {
    bus.$emit('emitOpenDeleteDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  mounted() {
    // TODO: Only fetch if doesn't exist, or needs update?
    this.retrieveAllResponsibilites()
    if (this.allResponsibilities() == []) { // <----- THIS DOESN'T WORK
      this.retrieveAllResponsibilites()
    }
  }
}
</script>

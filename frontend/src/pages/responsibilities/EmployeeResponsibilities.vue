<template>
  <div>
    <div>
      <q-btn-toggle
        :value="displayEmployeeSecondaryResponsibilities"
        class="q-mb-sm"
        no-caps
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
          {label: 'Primary', value: false},
          {label: 'Secondary', value: true}
        ]"
        @click="toggleResponsibilityType()"
      />
    </div>
    <q-table
      :title="`Responsibilities for ${employeeName()}`"
      v-if="!displayEmployeeSecondaryResponsibilities"
      :data="employeePrimaryResponsibilities()"
      :columns="tableColumns"
      :pagination="initialTablePagination"
      :filter="tableFilter"
      :filter-method="tableFilterMethod"
      row-key="pk"
    >
      <template v-slot:top-right>
        <q-input borderless dense clearable debounce="300" v-model="tableFilter" placeholder="Search">
          <template v-slot:prepend>
            <q-icon name="search">
              <q-tooltip>
                Type to search on Name, Description, or Tag name
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
    </q-table>

    <q-table
      :title="`Secondary Responsibilities for ${employeeName()}`"
      v-if="displayEmployeeSecondaryResponsibilities"
      :data="employeeSecondaryResponsibilities()"
      :columns="tableColumns"
      :pagination="initialTablePagination"
      :filter="tableFilter"
      :filter-method="tableFilterMethod"
      row-key="pk"
    >
      <template v-slot:top-right>
        <q-input borderless dense clearable debounce="300" v-model="tableFilter" placeholder="Search">
          <template v-slot:prepend>
            <q-icon name="search">
              <q-tooltip>
                Type to search on Name, Description, or Tag name
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
    </q-table>
  </div>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'
import { Responsibility, VuexStoreGetters } from '../../store/types'

@Component
export default class EmployeeResponsibilites extends Vue {
  private pk = this.$route.params.pk
  private secondary = () => {
    const routeParts = this.$route.path.split('/')
    return routeParts[routeParts.length - 1] === 'secondary'
  }
  
  private tableFilter = ''

  private employeeName(): string {
    return this.getters['responsibilityModule/simpleEmployeeDetail'].name
  }

  private displayEmployeeSecondaryResponsibilities = false

  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private tableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'description', required: false, label: 'Description', field: 'description', sortable: false, align: 'left' },
    { name: 'link', required: false, label: 'Link', field: 'link', sortable: false, align: 'left' },
    { name: 'tags', required: false, label: 'Tags', field: 'tags', sortable: false, align: 'left' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    { name: 'actions', label: 'Actions', },
  ]

  private initialTablePagination = {
    rowsPerPage: 50
  }

  private getters = this.$store.getters as VuexStoreGetters

  private toggleResponsibilityType(): void {
    let routeName
    if (this.secondary()) {
      routeName = 'employee-responsibilities'
    } else {
      routeName = 'employee-secondary-responsibilities'
    }
    this.$router.push({ name: routeName, params: { pk: this.pk }})
      .catch(e => {
        console.error('Error navigating to employee\'s other responsibilities:', e)
      })
  }

  private retrieveEmployeeName(): void {
    this.$store.dispatch('responsibilityModule/getSimpleEmployeeDetail', {pk: this.pk})
      .catch(e => {
        console.error('Error retrieving simple employee detail', e)
      })
  }

  private tableFilterMethod(rows: Array<Responsibility>, term: string) {
    // rows contain the entire data
    // terms contains whatever you have as filter
    // TODO: Make this a shared util with other tables

    const searchTerm = term ? term.toLowerCase() : ''

    const filteredRows = rows.filter(
      (row) =>{
        if (searchTerm == '') {
          // If no search term, return all rows
          return true
        } else {
          // Check name, description, and tags
          const nameMatches = row.name.toLowerCase().includes(searchTerm)
          const descriptionMatches = row.description.toLowerCase().includes(searchTerm)
          let tagsMatch = false
          for (let i=0; i<row.tags.length; i++) {
            if (row.tags[i].name.toLowerCase().includes(searchTerm)) {
              tagsMatch = true
            }
          }
          if (nameMatches || descriptionMatches || tagsMatch) {
            return true
          }
          // Assume row doesn't match
          return false
        }
      })
    return filteredRows
  }

  private employeeResponsibilities(secondary=false): Array<Responsibility> {
    let allEmployeeResponsibilities
    if (secondary) {
      allEmployeeResponsibilities = this.getters['responsibilityModule/employeeSecondaryResponsibilities']  
    } else {
      allEmployeeResponsibilities = this.getters['responsibilityModule/employeePrimaryResponsibilities']
    }
    const thisEmployeeResponsibilities = allEmployeeResponsibilities.filter((list) => list.pk == parseInt(this.pk, 10))
    if (thisEmployeeResponsibilities.length && thisEmployeeResponsibilities[0].responsibilities) {
      return thisEmployeeResponsibilities[0].responsibilities
    } else {
      return []
    }
  }

  private employeePrimaryResponsibilities(): Array<Responsibility> {
    return this.employeeResponsibilities()
  }

  private employeeSecondaryResponsibilities(): Array<Responsibility> {
    return this.employeeResponsibilities(true)
  }

  private updateName(pk: number, name: string) {
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
  }

  private cancelUpdateName(pk: number, name: string, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
    closePopupMethod()
  }

  private updateResponsibility(responsibility: Responsibility, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(responsibility.pk.toString(), {
        name: responsibility.name
        // TODO: employees
      })
      .then(() => {
        closePopupMethod()
        Notify.create('Updated responsibility')
        resolve('Updated')
      })
      .catch(e => {
        console.error('Error updating Responsibility:', e)
        reject(e)
      })
    })
  }

  private retrieveEmployeeResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeePrimaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee responsibilities', e)
      })
  }

  private retrieveEmployeeSecondaryResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeeSecondaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee secondary responsibilities', e)
      })
  }

  private navigateToTag(tagPk: string): void {
    this.$router.push({ name: 'tagged-responsibilities', params: { pk: tagPk }})
      .catch(e => {
        console.error('Error navigating to tag detail:', e)
      })
  }
  
  // TODO: Move this to a UTIL
  private isNormalInteger(str: string | (string | null)[]) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
  }

  private showEditDialog(row: Responsibility): void {
    bus.$emit('emitOpenEditDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  private showDeleteDialog(row: Responsibility): void {
    bus.$emit('emitOpenDeleteDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  mounted() {
    this.retrieveEmployeeName()
    if (this.secondary()) {
      this.displayEmployeeSecondaryResponsibilities = true 
    }
    this.retrieveEmployeeResponsibilites(this.pk)
    this.retrieveEmployeeSecondaryResponsibilites(this.pk)
  }
}
</script>

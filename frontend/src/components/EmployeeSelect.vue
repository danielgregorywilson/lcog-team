<template>
  <q-select
    v-model="selectedEmployee"
    :options="employees()"
    option-value="pk"
    option-label="name"
    :label="label"
    use-input
    hide-selected
    fill-input
    input-debounce="500"
    @filter="filterFn"
    @input="$emit('input', selectedEmployee)"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey">
          No results
        </q-item-section>
      </q-item>
    </template>
    <template v-if="selectedEmployee.name" v-slot:append>
      <q-icon name="cancel" @click.stop="clearEmployee()" class="cursor-pointer" />
    </template>
  </q-select>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { SimpleEmployeeRetrieve, VuexStoreGetters } from '../store/types'

@Component
export default class EmployeeSelect extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  public emptyEmployee = {name: '', pk: -1}
  
  @Prop({required: true}) readonly label!: string
  @Prop({required: true}) employee!: {name: string, pk: number}

  private needle = '' // For filtering employee list
  public selectedEmployee = this.emptyEmployee

  private retrieveSimpleEmployeeList(): void {
    this.$store.dispatch('peopleModule/getSimpleEmployeeList')
      .catch(e => {
        console.error('Error retrieving simple employee list', e)
      })
  }

  public employees(): Array<SimpleEmployeeRetrieve> {    
    const employees = this.getters['peopleModule/simpleEmployeeList']
    return employees.filter((employee) => {
      return employee.name.toLowerCase().indexOf(this.needle) != -1
    })
  }

  public filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      this.needle = val.toLowerCase()
    })
  }

  public clearEmployee() {
    this.selectedEmployee = this.emptyEmployee
    this.$emit('clear')
  }

  mounted() {
    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
    }
    this.selectedEmployee = this.employee
  }

  updated() {
    this.selectedEmployee = this.employee
  }

}
</script>
<template>
<div>
  <div style="display: none">{{ unit }}</div> <!-- TODO: This is a hack to force the component to render the currently selected unit -->
  <q-select
    v-model="selectedUnit"
    :options="units()"
    option-value="pk"
    option-label="name"
    :label="label"
    use-input
    hide-selected
    fill-input
    input-debounce="500"
    @filter="filterFn"
    @input="$emit('input', selectedUnit)"
    class="unit-select"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey">
          No results
        </q-item-section>
      </q-item>
    </template>
    <template v-if="selectedUnit.name" v-slot:append>
      <q-icon name="cancel" @click.stop="clearUnit()" class="cursor-pointer" />
    </template>
  </q-select>
</div>
</template>

<style scoped lang="scss">
  .unit-select {
    width: 350px
  }
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Unit, VuexStoreGetters } from '../store/types'

@Component
export default class UnitSelect extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  public emptyUnit = {name: '', pk: -1}
  
  @Prop({required: true}) readonly label!: string
  @Prop({required: true}) unit!: {name: string, pk: number}

  private needle = '' // For filtering unit list
  public selectedUnit = this.emptyUnit

  private retrieveUnitList() {
    this.$store.dispatch('peopleModule/getUnitList')
      .catch(e => {
        console.error('Error retrieving unit list', e)
      })
  }

  public units(): Array<Unit> {    
    const units = this.getters['peopleModule/unitList'].results
    if (units) {
      return units.filter((unit: Unit) => {
        return unit.name.toLowerCase().indexOf(this.needle) != -1
      })
    } else {
      return []
    }
  }

  public filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      this.needle = val.toLowerCase()
    })
  }

  public clearUnit() {
    this.selectedUnit = this.emptyUnit
    this.$emit('clear')
  }

  mounted() {
    if (!this.units().length) {
      this.retrieveUnitList()
    }
  }

  updated() {
    this.selectedUnit = this.unit
  }

}
</script>

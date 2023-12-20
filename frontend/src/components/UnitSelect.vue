<template>
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
  @update:model-value="emit('input', selectedUnit)"
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
</template>

<style scoped lang="scss">
  .unit-select {
    width: 742px
  }
</style>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'

import { usePeopleStore } from 'src/stores/people'
import { Unit } from 'src/types'

const peopleStore = usePeopleStore()

const emptyUnit = {name: '', pk: -1}

const props = defineProps<{
  label: string,
  unit: {name: string, pk: number},
}>()

const emit = defineEmits<{
  (e: 'clear'): void
  (e: 'input', arg: {name: string, pk: number}): void
}>()

let needle = ref('') // For filtering unit list
let selectedUnit = ref(emptyUnit)

function retrieveUnitList() {
  peopleStore.getUnitList()
    .catch(e => {
      console.error('Error retrieving unit list', e)
    })
}

function units(): Array<Unit> {    
  const unitList = peopleStore.unitList
  if (unitList.length) {
    return unitList
      .filter((unit: Unit) => {
        return ['Administrative Services', 'Government Services', 'Senior & Disability Services', 'Test Division'].indexOf(unit.name) != -1
      })
      .filter((unit: Unit) => {
        return unit.name.toLowerCase().indexOf(needle.value) != -1
      })
  } else {
    return []
  }
}

function filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
  update(() => {
    needle.value = val.toLowerCase()
  })
}

function clearUnit() {
  selectedUnit.value = emptyUnit
  emit('clear')
}

onMounted(() => {
  if (!units().length) {
    retrieveUnitList()
  }
})

onUpdated(() => {
  selectedUnit.value = props.unit
})
</script>

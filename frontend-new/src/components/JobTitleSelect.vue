<template>
  <q-select
    v-model="selectedTitle"
    :options="titles()"
    option-value="pk"
    option-label="name"
    :label="label"
    use-input
    hide-selected
    fill-input
    input-debounce="500"
    @filter="filterFn"
    @update:model-value="emit('input', selectedTitle)"
    class="title-select"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey">
          No results
        </q-item-section>
      </q-item>
    </template>
    <template v-if="selectedTitle.name" v-slot:append>
      <q-icon name="cancel" @click.stop="clearTitle()" class="cursor-pointer" />
    </template>
  </q-select>
  </template>
  
  <style scoped lang="scss">
    .title-select {
      width: 350px
    }
  </style>
  
  <script setup lang="ts">
  import { onMounted, onUpdated, ref } from 'vue'
  
  import { usePeopleStore } from 'src/stores/people'
  import { Title } from 'src/types'
  
  const peopleStore = usePeopleStore()
  
  const emptyTitle = {name: '', pk: -1}
  
  const props = defineProps<{
    label: string,
    title: {name: string, pk: number},
  }>()
  
  const emit = defineEmits<{
    (e: 'clear'): void
    (e: 'input', arg: {name: string, pk: number}): void
  }>()
  
  let needle = ref('') // For filtering unit list
  let selectedTitle = ref(emptyTitle)
  
  function retrieveTitleList() {
    peopleStore.getTitleList()
      .catch(e => {
        console.error('Error retrieving title list', e)
      })
  }
  
  function titles(): Array<Title> {    
    const titleList = peopleStore.titleList
    if (titleList.length) {
      return titleList.filter((title: Title) => {
        return title.name.toLowerCase().indexOf(needle.value) != -1
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
  
  function clearTitle() {
    selectedTitle.value = emptyTitle
    emit('clear')
  }
  
  onMounted(() => {
    if (!titles().length) {
      retrieveTitleList()
    }
  })
  
  onUpdated(() => {
    selectedTitle.value = props.title
  })
  </script>
  
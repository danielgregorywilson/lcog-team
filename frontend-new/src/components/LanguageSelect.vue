<template>
  <q-select
    v-model="selectedLanguage"
    :options="languageOptions"
    label="Language"
    name="language"
    id="language"
    input-debounce="500"
    @filter="filterFn"
    @update:model-value="emit('input', selectedUnit)"
  >
    <template v-if="selectedLanguage" v-slot:append>
      <q-icon name="cancel" @click.stop="clearLanguage()" class="cursor-pointer" />
    </template>
  </q-select>
  </template>

  
  <script setup lang="ts">
  import { onUpdated, ref } from 'vue'
  
  const languageOptions = [
    "American Sign Language", "Arabic", "Bengali", "Chinese", "Croatian",
    "Czech", "Danish", "Dutch", "Finnish", "French", "German", "Greek",
    "Gujarati", "Haitian Creole", "Hebrew", "Hindi", "Hungarian", "Indonesian",
    "Italian", "Japanese", "Korean", "Latvian", "Lithuanian", "Norwegian",
    "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian",
    "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil",
    "Thai", "Turkish", "Urdu", "Vietnamese", "Welsh", "Xhosa", "Zulu",
  ]

  let selectedLanguage = ref('')
  
  const props = defineProps<{
    language: string,
  }>()
  
  const emit = defineEmits<{
    (e: 'clear'): void
    (e: 'input', arg: {name: string, pk: number}): void
  }>()
  
  let needle = ref('') // For filtering language list
  
  function filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      needle.value = val.toLowerCase()
    })
  }
  
  function clearLanguage() {
    selectedLanguage.value = ''
    emit('clear')
  }
  
  onUpdated(() => {
    selectedLanguage.value = props.language
  })
  </script>
  
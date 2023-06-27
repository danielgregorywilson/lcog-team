<template>
  <q-select
    v-model="selectedLanguage"
    :options="languageOptions"
    @update:model-value="emit('input', selectedLanguage)"
    class="language-select"
  >
    <template v-if="selectedLanguage" v-slot:append>
      <q-icon name="cancel" @click.stop="clearLanguage()" class="cursor-pointer" />
    </template>
  </q-select>
  {{ selectedLanguage }}
</template>

<style scoped lang="scss">
  .language-select {
    width: 221px
  }
</style>

  
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
    foo: string,
  }>()
  
  const emit = defineEmits<{
    (e: 'clear'): void
    (e: 'input', arg: string): void
  }>()
  
  function clearLanguage() {
    selectedLanguage.value = ''
    emit('clear')
  }
  
  onUpdated(() => {
    // selectedLanguage.value = props.language
  })
  </script>
  
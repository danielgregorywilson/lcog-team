<template>
<div>
  <div v-if="statement" class="q-mt-md">
    <div class="text-h6">Statement Total: ${{ props.statement?.total }}</div>
    <q-markup-table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Item</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in statement.items" :key="item.pk">
          <td>{{ readableDateNEW(item.date) }}</td>
          <td>{{ item.description }}</td>
          <td>${{ item.amount }}</td>
        </tr>
      </tbody>
    </q-markup-table>
  </div>
  <div v-else class="q-mt-md text-h6">No statement selected</div>
</div>
</template>

<style scoped lang="scss">

</style>

<script setup lang="ts">
import { readableDateNEW } from 'src/filters'
import { ExpenseStatement } from 'src/types'

const props = defineProps<{
  statement: ExpenseStatement | undefined
}>()
</script>

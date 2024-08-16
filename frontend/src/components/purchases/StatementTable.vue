<template>
<div>
  <div v-if="statement" class="q-mt-md">
    <div class="text-h6">Statement Total: ${{ statementTotal() }}</div>
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

const statementTotal = () => {
  if (!props.statement) return 0
  return props.statement.items.reduce(
    (acc, item) => acc + parseFloat(item.amount), 0
  ).toFixed(2)
}
</script>

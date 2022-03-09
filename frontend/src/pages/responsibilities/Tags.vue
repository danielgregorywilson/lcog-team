<template>
  <div>
    <q-table
      :title="`Tags`"
      :data="allTags()"
      :columns="tableColumns"
      :pagination="initialTablePagination"
      row-key="pk"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props">
            {{ props.row.name }}
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
import { Responsibility, ResponsibilityTag, VuexStoreGetters } from '../../store/types'

@Component
export default class Tags extends Vue {
  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private tableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'actions', label: 'Actions', },
  ]

  private initialTablePagination = {
    rowsPerPage: 50
  }

  private getters = this.$store.getters as VuexStoreGetters


  private allTags(): Array<ResponsibilityTag> {
    const allTags = this.getters['responsibilityModule/allTags']
    return allTags.results
  }

  private updateTag(tag: ResponsibilityTag, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return new Promise((resolve, reject) => {
      if (tag.pk) {
        ResponsibilityDataService.updateTag(tag.pk.toString(), {
          name: tag.name
        })
        .then(() => {
          closePopupMethod()
          Notify.create('Updated tag')
          resolve('Updated')
        })
        .catch(e => {
          console.error('Error updating Tag:', e)
          reject(e)
        })
      }
    })
  }

  private retrieveTags(): void {
    this.$store.dispatch('responsibilityModule/getAllTags')
      .catch(e => {
        console.error('Error retrieving tags', e)
      })
  }
  
  // TODO: Move this to a UTIL
  private isNormalInteger(str: string | (string | null)[]) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
  }

  private showEditDialog(row: Responsibility): void {
    bus.$emit('emitOpenEditTagDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  private showDeleteDialog(row: Responsibility): void {
    bus.$emit('emitOpenDeleteTagDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  mounted() {
    this.retrieveTags()
  }
}
</script>

<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md row justify-between q-gutter-y-sm">
      <div class="q-gutter-x-sm">
        <q-btn :to="{ name: 'all-responsibilities' }" unelevated rounded color="primary" icon="visibility" label="View All" />
        <q-btn :to="{ name: 'orphaned-responsibilities' }" unelevated rounded color="primary" icon="visibility_off" label="View Orphaned" />
        <q-btn :to="{ name: 'tags' }" unelevated rounded color="primary" icon="tag" label="View Tags" />
      </div>
      <div>
        <q-btn unelevated rounded color="primary" icon="add" label="Add" @click="addDialogVisible=true" />
      </div>
    </div>
    <router-view :key="$route.path" />

    <!-- ADD RESPONSIBILITY DIALOG -->
    <q-dialog v-model="addDialogVisible">
      <q-card>
        <q-card-section>
          <q-form
            @submit="onAddFormSubmit"
            @reset="clearAddForm"
            class="q-gutter-sm"
          >
            <div class="text-h5">Add a Responsibility</div>
            <q-input
              filled
              v-model="addFormName"
              label="Name"
            />
            <q-input
              filled
              v-model="addFormDescription"
              label="Description"
            />
            <q-input
              filled
              v-model="addFormLink"
              label="Link"
            />
            <div>Tags</div>
            <q-chip v-for="tag of addFormTags" :key="addFormTags.indexOf(tag)" removable @remove="addFormRemoveTag(addFormTags.indexOf(tag))" color="secondary" text-color="white">{{ tag.name }}</q-chip>
            <div class="row justify-between">
              <q-select :value="addFormNewTag" :options="tags()" option-value="pk" option-label="name" label="Add Tag" use-input hide-selected fill-input input-debounce="500" @filter="tagFilterFn" @input-value="setNewAddTagName">
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      No results
                    </q-item-section>
                  </q-item>
                </template>
                <template v-if="addFormNewTag.name" v-slot:append>
                  <q-icon name="cancel" @click.stop="addFormNewTag = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <q-btn label="Add" color="primary" :disable="!addFormNewTag" @click="addFormAddTag(addFormNewTag)"/>
            </div>
            <q-select v-model="addFormPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="addFormPrimaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="addFormPrimaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select v-model="addFormSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee"  use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="addFormSecondaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="addFormSecondaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <div>
              <q-btn label="Submit" type="submit" color="primary" :disable="!addFormName"/>
              <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- EDIT RESPONSIBILITY DIALOG -->
    <q-dialog v-model="editDialogVisible">
      <q-card>
        <q-card-section>
          <q-form
            @submit="onEditFormSubmit"
            class="q-gutter-sm"
          >
            <div class="text-h5">Edit Responsibility</div>
            <q-input
              filled
              v-model="editFormName"
              label="Name"
            />
            <q-input
              filled
              v-model="editFormDescription"
              label="Description"
            />
            <q-input
              filled
              v-model="editFormLink"
              label="Link"
            />
            <div>Tags</div>
            <q-chip v-for="tag of editFormTags" :key="editFormTags.indexOf(tag)" removable @remove="editFormRemoveTag(editFormTags.indexOf(tag))" color="secondary" text-color="white">{{ tag.name }}</q-chip>
            <div class="row justify-between">
              <q-select :value="editFormNewTag" :options="tags()" option-value="pk" option-label="name" label="Add Tag" use-input hide-selected fill-input input-debounce="500" @filter="tagFilterFn" @input-value="setNewEditTagName">
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      No results
                    </q-item-section>
                  </q-item>
                </template>
                <template v-if="editFormNewTag.name" v-slot:append>
                  <q-icon name="cancel" @click.stop="editFormNewTag = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <q-btn label="Add" color="primary" :disable="!editFormNewTag" @click="editFormAddTag(editFormNewTag)"/>
            </div>
            <q-select v-model="editFormPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="editFormPrimaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="editFormPrimaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select v-model="editFormSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee"  use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="editFormSecondaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="editFormSecondaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <div>
              <q-btn label="Submit" type="submit" color="primary" :disable="!editFormName"/>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- DELETE RESPONSIBILITY DIALOG -->
    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="list" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this responsibility?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogResponsibilityName }}</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- EDIT TAG DIALOG -->
    <q-dialog v-model="editTagDialogVisible">
      <q-card>
        <q-card-section>
          <q-form
            @submit="onTagEditFormSubmit"
            class="q-gutter-sm"
          >
            <div class="text-h5">Edit Tag</div>
            <q-input
              filled
              v-model="editTagFormName"
              label="Name"
            />
            <div>
              <q-btn label="Submit" type="submit" color="primary" :disable="!editTagFormName"/>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- DELETE TAG DIALOG -->
    <q-dialog v-model="deleteTagDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="list" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this tag?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteTagDialogName }}</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteTag()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Notify } from 'quasar'
import { bus } from '../../App.vue'
import { Responsibility, ResponsibilityTag, SimpleEmployeeRetrieve, SimpleResponsibilityTagRetrieve, VuexStoreGetters } from '../../store/types'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'

@Component
export default class Responsibilities extends Vue {
  private emptyEmployee = {name: '', pk: -1}
  
  private addDialogVisible = false
  private addFormName = ''
  private addFormDescription = ''
  private addFormLink = ''
  private addFormTags: Array<{'name': string}> = []
  private addFormNewTag = ''
  private addFormPrimaryEmployee = this.emptyEmployee
  private addFormSecondaryEmployee = this.emptyEmployee

  private editDialogVisible = false
  private pkToEdit = -1
  private editFormName = ''
  private editFormDescription = ''
  private editFormLink = ''
  private editFormTags: Array<ResponsibilityTag> = []
  private editFormNewTag = ''
  private editFormPrimaryEmployee = this.emptyEmployee
  private editFormSecondaryEmployee = this.emptyEmployee
  
  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private editTagDialogVisible = false
  private tagPkToEdit = -1
  private editTagFormName = ''

  private deleteTagDialogVisible = false
  private deleteTagDialogName = ''
  private tagPkToDelete = ''

  private getters = this.$store.getters as VuexStoreGetters

  private needle = '' // For filtering employee list
  private tagNeedle = '' // For filtering tag list

  ///////////////
  // EMPLOYEES //
  ///////////////
  private employees(): Array<SimpleEmployeeRetrieve> {    
    const employees = this.getters['responsibilityModule/simpleEmployeeList']
    return employees.filter((employee) => {
      return employee.name.toLowerCase().indexOf(this.needle) != -1
    })
  }

  private retrieveSimpleEmployeeList(): void {
    this.$store.dispatch('responsibilityModule/getSimpleEmployeeList')
      .catch(e => {
        console.error('Error retrieving simple employee list', e)
      })
  }

  private filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      this.needle = val.toLowerCase()
    })
  }

  //////////
  // TAGS //
  //////////
  private tags(): Array<SimpleResponsibilityTagRetrieve> {    
    const tags = this.getters['responsibilityModule/simpleTagList']
    return tags.filter((tag) => {
      return tag.name.toLowerCase().indexOf(this.tagNeedle) != -1
    })
  }

  private retrieveSimpleTagList(): void {
    this.$store.dispatch('responsibilityModule/getSimpleTagList')
      .catch(e => {
        console.error('Error retrieving simple tag list', e)
      })
  }

  private tagFilterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      this.tagNeedle = val.toLowerCase()
    })
  }

  private setNewEditTagName(val: string) {
    this.editFormNewTag = val
  }

  //////////////
  // ADD FORM //
  //////////////
  private setNewAddTagName(val: string) {
    this.addFormNewTag = val
  }
  
  private addFormAddTag(): void {
    this.addFormTags.push({'name': this.addFormNewTag})
    this.addFormNewTag = ''
  }

  private addFormRemoveTag(tagIndex: number): void {
    this.addFormTags.splice(tagIndex, 1)
  }
  
  private clearAddForm() {
    this.addFormName = ''
    this.addFormDescription = ''
    this.addFormLink = ''
    this.addFormNewTag = ''
    this.addFormTags = []
    this.addFormPrimaryEmployee = this.emptyEmployee
    this.addFormSecondaryEmployee = this.emptyEmployee
  }

  private onAddFormSubmit () {
    this.createResponsibility()
      .then(() => {
        this.updateResponsibiliyLists()
        this.retrieveSimpleTagList()
        this.addDialogVisible = false
        Notify.create('Created responsibility')
        this.clearAddForm()
      })
      .catch(e => {
        console.error('Error creating Responsibility:', e)
      })
   }

  private createResponsibility() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.create({
        name: this.addFormName,
        description: this.addFormDescription,
        link: this.addFormLink,
        tags: this.addFormTags,
        primary_employee: this.addFormPrimaryEmployee.pk,
        secondary_employee: this.addFormSecondaryEmployee.pk
      })
        .then(() => {
          resolve('Created')
        })
        .catch(e => {
          console.error('Error creating Responsibility:', e)
          reject(e)
        })
    })
  }

  ///////////////
  // EDIT FORM //
  ///////////////

  private openEditDialog(row: Responsibility) {
    this.pkToEdit = row.pk
    this.editFormName = row.name
    this.editFormDescription = row.description
    this.editFormLink = row.link
    this.editFormTags = row.tags
    if (row.primary_employee_pk && row.primary_employee_name) {
      this.editFormPrimaryEmployee = { pk: row.primary_employee_pk, name: row.primary_employee_name}
    }
    if (row.secondary_employee_pk && row.secondary_employee_name) {
      this.editFormSecondaryEmployee = { pk: row.secondary_employee_pk, name: row.secondary_employee_name}
    }
    this.editDialogVisible = true
  }

  private editFormAddTag(editFormNewTag: string): void {
    let newTags = [...this.editFormTags]
    newTags.push({'name': editFormNewTag})
    this.editFormTags = newTags
    this.editFormNewTag = ''
  }

  private editFormRemoveTag(tagIndex: number): void {
    let newTags = [...this.editFormTags]
    newTags.splice(tagIndex, 1)
    this.editFormTags = newTags
  }

  private clearEditForm() {
    this.pkToEdit = -1
    this.editFormName = ''
    this.editFormDescription = ''
    this.editFormLink = ''
    this.editFormTags = []
    this.editFormNewTag = ''
    this.editFormPrimaryEmployee = this.emptyEmployee
    this.editFormSecondaryEmployee = this.emptyEmployee
  }

  private onEditFormSubmit () {
    this.editResponsibility()
      .then(() => {
        this.updateResponsibiliyLists()
        this.retrieveSimpleTagList()
        this.editDialogVisible = false
        Notify.create('Updated responsibility')
        this.clearEditForm()
      })
      .catch(e => {
        console.error('Error updating Responsibility:', e)
      })
  }

  private editResponsibility() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(this.pkToEdit.toString(), {
        name: this.editFormName,
        description: this.editFormDescription,
        link: this.editFormLink,
        tags: this.editFormTags,
        primary_employee: this.editFormPrimaryEmployee.pk,
        secondary_employee: this.editFormSecondaryEmployee.pk
      })
        .then(() => {
          resolve('Updated')
        })
        .catch(e => {
          console.error('Error updating Responsibility:', e)
          reject(e)
        })
    })
  }

  ////////////////////////////////
  // DELETE RESPONSIBILITY FORM //
  ////////////////////////////////

  private openDeleteDialog(row: Responsibility) {
    this.rowPkToDelete = row.pk.toString()
    this.deleteDialogResponsibilityName = row.name
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    ResponsibilityDataService.delete(this.rowPkToDelete)
      .then(() => {
        this.updateResponsibiliyLists()
        Notify.create('Deleted a responsibility.')
      })
      .catch(e => {
        console.error('Error deleting responsibility', e)
      })
  }

  ///////////////////
  // EDIT TAG FORM //
  ///////////////////

  private openTagEditDialog(tag: ResponsibilityTag) {
    if (tag.pk) {
      this.tagPkToEdit = tag.pk
      this.editTagFormName = tag.name
      this.editTagDialogVisible = true
    }
  }

  private clearTagEditForm() {
    this.tagPkToEdit = -1
    this.editTagFormName = ''
  }

  private onTagEditFormSubmit () {
    this.editTag()
      .then(() => {
        this.updateTagLists()
        this.editTagDialogVisible = false
        Notify.create('Updated tag')
        this.clearTagEditForm()
      })
      .catch(e => {
        console.error('Error updating Tag:', e)
      })
  }

  private editTag() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.updateTag(this.tagPkToEdit.toString(), {
        name: this.editTagFormName,
      })
        .then(() => {
          resolve('Updated')
        })
        .catch(e => {
          console.error('Error updating Tag:', e)
          reject(e)
        })
    })
  }

  /////////////////////
  // DELETE TAG FORM //
  /////////////////////

  private openDeleteTagDialog(row: ResponsibilityTag) {
    if (row.pk) {
      this.tagPkToDelete = row.pk.toString()
      this.deleteTagDialogName = row.name
      this.deleteTagDialogVisible = true
    }
  }

  private deleteTag(): void {
    ResponsibilityDataService.deleteTag(this.tagPkToDelete)
      .then(() => {
        this.updateTagLists()
        Notify.create('Deleted a tag.')
      })
      .catch(e => {
        console.error('Error deleting tag', e)
      })
  }

  ///////////////
  // SET STATE //
  ///////////////

  // Update the various responsibility lists in Vuex
  private updateResponsibiliyLists(): void {
    this.retrieveAllResponsibilites()
    this.retrieveOrphanedResponsibilites()
    const pk = this.$route.params.pk
    if (pk) {
      this.retrieveEmployeeResponsibilites(pk)
      this.retrieveEmployeeSecondaryResponsibilites(pk)
    }
  }

  // Update the various tag lists in Vuex
  private updateTagLists(): void {
    this.retrieveAllTags()
    this.retrieveSimpleTagList()
  }

  // Update All Tags Table
  private retrieveAllTags(): void {
    this.$store.dispatch('responsibilityModule/getAllTags')
      .catch(e => {
        console.error('Error retrieving tags', e)
      })
  }

  // Update All Responsibilities Table
  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  // Update Orphaned Responsibilities Table
  private retrieveOrphanedResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getOrphanedResponsibilities')
      .catch(e => {
        console.error('Error retrieving orphaned responsibilities', e)
      })
  }

  // Update Employee Responsibilities Table
  private retrieveEmployeeResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeePrimaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee responsibilities', e)
      })
  }

  // Update Employee Secondary Responsibilities Table
  private retrieveEmployeeSecondaryResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeeSecondaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee secondary responsibilities', e)
      })
  }

  created() {
    // We trigger opening the edit and delete dialogs in AllResponsibilities, EmployeeResponsibilites, or OrphanedResponsibilities
    bus.$on('emitOpenEditDialog', (row: Responsibility) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openEditDialog(row)
    })
    bus.$on('emitOpenDeleteDialog', (row: Responsibility) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openDeleteDialog(row)
    })
    bus.$on('emitOpenEditTagDialog', (row: ResponsibilityTag) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openTagEditDialog(row)
    })
    bus.$on('emitOpenDeleteTagDialog', (row: ResponsibilityTag) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openDeleteTagDialog(row)
    })
  }

  mounted() {
    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
      this.retrieveSimpleTagList()
    }
    
  }
}
</script>

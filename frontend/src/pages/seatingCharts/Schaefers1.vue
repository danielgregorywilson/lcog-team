<template>
  <q-page class="q-mt-md" id="schaefers-1-page">
    <div class="row justify-between">
      <q-select class="" v-model="selectedEmployee" :options="employees()" option-value="pk" option-label="name" label="Employee" use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              No results
            </q-item-section>
          </q-item>
        </template>
        <template v-if="selectedEmployee.name" v-slot:append>
          <q-icon name="cancel" @click.stop="selectedEmployee = emptyEmployee" class="cursor-pointer" />
        </template>
      </q-select>
      <q-btn class="" :disabled="selectedEmployee.pk == -1" @click="clickReserve()">Reserve</q-btn>
    </div>
    <div class="row q-gutter-md q-mt-sm">
      <FloorPlan class="floor-plan"/>
    </div>
    <!-- {{ desks }} -->
    <!-- {{ deskReservations[0] }} -->
  </q-page>
</template>

<style lang="scss"> 
  .floor-plan {
    width: 800px;
  }
  
  @media only screen and (max-width: 800px) {
    .floor-plan {
      width: 450px;
    }
  }
  
  @media only screen and (min-width: 1500px) {
    .floor-plan {
      width: 1600px;
    }
  }
  
  .annotation {
    position: absolute;
    background: white;
    font-size: 8px;
    text-align: center;
  }
  .annotation button {
    font-size: 10px;
  }
</style>

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import DeskReservationDataService from '../../services/DeskReservationDataService'
import FloorPlan from '../../assets/floorPlans/schaefers1.fpsvg'
import { AxiosDeskReservationCreateServerResponse, Desk, DeskReservation, SimpleEmployeeRetrieve, VuexStoreGetters } from '../../store/types'

interface EmployeeType {
  name: string
  selected: boolean
}

@Component({
  components: { FloorPlan }
})
export default class Schaefers1 extends Vue{
  private getters = this.$store.getters as VuexStoreGetters

  private needle = '' // For filtering employee list
  
  private ignoreList = ['UP', 'DOWN']
  
  private unassignedEmployees: EmployeeType[] = [
    {name: 'Jean-Luc Picard', selected: false},
    {name: 'Jordi LaForge', selected: false},
    {name: 'Dr. Crusher', selected: false},
    {name: 'Wesley Crusher', selected: false},
    {name: 'Data', selected: false},
    {name: 'Deanna Troi', selected: false}
  ]
  private currentEmployee: EmployeeType = {name: '', selected: false}
  private allRooms: HTMLElement[] = []
  private currentRoom: HTMLElement = document.createElement('div')

  private BUILDING = 'S'
  private FLOOR = '1'
  private desks: Array<Desk> = []
  private deskReservations: Array<DeskReservation> = []

  private emptyEmployee = {name: '', pk: -1}
  private selectedEmployee = this.emptyEmployee

  private selectedDeskNumber = ''
  
  // TODO: Use Quasar colors
  private primaryColor = '#1976d2'
  private greyColor = '#767676'
  private blackColor = '#000000'
  private redColor = 'red'

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

  private deselectAllRoomButtons() {
    Array.from(document.getElementsByClassName('desk-button') as HTMLCollectionOf<HTMLElement>).forEach(room => {
      if (!room.classList.contains('reserved')) {
        room.style.borderColor = this.greyColor
        room.style.color = this.blackColor
      }
    })
  }

  private roomClick(roomButton: HTMLElement, annotationElem: HTMLDivElement) {
    // TODO: Remove
    console.log(annotationElem)
    
    if (roomButton.dataset.pk) {
      const buttonNumber = roomButton.dataset.pk

      if (buttonNumber == this.selectedDeskNumber) {
        // Deselect the room
        this.selectedDeskNumber = ''
        roomButton.style.borderColor = this.greyColor
        roomButton.style.color = this.blackColor
      } else {
        // Select the room (and deselect others)
        this.selectedDeskNumber = buttonNumber
        this.deselectAllRoomButtons()
        roomButton.style.borderColor = this.primaryColor
        roomButton.style.color = this.primaryColor
      }
      
      


    }

    // if (roomButton.innerText == 'Unassigned') {
    //   if (this.currentEmployee.name) {
    //     // Assign the current employee to the room
    //     roomButton.innerText = this.currentEmployee.name
    //     const annotationSize = annotationElem.getBoundingClientRect()
    //     annotationElem.style.marginLeft = `-${annotationSize.width/2}px`
    //     annotationElem.style.marginTop = `-${annotationSize.height/2}px`
    //     // Remove the current employee from the list
    //     this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
    //     this.currentEmployee = {name: '', selected: false}
    //   } else {
    //     if (this.currentRoom == roomButton) {
    //       // Unhighlight the room
    //       this.currentRoom = document.createElement('div')
    //       roomButton.style.borderColor = this.greyColor
    //       roomButton.style.color = this.blackColor
    //     } else {
    //       // Highlight the room (and unhighlight others)
    //       this.allRooms.forEach((room) => {
    //         room.style.borderColor = this.greyColor
    //         room.style.color = this.blackColor
    //       })
    //       this.currentRoom = roomButton
    //       roomButton.style.borderColor = this.primaryColor
    //       roomButton.style.color = this.primaryColor
    //     }
    //   }
    // } else {
    //   if (this.currentEmployee.name) {
    //     // Swap the two employees
    //     // Move the room employee out
    //     this.unassignedEmployees.push({name: roomButton.innerText, selected: false})
    //     // Remove the current employee in
    //     roomButton.innerText = this.currentEmployee.name
    //     const annotationSize = annotationElem.getBoundingClientRect()
    //     annotationElem.style.marginLeft = `-${annotationSize.width/2}px`
    //     annotationElem.style.marginTop = `-${annotationSize.height/2}px`
    //     // Remove the current employee from the list
    //     this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
    //     this.currentEmployee = {name: '', selected: false}
    //   } else {
    //     // Kick out the room employee
    //     this.unassignedEmployees.push({name: roomButton.innerText, selected: false})
    //     roomButton.innerText = 'Unassigned'
    //     const annotationSize = annotationElem.getBoundingClientRect()
    //     annotationElem.style.marginLeft = `-${annotationSize.width/2}px`
    //     annotationElem.style.marginTop = `-${annotationSize.height/2}px`
    //   }
    // }
  }

  private clickReserve() {
    DeskReservationDataService.create({
      employee_pk: this.selectedEmployee.pk,
      building: this.BUILDING,
      floor: this.FLOOR,
      desk_number: this.selectedDeskNumber
    })
      .then((response: AxiosDeskReservationCreateServerResponse) => {
        Notify.create(`Reserved desk ${response.data.desk_number} for ${response.data.employee_name}`)
        this.selectedEmployee = this.emptyEmployee
        this.selectedDeskNumber = ''
        this.deselectAllRoomButtons()
        this.initDeskReservations()
          .then(() => {
            this.handleSVG()
          })
          .catch(e => {
            console.error('Error initializing desk reservations:', e)
          })
        // TODO: Update reserved desks list everywhere
      })
      .catch(e => {
        console.error('Error creating desk reservation:' ,e)
      })
  }

  private initDesksAndReservations() {
    return Promise.all([this.initDesks(), this.initDeskReservations()])
      .catch(e => {
        console.error('Error initializing desks and desk reservations from API:', e)
      })
  }

  private initDesks() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('deskReservationModule/getAllDesks', {building: this.BUILDING, floor: this.FLOOR})
        .then(() => {
          this.desks = this.getters['deskReservationModule/allDesks'].results
          resolve('Set desks')
        })
        .catch(e => {
          console.error('Error getting desks from API:', e)
          reject(e)
        })
    })
  }

  private initDeskReservations() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('deskReservationModule/getAllDeskReservations', {building: this.BUILDING, floor: this.FLOOR})
        .then(() => {
          this.deskReservations = this.getters['deskReservationModule/allDeskReservations'].results
          resolve(this.deskReservations)
        })
        .catch(e => {
          console.error('Error initializing desk reservations from API:', e)
          reject(e)
        })
    })
  }

  private handleSVG() {
    // Destroy any previously created annotation nodes
    const staleAnnotationNodes = Array.from(document.querySelectorAll('.annotation'))
    staleAnnotationNodes.forEach(node => { node.remove() })

    // Get horizontal and vertical offsets of svg floor plan
    const floorPlanNode = document.getElementsByClassName('floor-plan')[0]
    const floorPlanRect = floorPlanNode.getBoundingClientRect()

    const textNodes = Array.from(document.querySelectorAll('text'))

    textNodes
      .filter(it => /^\s*/.exec(it.innerHTML))
      .forEach(node => {
        const text = node.innerHTML
        
        // Ignore any text on the ignore list
        if (this.ignoreList.indexOf(text) != -1) {
          return
        }

        const matchingDesks = this.desks.filter((desk: Desk) => {
          return desk.building == this.BUILDING && desk.floor == this.FLOOR && desk.number == text
        })
        if (!matchingDesks.length) {
          // Hide any desk labels that shouldn't be displayed
          node.style.display = 'none'
          return
        }

        // Determine if desk is already reserved
        // TODO: Determine if desk is actually still reserved - right now just checking if it has EVER been reserved
        let deskReserved = false
        const reservations = this.deskReservations.filter((reservation: DeskReservation) => {
          return reservation.desk_building == this.BUILDING && reservation.desk_floor == this.FLOOR && reservation.desk_number == text
        })
        if (reservations.length) {
          // Hide any desk labels that shouldn't be displayed
          deskReserved = true
        }
      
        // Get the rectangle around the static map label
        const rect = node.getBoundingClientRect()

        // Create an annotation element to replace the static map label
        const annotationElem = document.createElement('div')
        annotationElem.className = 'annotation'
      
        annotationElem.innerHTML = `<button class="desk-button" data-pk="${text}">${text}</button>`
        
        // Position the annotation directly on top of the map label
        // annotationElem.style.left = (rect.left + rect.width/2 - 88).toString() + 'px'
        // annotationElem.style.top = (rect.top + rect.height/2 - 70).toString() + 'px'
        
        // TODO: Finish and annotate this - can't brain today
        annotationElem.style.left = (rect.left - floorPlanRect.left - rect.width/2 + annotationElem.offsetWidth/2).toString() + 'px'
        // TODO: Fix and annotate this - can't brain today
        annotationElem.style.top = (rect.top - floorPlanRect.top + 70).toString() + 'px'

        const clickableButton = annotationElem.querySelector('button') as HTMLElement
        this.allRooms.push(clickableButton)

        if (clickableButton) {
          if (deskReserved) {
            clickableButton.style.borderColor = this.redColor
            clickableButton.style.color = this.redColor
            clickableButton.classList.add('reserved')
          } else {
            clickableButton.addEventListener('click', e => { // eslint-disable-line @typescript-eslint/no-non-null-assertion
              const buttonElem = e.target as HTMLElement
              this.roomClick(buttonElem, annotationElem)
            })
          }
        }
        
        document.querySelector('#schaefers-1-page')?.appendChild(annotationElem)
        
        // const annotationSize = annotationElem.getBoundingClientRect()
        
        // annotationElem.style.marginLeft = `-${annotationSize.width/2}px`
        // annotationElem.style.marginTop = `-${annotationSize.height/2}px`

    })
  }

  private windowResizeEventHandler = this.handleSVG.bind(this)

  created() {
    window.addEventListener('resize', this.windowResizeEventHandler)
  }

  destroyed() {
    window.removeEventListener('resize', this.windowResizeEventHandler)
  }

  mounted() {
    this.initDesksAndReservations()
      .then(() => {
        this.handleSVG()
      })
      .catch(e => {
        console.error('Error initializing desk reservations in component:', e)
      })
    // this.initDesks()
    // this.initDeskReservations()
    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
    }
  }
}
</script>

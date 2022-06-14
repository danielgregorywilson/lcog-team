<template>
  <q-page class="q-mt-xs" id="schaefers-1-page">
    <div class="row justify-between items-center">
      <div class="row items-center">
        <q-icon name="help" color="primary" size="48px" class="q-mr-md cursor-pointer" @click="showHelp()" />
        <div class="row items-center q-gutter-md">
          <q-btn-group push class="">
            <q-btn push color="secondary" glossy label="1F" :to="{ name: 'schaefers-1' }" />
            <q-btn push color="primary" glossy label="2F" :to="{ name: 'schaefers-2' }" />
            <q-btn push color="primary" glossy label="3F" :to="{ name: 'schaefers-3' }"  />
          </q-btn-group>
        </div>
      </div>
      <q-select class="" v-model="selectedEmployee" :options="employees()" option-value="pk" option-label="name" label="Select your name" use-input hide-selected fill-input input-debounce="500" @filter="filterFn">
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
      <div class="row items-center q-gutter-md">
        <div class="row items-center q-gutter-sm">
          <div>Drop-In</div>
          <div id="drop-in-key">123</div>
        </div>
        <div class="row items-center q-gutter-sm">
          <div>Lead Drop-In</div>
          <div id="lead-drop-in-key">123</div>
        </div>
        <div class="row items-center q-gutter-sm">
          <div>Ergonomic Work Station</div>
          <q-img src="../../assets/floorPlans/desk-ergo.png" width=48px />
        </div>
        <div class="row items-center q-gutter-sm">
          <div>*held</div>
        </div>
      </div>
      <q-btn color="primary" :disabled="selectedEmployee.pk == -1 || selectedDeskNumber == ''" @click="clickReserve()">Reserve</q-btn>
    </div>
    
    <div class="row q-gutter-md q-mt-xs">
      <FloorPlan class="floor-plan"/>
    </div>

    <!-- Dialog to cancel a reservation -->
    <q-dialog v-model="cancelDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="no_meeting_room" color="primary" text-color="white" />
            <span class="q-ml-sm"><strong>{{ selectedDeskOccupantToCancel }}</strong> checked in to desk <strong>{{ selectedDeskNumberToCancel }}</strong> at <strong>{{ selectedDeskToCancelCheckInTime }}</strong>. End this reservation?</span>
          </div>
        </q-card-section>
        <q-card-actions class="row justify-around">
          <q-btn flat label="No" color="primary" v-close-popup />
          <q-btn flat label="Yes, end reservation" color="primary" @click="deleteReservation(selectedDeskReservationToCancelPk)" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog to confirm moving a reservation -->
    <q-dialog v-model="moveReservationDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="no_meeting_room" color="primary" text-color="white" />
            <span class="q-ml-sm"><strong>{{ selectedEmployee.name }}</strong> has a reservation at <span v-for="(reservation, index) in activeUserReservations" :key="reservation.pk"><span v-if="index != 0"> and </span>desk <strong>{{ reservation.desk_number }}</strong></span>. Cancel this existing reservation and make a new one?</span>
          </div>
        </q-card-section>
        <q-card-actions class="row justify-around">
          <q-btn flat label="No" color="primary" v-close-popup />
          <q-btn flat label="Yes, move reservation" color="primary" @click="moveReservation()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style lang="scss"> 
  #drop-in-key {
    width: 48px;
    height: 48px;
    background-color: yellow;
    border: 1px black solid;
    text-align: center;
  }
  
  #lead-drop-in-key {
    width: 48px;
    height: 48px;
    background-color: orange;
    border: 1px black solid;
    text-align: center;
  }
  
  .desk-ergo {
    width: 50px;
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
import { bus } from '../../App.vue'
import FloorPlan from '../../assets/floorPlans/schaefers1.fpsvg'
import DeskReservationDataService from '../../services/DeskReservationDataService'
import TrustedIPDataService from '../../services/TrustedIPDataService'
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
  
  private ignoreList = ['UP', 'DOWN', 'DN']
  
  private standardDesk = require('../../assets/floorPlans/desk-standard.png') as string // eslint-disable-line @typescript-eslint/no-var-requires
  private ergoDesk = require('../../assets/floorPlans/desk-ergo.png') as string // eslint-disable-line @typescript-eslint/no-var-requires

  private BUILDING = 'S'
  private FLOOR = '1'
  private desks: Array<Desk> = []
  private deskReservations: Array<DeskReservation> = []

  private emptyEmployee = {name: '', pk: -1}
  
  private moveReservationDialogVisible = false
  private activeUserReservations: Array<DeskReservation> = []
  private selectedEmployee = this.emptyEmployee
  private selectedDeskNumber = ''
  
  private cancelDialogVisible = false
  private selectedDeskReservationToCancelPk = -1
  private selectedDeskNumberToCancel = ''
  private selectedDeskOccupantToCancel = ''
  private selectedDeskToCancelCheckInTime = ''
  
  // TODO: Use Quasar colors
  private primaryColor = '#1976d2'
  private greyColor = '#767676'
  private blackColor = '#000000'
  private redColor = 'red'
  private yellowColor = 'yellow'
  private orangeColor = 'orange'

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

  private roomClick(roomButton: HTMLElement) {
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
  }

  private reservedRoomClick(roomButton: HTMLElement) {
    if (roomButton.dataset.pk) {
      const buttonNumber = roomButton.dataset.pk
      this.selectedDeskNumberToCancel = buttonNumber
      const currentDeskReservation = this.deskReservations.filter(deskReservation => deskReservation.desk_number == buttonNumber)[0]
      this.selectedDeskReservationToCancelPk = currentDeskReservation.pk
      this.selectedDeskOccupantToCancel = currentDeskReservation.employee_name
      const checkInDate = new Date(currentDeskReservation.check_in)
      this.selectedDeskToCancelCheckInTime = checkInDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })

      // Open reservation cancel dialog
      this.cancelDialogVisible = true
    }
  }

  private deleteReservation(pk: number) {
    DeskReservationDataService.cancelReservation(pk) 
      .then(() => {
        if (this.selectedDeskNumberToCancel) {
          Notify.create({message: `Canceled reservation of desk ${this.selectedDeskNumberToCancel} for ${this.selectedDeskOccupantToCancel}`})
        }
        this.selectedDeskReservationToCancelPk = -1
        this.selectedDeskNumberToCancel = ''
        this.selectedDeskOccupantToCancel = ''

        // TODO: Temporarily restoring to remove sockets for production
        this.initDeskReservations()
          .then(() => {
            this.handleSVG()
          })
          .catch(e => {
            console.error('Error initializing desk reservations:', e)
          })
        
        // Update reserved desks list everywhere with WebSocket
        // this.deskReservationSocket.send(
        //   JSON.stringify({
        //     'message': `Reserved desk ${response.data.desk_number} for ${response.data.employee_name}`
        //   })
        // );
      })
      .catch(e => {
        console.error('Error cancelling desk reservation:' ,e)
      })
  }

  private clickReserve() {
    // Before we reserve the desk, ensure the user does not have any active reservations. If so, offer to move them
    const activeUserReservations = this.deskReservations.filter(desk => desk.employee_pk == this.selectedEmployee.pk)
    if (activeUserReservations.length) {
      this.activeUserReservations = activeUserReservations
      this.moveReservationDialogVisible = true
    } else {
      this.reserveDesk()
    }
  }

  private moveReservation() {
    // Cancel all existing reservations and make the new one.
    for (let i=0; i<this.activeUserReservations.length; i++) {
      this.deleteReservation(this.activeUserReservations[i].pk)
    }
    this.reserveDesk()
  }

  private reserveDesk() {
    DeskReservationDataService.create({
      employee_pk: this.selectedEmployee.pk,
      building: this.BUILDING,
      floor: this.FLOOR,
      desk_number: this.selectedDeskNumber
    })
      .then((response: AxiosDeskReservationCreateServerResponse) => {
        this.selectedEmployee = this.emptyEmployee
        this.selectedDeskNumber = ''
        this.deselectAllRoomButtons()
        if (response.data.created) {
          Notify.create(`Reserved desk ${response.data.desk_number} for ${response.data.employee_name}`)  
        } else {
          if (response.data.desk_held) {
            Notify.create({message: `Sorry! Desk ${response.data.desk_number} is held today. Please choose another`, type: 'negative'})
          } else {
            Notify.create({message: `Sorry! Desk ${response.data.desk_number} is already reserved for ${response.data.employee_name}. Please choose another`, type: 'negative'})
          }
        }
        
        // TODO: Temporarily restoring to remove sockets for production
        this.initDeskReservations()
          .then(() => {
            this.handleSVG()
          })
          .catch(e => {
            console.error('Error initializing desk reservations:', e)
          })
        
        // Update reserved desks list everywhere with WebSocket
        // this.deskReservationSocket.send(
        //   JSON.stringify({
        //     'message': `Reserved desk ${response.data.desk_number} for ${response.data.employee_name}`
        //   })
        // );
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
        if (!node.firstElementChild) {
          return
        }
        const text = node.firstElementChild.innerHTML
        
        // Ignore any text on the ignore list
        if (this.ignoreList.indexOf(text) != -1) {
          return
        }

        const matchingDesks = this.desks.filter((desk: Desk) => {
          let number = ''
          if (['A', 'B'].indexOf(desk.number.slice(-1)) == -1) {
            number = desk.number
          } else {
            number = desk.number.substring(0, desk.number.length-1)
            desk.letter = desk.number.slice(-1)
          }
          return desk.building == this.BUILDING && desk.floor == this.FLOOR && number == text
        })
        if (!matchingDesks.length) {
          // Hide any desk labels that shouldn't be displayed
          node.style.display = 'none'
          return
        }

        for (let desk of matchingDesks) {
          
          // Determine if desk is already reserved
          let deskReserved = false
          const reservations = this.deskReservations.filter((reservation: DeskReservation) => {
            return reservation.desk_building == this.BUILDING && reservation.desk_floor == this.FLOOR && reservation.desk_number == desk.number
          })
          if (reservations.length) {
            // Hide any desk labels that shouldn't be displayed
            deskReserved = true
          }

          // const desk  = this.desks.filter((desk: Desk) => {
          //   return desk.building == this.BUILDING && desk.floor == this.FLOOR && desk.number == text
          // })[0]

          // Determine if the desk is ergo and/or lead
          // Use correct icon based on ergonomic or not
          const deskLogo = desk.ergonomic ? this.ergoDesk : this.standardDesk
          const deskLead = desk.lead

          // Determine if the desk has a hold on it today
          const heldTodayText = desk.held_today ? '*' : ''
        
          // Get the rectangle around the static map label
          const rect = node.getBoundingClientRect()

          // Create an annotation element to replace the static map label
          const annotationElem = document.createElement('div')
          annotationElem.className = 'annotation'
        
          annotationElem.innerHTML = `<button class="desk-button" data-pk="${desk.number}"><div>${desk.number}${heldTodayText}</div><img class="desk-ergo" src="${ deskLogo }" /></button>`
          
          // Position the annotation directly on top of the map label
          // annotationElem.style.left = (rect.left + rect.width/2 - 88).toString() + 'px'
          // annotationElem.style.top = (rect.top + rect.height/2 - 70).toString() + 'px'
          
          // On narrower screens, the header takes up 2-4 rows, so we need to nudge the buttons down to match.
          var singleRowHeaderSpace = 56
          var rowsHeaderSpace = 56
          if (window.innerWidth < 514) {
            // If width less than 514px, there are 4 tall rows of header
            rowsHeaderSpace = 220
          } else if (window.innerWidth < 570) {
            // If width less than 570px, there are 4 short rows of header
            rowsHeaderSpace = 193
          } else if (window.innerWidth < 661) {
            // If width less than 661px, there are 3 rows of header
            rowsHeaderSpace = 148
          } else if (window.innerWidth < 959) {
            // If width less that 959px, there are 2 tall rows of header
            rowsHeaderSpace = 112
          } else if (window.innerWidth < 1050) {
            // If width less that 1050px, there are 2 short rows of header
            rowsHeaderSpace = 92
          }
          var extraHeaderSpace = rowsHeaderSpace - singleRowHeaderSpace

          // Adjust A and B desks so they both show up
          let deskSplitHorizontalAdjustment = 0
          if (desk.letter) {
            if (desk.letter == 'A') {
              deskSplitHorizontalAdjustment = -34
            } else {
              deskSplitHorizontalAdjustment = 34
            }
          }

          // TODO: Finish and annotate this - can't brain today
          annotationElem.style.left = (rect.left - floorPlanRect.left - rect.width/2 + annotationElem.offsetWidth/2 - 12 + deskSplitHorizontalAdjustment).toString() + 'px'
          // TODO: Fix and annotate this - can't brain today
          annotationElem.style.top = (rect.top - floorPlanRect.top + 48 + extraHeaderSpace).toString() + 'px'

          const clickableButton = annotationElem.querySelector('button') as HTMLElement

          if (clickableButton) {
            if (deskReserved) {
              clickableButton.style.borderColor = this.redColor
              clickableButton.classList.add('reserved')
              clickableButton.addEventListener('click', e => { // eslint-disable-line @typescript-eslint/no-non-null-assertion
                const target = e.target as HTMLElement
                const buttonElem = target.closest('button')
                if (buttonElem) {
                  this.reservedRoomClick(buttonElem)
                }
              })
            } else {
              if (deskLead) {
                clickableButton.style.backgroundColor = this.orangeColor
              } else {
                clickableButton.style.backgroundColor = this.yellowColor
              }
              clickableButton.addEventListener('click', e => { // eslint-disable-line @typescript-eslint/no-non-null-assertion
                const target = e.target as HTMLElement
                const buttonElem = target.closest('button')
                if (buttonElem) {
                  this.roomClick(buttonElem)
                }
              })
            }
          }
          
          document.querySelector('#schaefers-1-page')?.appendChild(annotationElem)
          
          // const annotationSize = annotationElem.getBoundingClientRect()
          
          // annotationElem.style.marginLeft = `-${annotationSize.width/2}px`
          // annotationElem.style.marginTop = `-${annotationSize.height/2}px`
        }
    })
  }

  private windowResizeEventHandler = this.handleSVG.bind(this)

  // WebSocket magic for sharing reservation changes
  private webSocketUrl = process.env.WEBSOCKET_URL ? process.env.WEBSOCKET_URL : 'ws://api.team.lcog.org/'
  // private deskReservationSocket = new WebSocket(
  //   `${ this.webSocketUrl }ws/desk-reservation/${ this.BUILDING }/${ this.FLOOR }/`
  // )

  private showHelp() {
    bus.$emit('showReservationHelpDialog') // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  created() {
    window.addEventListener('resize', this.windowResizeEventHandler)
  }

  destroyed() {
    window.removeEventListener('resize', this.windowResizeEventHandler)
  }

  mounted() {
    // When a WebSocket message is received
    // this.deskReservationSocket.onmessage = (socketMessageObj) => {
    //   const socketMessageData = JSON.parse(socketMessageObj.data) // eslint-disable-line @typescript-eslint/no-unsafe-assignment
    //   const updateMessage = socketMessageData.message // eslint-disable-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    //   this.initDeskReservations()
    //     .then(() => {
    //       this.handleSVG()
    //       Notify.create(updateMessage)
    //     })
    //     .catch(e => {
    //       console.error('Error initializing desk reservations from socket message:', e)
    //     })
    // }

    // We do not expect the socket to ever close
    // this.deskReservationSocket.onclose = () => {
    //   console.error('Desk Reservation socket closed unexpectedly');
    // };

    // Boot session to dashboard if not authenticated or IP not in trusted IP lists
    const isAuthenticated = this.getters['authModule/isAuthenticated']
    if (!isAuthenticated) {
      TrustedIPDataService.getTrustedIPs()
        .then((response: {data: boolean}) => {
          const addressIsSafe = response.data
          if (!addressIsSafe) {
            this.$router.push('/')
              .catch((e) => {
                console.error('Error navigating to dashboard upon rejecting connection to desk reservations:', e)
              })
          }
        })
        .catch(e => {
          console.error('Error getting safe IP address status from API:', e)
        })
    }
    
    this.initDesksAndReservations()
      .then(() => {
        this.handleSVG()
      })
      .catch(e => {
        console.error('Error initializing desk reservations in component:', e)
      })

    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
    }
  }
}
</script>

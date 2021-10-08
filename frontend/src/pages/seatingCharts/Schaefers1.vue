<template>
  <q-page class="row items-center justify-evenly">
    <!-- <img :src="floorPlan()" class="floor-plan" /> -->
    <!-- <div v-html="floorPlan()" /> -->
    <!-- <q-img
      class="floor-plan"
      src="../../assets/floorPlans/schaefers1.svg"
    /> -->
    <div class="row q-gutter-md">
      <div class="col">
        <div>Unassigned Employees</div>
        <q-btn v-for="employee in unassignedEmployees" :key="employee.name" :color="employee.selected ? 'primary' : 'white'" @click="unassignedEmployeeClick(employee)" text-color="black" :label="employee.name" />
      </div>
      <FloorPlan class="floor-plan"/>
    </div>
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
      width: 1000px;
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
import { Component, Vue } from 'vue-property-decorator'
import FloorPlan from '../../assets/floorPlans/schaefers1.svg';

interface EmployeeType {
  name: string
  selected: boolean
}

@Component({
  components: { FloorPlan }
})
export default class Schaefers1 extends Vue{
  // private floorPlan() {         
  //   let plan = require('../../assets/floorPlans/schaefers1.svg') // eslint-disable-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-var-requires
  //   debugger
  //   return plan // eslint-disable-line @typescript-eslint/no-unsafe-return
  // }

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
  private currentRoom: HTMLElement = document.createElement('div')
  private currentAnnotationElem: HTMLDivElement = document.createElement('div')
  private currentannotationSize: DOMRect = document.createElement('div').getBoundingClientRect()
  
  // TODO: Use Quasar colors
  private primaryColor = '#1976d2'
  private greyColor = '#767676'
  private blackColor = '#000000'

  private unassignedEmployeeClick(employee: EmployeeType) {
    if (employee.selected) {
      employee.selected = false
      this.currentEmployee = {name: '', selected: false}
    } else {
      if (this.currentRoom.innerText) {
      // TODO
      //   if (this.currentRoom.innerText == 'Unassigned') {
      //     // Assign the employee to the current room
      //     this.currentRoom.innerText = employee.name;
      //     const annotationSize = annotationElem.getBoundingClientRect();
      //     annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
      //     annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
      //     // Remove the current employee from the list
      //     this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
      //     this.currentEmployee = {name: '', selected: false}
      //   } else {
      //     // Swap the two employees
      //     // Move the room employee out
      //     this.unassignedEmployees.push({name: roomButton.innerText, selected: false})
      //     // Remove the current employee in
      //     roomButton.innerText = this.currentEmployee.name;
      //     const annotationSize = annotationElem.getBoundingClientRect();
      //     annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
      //     annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
      //     // Remove the current employee from the list
      //     this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
      //     this.currentEmployee = {name: '', selected: false}
      //   }
        
        
        
      } else {
        // Select this employee (and deselect others)
        this.unassignedEmployees.forEach((employee) => {employee.selected = false})
        employee.selected = true
        this.currentEmployee = employee
      }
      
    }
  }

  private roomClick(roomButton: HTMLElement, annotationElem: HTMLDivElement, annotationSize: DOMRect) {
    if (roomButton.innerText == 'Unassigned') {
      if (this.currentEmployee.name) {
        // Assign the current employee to the room
        roomButton.innerText = this.currentEmployee.name;
        const annotationSize = annotationElem.getBoundingClientRect();
        annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
        annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
        // Remove the current employee from the list
        this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
        this.currentEmployee = {name: '', selected: false}
      } else {
        if (this.currentRoom == roomButton) {
          // Unhighlight the room
          this.currentRoom = document.createElement('div')
          roomButton.style.borderColor = this.greyColor
          roomButton.style.color = this.blackColor
        } else {
          // Highlight the room
          this.currentRoom = roomButton
          roomButton.style.borderColor = this.primaryColor
          roomButton.style.color = this.primaryColor
        }
      }
    } else {
      if (this.currentEmployee.name) {
        // Swap the two employees
        // Move the room employee out
        this.unassignedEmployees.push({name: roomButton.innerText, selected: false})
        // Remove the current employee in
        roomButton.innerText = this.currentEmployee.name;
        const annotationSize = annotationElem.getBoundingClientRect();
        annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
        annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
        // Remove the current employee from the list
        this.unassignedEmployees.splice(this.unassignedEmployees.indexOf(this.currentEmployee), 1)
        this.currentEmployee = {name: '', selected: false}
      } else {
        // Kick out the room employee
        this.unassignedEmployees.push({name: roomButton.innerText, selected: false})
        roomButton.innerText = 'Unassigned'
        const annotationSize = annotationElem.getBoundingClientRect();
        annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
        annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
      }
    }
  }

  private handleSVG() {
    // Destroy any previously created annotation nodes
    const staleAnnotationNodes = Array.from(document.querySelectorAll('.annotation'));
    staleAnnotationNodes.forEach(node => { node.remove() })

    const textNodes = Array.from(document.querySelectorAll('text'));

    textNodes
      .filter(it => it.innerHTML.match(/^\s*/))
      .forEach(node => {
        const text = node.innerHTML;
        console.log(text)
        if (this.ignoreList.indexOf(text) != -1) {
          return
        }
      
        node.style.display = 'hidden';
      
        const rect = node.getBoundingClientRect();

        const annotationElem = document.createElement('div');
        annotationElem.className = 'annotation';
      
        annotationElem.style.left = (rect.left + rect.width/2).toString() + 'px';
        annotationElem.style.top = (rect.top + rect.height/2).toString() + 'px';

        annotationElem.innerHTML = `<div>${text}</div><button>Unassigned</button>`;

        const clickableButton = annotationElem.querySelector('button') as HTMLElement
        if (clickableButton) {
          clickableButton.addEventListener('click', e => { // eslint-disable-line @typescript-eslint/no-non-null-assertion
            const buttonElem = e.target as HTMLElement
            this.roomClick(buttonElem, annotationElem, annotationSize)

            // for (let name = ''; name != buttonElem.innerText; name = [
            //   'Jean-Luc Picard',
            //   'Jordi LaForge',
            //   'Dr. Crusher',
            //   'Wesley Crusher',
            //   'Data',
            //   'Deanna Troi',
            // ][(Math.random() * 6) | 0]) {
            //   buttonElem.innerText = name;
              
            //   const annotationSize = annotationElem.getBoundingClientRect();
            //   annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
            //   annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
            // }
          })
        }
        
        document.body.appendChild(annotationElem);
        
        const annotationSize = annotationElem.getBoundingClientRect();
        
        annotationElem.style.marginLeft = `-${annotationSize.width/2}px`;
        annotationElem.style.marginTop = `-${annotationSize.height/2}px`;
    });
  }

  private windowResizeEventHandler() {
    this.handleSVG()
  }

  created() {
    window.addEventListener('resize', this.windowResizeEventHandler);
  }

  destroyed() {
    window.removeEventListener('resize', this.windowResizeEventHandler);
  }

  mounted() {
    this.handleSVG();
  }
}
</script>

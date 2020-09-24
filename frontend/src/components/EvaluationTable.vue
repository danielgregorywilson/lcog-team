<template>
  <div class="q-py-sm">
    <q-table
      :data="performanceReviews"
      :columns="columns"
      row-key="name"
    >
      <template v-slot:body-cell-dateOfReview="props">
        <q-td key="dateOfReview" :props="props">
          {{ props.row.date_of_review | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-status="props">
        <q-td key="status" class="td-status" :props="props">
          {{ props.row.status }}
        </q-td>
      </template>
      <template v-slot:body-cell-dateOfDiscussion="props">
        <q-td key="dateOfDiscussion" :props="props" >
          {{ props.row.date_of_discussion | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-discussionTookPlace="props">
        <q-td key="discussionTookPlace" :props="props">
          <!-- <q-btn v-if="props.row.discussion_took_place=='No'" color="white" text-color="black" label="Mark as Discussed" /> -->
          {{ props.row.discussion_took_place }}
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props" :class="{ 'wide-actions' : props.row.discussion_took_place == 'No'}">
          <div class="row">
            <q-btn class="col" dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
            <q-btn class="col" v-if="props.row.discussion_took_place=='No'" color="white" text-color="black" label="Mark as Discussed" @click="managerMarkDiscussed(props)" />
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<style scoped>
.q-table tbody td.td-status {
    min-width: 135px;
    white-space: normal;
}
.q-table tbody td.wide-actions {
    min-width: 200px;
    white-space: normal;
}
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { AxiosPerformanceReviewManagerMarkDiscussedServerResponse, AxiosPerformanceReviewRetrieveManyServerResponse } from '../store/types'
import { bus } from '../App.vue'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService';
import { PerformanceReviewRetrieve } from '../store/types'
import '../filters'

interface EvaluationColumn {
  name: string;
  required?: boolean;
  label: string;
  align?: string;
  field?: string;
  sortable?: boolean;
  style?: string;
  headerStyle?: string;
}

interface QuasarEvaluationTableRowClickActionProps {
  evt: MouseEvent;
  row: PerformanceReviewRetrieve;
}

@Component
export default class EvaluationTable extends Vue {
  @Prop({required: true}) readonly actionRequired!: boolean
  private performanceReviews: Array<PerformanceReviewRetrieve> = []
  private columns: Array<EvaluationColumn> = [
    { name: 'employeeName', required: true, label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
    { name: 'daysUntilReview', label: 'Days Until Review', field: 'days_until_review', sortable: true },
    { name: 'status', label: 'Status', field: 'status' },
    { name: 'dateOfDiscussion', label: 'Date of Discussion', field: 'date_of_discussion' },
    { name: 'discussionTookPlace', label: 'Discussion took place', field: 'discussion_took_place', align: 'left' },
    { name: 'actions', label: 'Actions', align: 'around', },
  ]

  private retrievePerformanceReviews(): void {
    if (this.actionRequired) {
      PerformanceReviewDataService.getAllManagerUpcomingActionRequired()
        .then((response: AxiosPerformanceReviewRetrieveManyServerResponse) => {
          this.performanceReviews = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    } else {
      PerformanceReviewDataService.getAllManagerUpcomingNoActionRequired()
        .then((response: AxiosPerformanceReviewRetrieveManyServerResponse) => {
          this.performanceReviews = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }

  private editEvaluation(props: QuasarEvaluationTableRowClickActionProps): void {
    this.$router.push(`pr/${ props.row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  private managerMarkDiscussed(props: QuasarEvaluationTableRowClickActionProps): void {
    PerformanceReviewDataService.managerMarkDiscussed(props.row.pk)
      .then((response: AxiosPerformanceReviewManagerMarkDiscussedServerResponse) => {
        console.log(response.data.status)
        bus.$emit('updateEvaluationTables', 'updated table') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      })
      .catch(e => {
        console.log(e)
      })
  }

  created() {
    bus.$on('updateEvaluationTables', (data: string) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      console.log(data)
      this.retrievePerformanceReviews()
    })
  }

  mounted() {
    this.retrievePerformanceReviews();
  }
}
</script>

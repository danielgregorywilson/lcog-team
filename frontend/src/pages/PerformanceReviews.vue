<template>
  <q-page class="q-pa-md">
    <div class="q-py-md">
      <div class="text-h4">Your Next Review</div>
      <div class="text-body1">You do not have a scheduled upcoming review</div>
    </div>
    <div class="q-py-md" v-if="profile.is_manager">
      <div class="row items-center q-mb-md">
        <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Review Notes</div>
      </div>
      <review-note-table />
    </div>
    <div class="q-py-md" v-if="profile.is_manager">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Current Evaluations (For Managers)</div>
      </div>
      <div class="text-h6">Action Required</div>
        <evaluation-table :actionRequired="true" />
      <div class="text-h6">No Action Required</div>
        <evaluation-table :actionRequired="false" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ReviewNoteTable from '../components/ReviewNoteTable.vue';
import EvaluationTable from '../components/EvaluationTable.vue';
import { UserRetrieve } from '../store/types';

@Component({
  components: { EvaluationTable, ReviewNoteTable }
})
export default class PerformanceReviews extends Vue {
  private currentIndex = -1;
  private title = '';
  private profile: UserRetrieve = {url: new URL('http://www.example.com'), username: '', email: '', name: '', groups: '', is_staff: false, is_manager: false, is_upper_manager: false}

  private getProfile(): void {
    if (this.$store.getters['userModule/isProfileLoaded']) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access
      this.profile = this.$store.getters['userModule/getEmployeeProfile'] // eslint-disable-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    } else {
      this.$store.dispatch('userModule/userRequest')
        .then(() => {
          this.profile = this.$store.getters['userModule/getEmployeeProfile'] // eslint-disable-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        })
        .catch(e => {
          console.log(e)
        })
    }
  }

  mounted() {
    this.getProfile();
  }
};
</script>

<template>
<div class="q-mt-md">
  <div class="text-h5 q-mb-sm">Credit Card Expenses</div>
  
  <div class="row q-gutter-sm q-mb-lg">
    <a href="#submitters">Submitters</a>
    <a href="#approvers">Approvers</a>
    <a href="#directors">Directors</a>
    <a href="#fiscal">Fiscal</a>
  </div>

  <hr />

  <div class="anchor" id="submitters"></div>
  <div class="text-h6">Submitters</div>
  <img src="../../assets/docs/cc-expenses/submitter.png" alt="Submitter view" />
  <p>You have three tasks here:</p>
  <ol>
    <li>Enter expenses as you make them! Click the “+ New Expense” button on the table. You should get feedback (shown) to correct errors where information is missing or incorrect.</li>
    <li>To begin, there will be no uploaded statements. At the end of each month, fiscal will upload a statement. You will need to come back and select the correct one and ensure the expenses match.</li>
    <li>Submit your expenses! Once the above two things are done, you can submit everything for review by the appropriate approvers.</li>
    <li>BONUS! If anyone in the approval chain rejects an expense, you will need to correct it or provide an explanation and resubmit.</li>
  </ol>

  <hr />

  <div class="anchor" id="approvers"></div>
  <div class="text-h6">Approvers</div>
  <img src="../../assets/docs/cc-expenses/approver.png" alt="Approver view" />
  <p>You have one task:</p>
  <ol>
    <li>Approve or Reject expenses! These have been assigned to you by the submitter. Review the details and either select approve or deny (with a note explaining why). Note that you may have to re-approve expenses that are changed if, say, fiscal rejects them back to the submitter.</li>
  </ol>

  <hr />

  <div class="anchor" id="directors"></div>
  <div class="text-h6">Directors</div>
  <img src="../../assets/docs/cc-expenses/director-1.png" alt="Director list view" />
  <img src="../../assets/docs/cc-expenses/director-2.png" alt="Director detail view" />
  <p>You have one task:</p>
  <ol>
    <li>Approve or Reject the month! You will see all the cards assigned to you for review. Note that there may be multiple people submitting for the same card!</li>
  </ol>

  <hr />

  <div class="anchor" id="fiscal"></div>
  <div class="text-h6">Fiscal</div>
  <img src="../../assets/docs/cc-expenses/fiscal-1.png" alt="Fiscal list view" />
  <img src="../../assets/docs/cc-expenses/fiscal-2.png" alt="Fiscal detail view" />
  <p>You have two tasks:</p>
  <ol>
    <li>At the end of the month, upload bank statements for each credit card. You can do this on the first screen at the bottom.</li>
    <li>After expenses are submitted (you can see the status in the table), approve or deny the month. Note that there may be multiple people submitting for the same card!</li>
    <li>BONUS! You can print out all the info for a statement (with statement, employee-entered info, and receipts) with the button on the second screen.</li>
  </ol>
</div>
</template>

<style scoped lang="scss">
img {
  width: 100%;
  margin-bottom: 20px;
}

.anchor {
  position: absolute;
  margin-top: -50px
}
</style>

<script setup lang="ts">
</script>

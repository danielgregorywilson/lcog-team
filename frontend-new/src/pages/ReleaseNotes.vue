<!-- From https://github.com/cstlaurent/vue-release-notes -->

<template>
<q-page>
  <div class="q-ma-sm">
    <div class="text-h4 text-center">Release Notes</div>
    <div class="_release-notes">
      <div class="_release" v-for="release in releaseData" :key="release.version">
        <div class="_release-header" v-if="showType(release.type)">
          <div class="_release-version">{{release.version}}</div>
          <div class="_release-date">{{release.date.toDateString()}}</div>
        </div>
        <div class="_changes-list" v-if="showType(release.type)">
          <div class="_change" v-for="(change, index) in release.changes" :key="index">
            <div class="_change-type" v-bind:class="tagColor(change.type)">{{change.type}}</div>
            <div class="_change-descripton" v-html="change.description"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</q-page>
</template>

<style lang="scss">
$break-small: 768px;

._release-notes {
  ._release {
    margin: 1em 0 2em 0;
    ._release-header {
      display: flex;
      align-items: center;
      ._release-date {
        margin: 0 0 5px 0.5em;
        font-size: 200%;
        font-weight: 300;
        @media screen and (max-width: $break-small) {
          font-size: 170%;
          margin: 0 0 5px 0.3em;
        }
      }
      ._release-version {
        background-color: #ce93d8;
        width: 65px;
        border-radius: 5px;
        text-align: center;
        padding-top: 4px;
        padding-bottom: 4px;
        margin-bottom: 3px;
        font-weight: 500;
      }
    }
    ._changes-list {
      margin-left: 80px;
      margin-top: 0.5em;
      list-style: none;
      transition: all 0.2s ease;
      @media screen and (max-width: $break-small) {
        margin-left: 0px;
        margin-top: 0px;
        padding-left: 0px;
      }
      ._change {
        display: flex;
        align-items: top;
        margin-bottom: 0.5em;
        ._change-type {        
          border-radius: 5px;
          text-align: center;
          width: 65px;
          text-transform: uppercase;
          font-size: 60%;
          font-weight: 500;
          padding-top: 2px;
          padding-bottom: 2px;
          margin-top: 2px;
          margin-right: 1em;
          margin-bottom: auto;          
          &._green {
            background-color: #a5d6a7;
          }
          &._blue {
            background-color: #90caf9;
          }
          &._orange {
            background-color: #ffab91;
          }
        }
        ._change-description {
          flex: 1;
          text-align: left;
        }
      }
    }
  }
}
</style>

<script setup lang="ts">
import { releases } from '../releaseNotes'

interface Release {
  version: string
  date: Date
  type: string
  changes: {
    type: string
    description: string
  }[]
}

const colorMap = new Map([
  ['new', '_green'],
  ['fix', '_orange']
])
const hiddenTypes = ['v-next']
const releaseData: Release[] = releases as Release[]

function tagColor (changeType: string) {
  if (colorMap.has(changeType)) {
    return colorMap.get(changeType)
  } else {
    return '_blue'
  }
}
function showType (type: string) {
  return !hiddenTypes.includes(type)
}

</script>

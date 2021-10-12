// https://github.com/visualfanatic/vue-svg-loader/blob/master/docs/faq.md#how-to-use-this-loader-with-typescript

// Handle '.fpsvg' files that represent floor plan svgs
declare module '*.fpsvg' {
  import Vue, {VueConstructor} from 'vue';
  const content: VueConstructor<Vue>;
  export default content;
}
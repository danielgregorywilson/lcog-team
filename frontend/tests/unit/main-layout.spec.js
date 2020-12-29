import MainLayout from "@/layouts/MainLayout.vue"
import { shallowMount } from "@vue/test-utils";

describe("MainLayout.vue", () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallowMount(MainLayout, {
      methods: { getCurrentUser: () => {}}
    })
  })

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  })
})

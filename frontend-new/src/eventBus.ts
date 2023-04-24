import { ref } from 'vue'
const bus = ref(new Map())

export default function useEventBus(){

    function emit(event: string, object: any) {
        bus.value.set(event, object)
    }

    return {
        emit,
        bus
    }
}
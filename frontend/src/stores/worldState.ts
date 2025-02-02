import { ref, provide, inject, type InjectionKey } from 'vue'

export interface WorldState {
  matrix: number[][]
  current_message: string
}

export const WorldStateSymbol: InjectionKey<{
  state: WorldState
  updateState: (newState: WorldState) => void
}> = Symbol('WorldState')

export function createWorldState() {
  // Dummy data: 5x5 matrix representing a simple graph
  const dummyMatrix = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1],
    [0, 0, 1, 1, 0]
  ]

  const state = ref<WorldState>({
    matrix: dummyMatrix,
    current_message: 'Test message'
  })

  const updateState = (newState: WorldState) => {
    state.value = newState
  }

  provide(WorldStateSymbol, {
    state: state.value,
    updateState
  })
}

export function useWorldState() {
  const context = inject(WorldStateSymbol)
  if (!context) {
    throw new Error('useWorldState must be used within a provider')
  }
  return context
} 
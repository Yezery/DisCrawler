import type { DirectiveBinding } from 'vue'

interface ElType extends HTMLElement {
  loadingElement: HTMLDivElement
  isloading: boolean
}

export default {
  mounted(el: ElType, binding: DirectiveBinding) {
    const loadingElement = document.createElement('div')
    const loadingSpinner = document.createElement('div')
    loadingElement.className = 'loading-overlay ' // Add spinner class
    loadingElement.style.display = 'none'
    loadingSpinner.className = 'spinner ' // Add spinner class
    loadingElement.appendChild(loadingSpinner)
    el.style.position = 'relative'
    el.isloading = binding.value
    el.loadingElement = loadingElement
    el.appendChild(loadingElement)
  },
  updated(el: ElType, binding: DirectiveBinding) {
    if (el.loadingElement) {
      el.loadingElement.style.display = binding.value ? 'flex' : 'none'
      el.isloading = binding.value
    }
  },
  beforeUnmount(el: ElType) {
    if (el.loadingElement) {
      el.removeChild(el.loadingElement)
    }
  },
}

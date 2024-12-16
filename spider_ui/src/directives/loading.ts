import { applyStyles } from '@/utils/convent'
import type { DirectiveBinding } from 'vue'

interface ElType extends HTMLElement {
  loadingElement?: HTMLDivElement
  isloading: boolean
}

const css = `{
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}`

export default {
  mounted(el: ElType, binding: DirectiveBinding) {
    const loadingElement = document.createElement('div')
    const loadingSpinner = document.createElement('span')
    loadingElement.style.display = 'none'
    loadingSpinner.className = 'loading loading-bars loading-lg'
    el.style.position = 'relative'
    applyStyles(loadingElement, css)
    loadingElement.appendChild(loadingSpinner)
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
  // beforeUnmount(el: ElType) {
  //   if (el.loadingElement) {
  //     el.removeChild(el.loadingElement)
  //   }
  // },
}

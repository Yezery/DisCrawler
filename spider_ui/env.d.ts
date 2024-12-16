/// <reference types="vite/client" />
declare module '@/assets/cityPostion.js' {
  export function getCityPositionByName(name: string): CityPosition
}

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent
  export default component
}

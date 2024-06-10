import React from 'react'
import { SecondaryLightBtn } from '../components'

const Reptile = () => {
  return (
    <div className='page'>
      <h1>Reptile</h1>
      <p className='page__desc'>A software tool designed to clean up survey records. Focuses on fixing data errors reported by users</p>
      <div>
        <SecondaryLightBtn>Ethiopia Reptile →</SecondaryLightBtn>
        <SecondaryLightBtn>Nigeria Reptile →</SecondaryLightBtn>
      </div>
    </div>
  )
}

export default Reptile

import React from 'react'

const SecondaryLightBtn = ({children, onClick}) => {
  return (
    <button className='btn_secondary_light' onClick={onClick}>
      {children}
    </button>
  )
}

export default SecondaryLightBtn
import React from 'react'

const SecondaryDarkBtn = ({children, onClick}) => {
  return (
    <button className='btn_secondary_dark' onClick={onClick}>
      {children}
    </button>
  )
}

export default SecondaryDarkBtn
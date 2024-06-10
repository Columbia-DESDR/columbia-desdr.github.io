import React from 'react'

const PrimaryBtn = ({children, onClick}) => {
  return (
    <button className='btn_primary' onClick={onClick}>
      {children}
    </button>
  )
}

export default PrimaryBtn

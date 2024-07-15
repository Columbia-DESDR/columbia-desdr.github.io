import React from 'react'

const PrimaryBtn = ({children, onClick}) => {
  return (
    <a className='btn_primary' onClick={onClick}>
      {children}
    </a>
  )
}

export default PrimaryBtn

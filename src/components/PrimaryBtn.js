import React from 'react'

const PrimaryBtn = ({children, onClick, id}) => {
  return (
    <a href={id} className='btn_primary' onClick={onClick}>
      {children}
    </a>
  )
}

export default PrimaryBtn

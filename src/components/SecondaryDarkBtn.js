import React from 'react'

const SecondaryDarkBtn = ({children, onClick, id}) => {
  return (
    <a href={id} className='btn_secondary_dark' onClick={onClick}>
    {children}
    </a>
  )
}

export default SecondaryDarkBtn
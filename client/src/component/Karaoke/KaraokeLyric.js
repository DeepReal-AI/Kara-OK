import React from 'react';

export default function KaraokeLyric({text,percentage,activeStyle}){
    return(
        <span style={percentage>0?activeStyle:{color:"#ffffff"}}>{text}</span>
    )
}
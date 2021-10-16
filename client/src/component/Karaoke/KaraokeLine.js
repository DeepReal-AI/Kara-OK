import React from 'react';

import KaraokeLyric from './KaraokeLyric';
import {makeStyles} from '@mui/styles';

const useStyles = makeStyles({
    currentLyrics:{
        fontSize:"30px",
        width:"100%",
        margin:"auto"
    },
    passLyrics:{
        fontSize:"28px",
        opacity:0.5,
        width:"100%",
        margin:"auto"
    },
    nextLyrics:{
        fontSize:"28px",
        opacity:0.7,
        width:"100%",
        margin:"auto"
    }
    
});
//State: Current,Pass,Next
export default function KaraokeLine({state,data,songTime}){
    const classes = useStyles();
    function pf(n){
        return parseFloat(n);
    }
    

    if(state=="Current"){
        return (
            <div className={classes.currentLyrics}>
                {data.map(wordData=>{
                    
                    let percentage = pf(songTime)>pf(wordData.startTime)?100:0;
                    
                    console.log(`line songTime: ${songTime}`);
                    console.log(`line startTime: ${wordData.startTime}`);
                    console.log(`line percentage: ${percentage}`);

                    let activeStyle = {
                        color: "#f0e935"
                    };
                    return (
                    <>
                        <KaraokeLyric 
                        percentage={percentage} 
                        text={wordData.word}  
                        activeStyle={activeStyle}/>
                        {" "}
                    </>
                )})}
            </div>
        )
    }

    else if(state=="Pass"){
        return (
            <div className={classes.passLyrics}>
                {data.map(wordData=>{
                    
                    let activeStyle = {
                        color: "#eeeeee"
                    };
                    return (
                    <>
                        <KaraokeLyric 
                        percentage={100} 
                        text={wordData.word}  
                        activeStyle={activeStyle}/>
                        {" "}
                    </>
                )})}
            </div>
        )
    }

    else{
        return (
            <div className={classes.nextLyrics}>
                {data.map(wordData=>{
                    
                    let activeStyle = {
                        color: "#ffffff"
                    };
                    return (
                    <>
                        <KaraokeLyric 
                        percentage={100} 
                        text={wordData.word}  
                        activeStyle={activeStyle}/>
                        {" "}
                    </>
                )})}
            </div>
        )
    }

}
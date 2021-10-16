import React,{useState,useEffect} from 'react';
import {useParams} from 'react-router-dom';
import axios from 'axios';
import {Box,Button} from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPause,faPlay } from '@fortawesome/free-solid-svg-icons';
import KaraokeLine from './KaraokeLine';



export default function Karaoke(){
    const [lyrics,setLyrics] = useState(null);
    const [loading,setLoading] = useState(true);
    const [playing,setPlaying] = useState(false);
    const {songName} = useParams();
    const [audio,setAudio] = useState(null);
    const [index,setIndex] = useState(0);
    const [milestone,setMilestone] = useState(null);
    const [offset,setOffset] = useState(0);
    const [timer,setTimer] = useState(null);
    const [songTime,setSongTime] = useState(0);
    var myIndex = 0;
    useEffect(()=>{
        setAudio(new Audio(`/api/song/accom/${songName}`));
        axios.get(`/api/song/lyrics/${songName}`).then(res=>{
            setLyrics(res.data);
            setLoading(false);
            setMilestone(Date.now()/1000);
        }).catch(error=>console.log(error))
    },[]);

    function pf(n){
        return parseFloat(n);
    }

    function updateSongTime(){
        let currTime = Date.now()/1000;
        let newSongTime = (currTime-milestone+offset).toFixed(2);
        let nextLineTime = ()=>lyrics[myIndex+1][0]["startTime"].toFixed(2);
        setSongTime(newSongTime);
        console.log(newSongTime);
        console.log(nextLineTime());
        if(pf(newSongTime)>pf(nextLineTime())){
            console.log("greater");
            setIndex(index=>index+1);
            myIndex++;
        }
    }

    function togglePlaying(){
        if(playing){
            var currMilestone = Date.now()/1000;
            audio.pause();
            setOffset(offset+currMilestone-milestone);
            setMilestone(currMilestone);
            clearInterval(timer);
            setTimer(null);       

        }else{
            console.log("play audio");
            audio.play();
            setTimer(setInterval(updateSongTime,150));
        }
        setPlaying(!playing);
    }
    
    function generateLyricsParagraph(index){
        var para = [];
        for(let i=Math.max(0,index-2);i<index;i++){
            para.push(<KaraokeLine state="Pass" data={lyrics[i]} songTime={songTime}/>)
        }

        if(index>-1 && index<lyrics.length){
            para.push(<KaraokeLine state="Current" data={lyrics[index]} songTime={songTime}/>);
        }
        
        for(let i=index+1;i<Math.min(lyrics.length,index+3);i++){
            para.push(<KaraokeLine state="Next" data={lyrics[i]} songTime={songTime}/>)
        }
        // para.push(<p style={{color:"white"}}>{songTime}</p>)
        return para;
    }
    return (
        !loading &&(
            <Box sx={{width:"100%",height:"80%"}}>
                <Box sx={{width:"100%",height:"300px",background:"#000000"}}>
                    {generateLyricsParagraph(index)}      
                </Box>
                <Button variant="contained" 
                sx={{width:"50px",height:"50px",borderRadius:"50%"}}
                onClick={()=>{
                    console.log("Clicked");
                    togglePlaying();
                }}>
                    {playing
                    ?<FontAwesomeIcon icon={faPause} />
                    :<FontAwesomeIcon icon={faPlay} />}
                </Button>
            </Box>
        )
    )
}
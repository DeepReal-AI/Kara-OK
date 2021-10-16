import React,{useState,useEffect} from 'react';
import axios from 'axios';
import { Button,Box } from '@mui/material';
import {makeStyles} from '@mui/styles';

const useStyles = makeStyles({
    form:{
        background:"white",
        '& div':{
            margin: "20px auto",
            width: "50%",
            padding:"10px auto"
        },
        height:"85%",
        paddingTop:"30px"
    }
    
});

export default function FileUpload(){
    const classes = useStyles();
    const [name,setName]=useState("");
    const [musicFile,setMusicFile] = useState(null);
    const [songList,setSongList] = useState([]);
    useEffect(()=>{
        axios.get('/api/songs').then((res)=>{
            setSongList(res.data)
        }).catch((error)=>{
            console.log(error);
        })
    },[]);

    function handleNameChange(event){
        setName(event.target.value);
    }
    function handleFileChange(event){
        setMusicFile(event.target.files[0]);
    }
    function submitFile(event){
        if(!musicFile) return;
        if(songList.includes('name')) return;
        var data = new FormData();
        data.append('in_file',musicFile);
        data.append('name',name);
        var config = {
            method: 'post',
            url: '/api/convert',
            data : data
          };
          axios(config)
          .then(function (response) {
            console.log(JSON.stringify(response.data));
          })
          .catch(function (error) {
            console.log(JSON.stringify(error));
          });
          
    }
    return(
        <Box className={classes.form}>
                <div >
                <label>
                    Song's name: <input type='text' value={name} onChange={(event)=>{
                        handleNameChange(event)
                    }}></input>
                </label>
                </div>
                <div>
                <Button
                variant="contained"
                component="label"
                >
                Upload File
                <input
                    type="file"
                    onChange={handleFileChange}
                    hidden
                />
                
                </Button>
                <span> {musicFile?musicFile.name:""}</span>
                </div>
                
                <div>
                <Button variant="contained" onClick={(event)=>{
                    submitFile(event);
                }}>Submit</Button>
                </div>
                
        </Box>
    )
}
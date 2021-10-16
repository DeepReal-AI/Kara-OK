import React,{useState,useEffect} from 'react';
import {AppBar,Tabs,Tab,Typography,Box} from '@mui/material';
import { useHistory,useLocation } from 'react-router-dom';

export default function NavBar(){
    const route = ["/convert","/songs"];
    const [index,setIndex] = useState(2);
    const history = useHistory();
    const handleChange = (event,newValue)=>{
        if(newValue>=route.length){
            return;
        }
        history.push(route[newValue]);
        setIndex(newValue)
    }
    const location = useLocation();
    useEffect(()=>{
        for(var i=0;i<route.length;i++){
            if(route[i]==location.pathname){
                setIndex(i);
                break;
            }
        }
    },[])
    return (
        <Box sx={{bgcolor: "#170fff",width:1}}>
            <AppBar position="static">
                <Tabs 
                    value={index}
                    onChange={handleChange}
                    textColor="inherit"
                    variant="fullWidth"
                    >
                    <Tab label="Upload"/>
                    <Tab label="Songs"/>
                </Tabs>
            </AppBar>
        </Box>
    )
}
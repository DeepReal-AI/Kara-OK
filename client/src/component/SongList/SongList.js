import React,{useState,useEffect} from 'react';
import {Box,
    List,
    ListItem,
    ListItemButton,
    ListItemText,
    ListItemAvatar,
    Avatar,
    Divider,
    Link
} from '@mui/material';
import axios from 'axios';
import {Link as BrowserLink} from 'react-router-dom';
import MusicLogo from '../../static/music.png';

function renderRow(props) {
    const { index, song } = props;
  
    return (
        <>
        <Link
        component={BrowserLink} 
        to={`/song/${song}`}
        style={{textDecoration:'none'}}>
      <ListItem key={index} component="div" disablePadding  alignItems="flex-start">
      <ListItemAvatar>
          <Avatar alt="Music" src={MusicLogo} />
        </ListItemAvatar>
        <ListItemButton>
          <ListItemText 
          primary={`${song}`} />
        </ListItemButton>
      </ListItem>
      </Link>
      <Divider variant="inset" component="li" />
      </>
    );
  }

export default function SongList(){
    const [songList,setSongList] = useState([]);
    useEffect(()=>{
        axios.get('/api/songs').then((res)=>{
            setSongList(res.data)
        }).catch((error)=>{
            console.log(error);
        })
    },[]);
    return(
        <Box
      sx={{ width: '100%', height: '85%', bgcolor: 'background.paper'}}
    >
        <List sx={{padding:"30px"}}>
        {songList.map((song,index)=>renderRow({index,song}))}
        </List>
    </Box>
    )
}
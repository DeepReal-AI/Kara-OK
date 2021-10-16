import logo from './logo.svg';
import './App.css';
import { Container,Box } from '@mui/material';
import NavBar from './component/Navbar/NavBar';
import Router from './component/Router/Router';
function App() {
  return (
    <Container maxWidth={'sm'} >
      <Box sx={{height:"100vh"}}>
        <Router bar={<NavBar/>}></Router>
      </Box>
        
    </Container>
  );
}

export default App;

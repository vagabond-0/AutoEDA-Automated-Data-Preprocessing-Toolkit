import React from 'react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';
import About from './About';
import FileUpload from './FileUpload';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="relative w-full min-h-screen flex flex-col gap-2 bg-white">
      <div className="absolute top-4 right-4">
    <Button onClick={()=>navigate('/auth')} variant="outline">Sign Up/Log In</Button>
      </div>
     <About></About>
     <FileUpload></FileUpload>
    </div>
  );
};

export default Home;

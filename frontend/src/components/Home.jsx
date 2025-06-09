import React from 'react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="relative w-full min-h-screen bg-white">
      <div className="absolute top-4 right-4">
    <Button onClick={()=>navigate('/auth')} variant="outline">Auth</Button>
      </div>

      <div className="flex justify-center items-center min-h-screen w-full">
        <h1 className="text-3xl font-bold text-black">This is homepage</h1>
      </div>
    </div>
  );
};

export default Home;

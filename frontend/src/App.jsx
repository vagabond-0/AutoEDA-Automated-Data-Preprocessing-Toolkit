import React from 'react';
import AuthPage from './components/Auth';
import { ThemeProvider } from "@/components/theme-provider";
import { Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Dashboard from './components/Dashboard';
import Footer from './components/Footer'; //  Import Footer

const App = () => {
  return (
    <div className='w-full min-h-screen flex flex-col justify-between'>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <div className="flex-grow"> {/* So footer stays at bottom */}
          <Routes>
            <Route path='*' element={<Home />} />
            <Route path='/' element={<Home />} />
            <Route path='/auth' element={<AuthPage />} />
            <Route path='/dashboard' element={<Dashboard />} />
          </Routes>
        </div>
        <Footer /> {/* ✅ Add Footer here */}
      </ThemeProvider>
    </div>
  );
};

export default App;

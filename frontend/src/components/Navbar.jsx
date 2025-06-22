import { useState } from 'react';
import { Link as ScrollLink } from 'react-scroll';
import { useNavigate } from 'react-router-dom';
import { Menu, X, Sun, Moon } from 'lucide-react';
import { Button } from './ui/button';
import { useAuth0 } from "@auth0/auth0-react";
import { useTheme } from './theme-provider'; // ✅ import Theme context
import logg from './Aut.svg';
import loggd from './Autd.svg';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const { user, loginWithRedirect, isAuthenticated, logout } = useAuth0();
  const { theme, setTheme } = useTheme(); // ✅ use theme from context

  const navItems = [
    { name: 'About Us', to: 'about' },
    { name: 'How it works', to: 'how-it-works' },
    { name: 'Try Our Model', to: 'upload' },
    { name: 'Leave a Review', to: 'contact' },
  ];

  const toggleMenu = () => setIsOpen(!isOpen);

  const toggleDarkMode = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark'); // ✅ update global theme
  };

  const isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

  return (
    <nav className="fixed top-0 z-50 w-full border-b border-gray-200 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex-shrink-0">
            <img src={logg} alt="AutoEDA Logo" className="h-8 w-auto block dark:hidden" />
            <img src={loggd} alt="AutoEDA Logo" className="h-8 w-auto hidden dark:block" />
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-6">
              {navItems.map((item) => (
                <ScrollLink
                  key={item.to}
                  to={item.to}
                  spy={true}
                  smooth={true}
                  offset={-70}
                  duration={500}
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white cursor-pointer text-sm font-medium transition-colors"
                >
                  {item.name}
                </ScrollLink>
              ))}

              {/* Dark Mode Toggle */}
              <Button
                variant="ghost"
                onClick={toggleDarkMode}
                className="rounded-full p-2"
              >
                {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </Button>

              {/* Login / Signup */}
              {isAuthenticated ? (
                <Button onClick={() => logout()}>Logout</Button>
              ) : (
                <Button onClick={() => navigate('/auth')} variant="default">
                  Login / Signup
                </Button>
              )}
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="default"
              size="icon"
              onClick={toggleMenu}
              className="inline-flex items-center justify-center"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden">
          <div className="space-y-1 px-4 pb-3 pt-2">
            {navItems.map((item) => (
              <ScrollLink
                key={item.to}
                to={item.to}
                spy={true}
                smooth={true}
                offset={-70}
                duration={500}
                className="block rounded-md px-3 py-2 text-base font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white cursor-pointer"
                onClick={toggleMenu}
              >
                {item.name}
              </ScrollLink>
            ))}

            {/* Dark Mode Toggle Mobile */}
            <Button
              variant="ghost"
              onClick={() => {
                toggleDarkMode();
                toggleMenu();
              }}
              className="w-full flex justify-start space-x-2"
            >
              {isDark ? (
                <>
                  <Sun className="h-5 w-5" />
                  <span>Light Mode</span>
                </>
              ) : (
                <>
                  <Moon className="h-5 w-5" />
                  <span>Dark Mode</span>
                </>
              )}
            </Button>

            <Button
              onClick={() => {
                navigate('/auth');
                toggleMenu();
              }}
              variant="default"
              className="mt-2 w-full"
            >
              Login / Signup
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
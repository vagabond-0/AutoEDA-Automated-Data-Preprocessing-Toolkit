import { useState } from 'react';
import { Link as ScrollLink } from 'react-scroll';
import { useNavigate } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { Button } from './ui/button';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { name: 'About Us', to: 'about' },
    { name: 'How it works', to: 'how-it-works' },
    { name: 'Try Our Model', to: 'upload' },
    { name: 'Leave a Review', to: 'contact' },
  ];

  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <nav className="fixed top-0 z-50 w-full border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex-shrink-0">
            <span className="text-xl font-semibold text-gray-900">AutoEDA</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-8">
              {navItems.map((item) => (
                <ScrollLink
                  key={item.to}
                  to={item.to}
                  spy={true}
                  smooth={true}
                  offset={-64}
                  duration={500}
                  className="text-gray-600 hover:text-gray-900 cursor-pointer text-sm font-medium transition-colors"
                >
                  {item.name}
                </ScrollLink>
              ))}
              <Button
                onClick={() => navigate('/auth')}
                variant="default"
                className="ml-4"
              >
                Login / Signup
              </Button>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="default"
              size="icon"
              onClick={toggleMenu}
              className="inline-flex items-center justify-center"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
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
                offset={-64}
                duration={500}
                className="block rounded-md px-3 py-2 text-base font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 cursor-pointer"
                onClick={toggleMenu}
              >
                {item.name}
              </ScrollLink>
            ))}
            <Button
              onClick={() => {
                navigate('/auth');
                toggleMenu();
              }}
              variant="default"
              className="mt-4 w-full"
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

import React, { useState } from 'react';
import { Search, ShoppingCart, User, Menu, LogOut } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';

interface HeaderProps {
  cartItems: number;
  onSearchChange: (query: string) => void;
}

const Header = ({ cartItems, onSearchChange }: HeaderProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, logout } = useAuth();

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    onSearchChange(query);
  };

  const handleLogout = () => {
    logout();
    setIsMenuOpen(false);
  };

  return (
    <header className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">NM</span>
            </div>
            <span className="text-white text-xl font-bold">NightMarket</span>
          </Link>

          {/* Search Bar */}
          <div className="flex-1 max-w-2xl mx-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearchChange}
                placeholder="Search products..."
                className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <Link
              to="/cart"
              className="relative p-2 text-gray-300 hover:text-white transition-colors"
            >
              <ShoppingCart className="w-6 h-6" />
              {cartItems > 0 && (
                <span className="absolute -top-1 -right-1 bg-purple-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {cartItems}
                </span>
              )}
            </Link>
            
            {user ? (
              <div className="flex items-center space-x-2">
                <span className="text-gray-300 hidden sm:block">Welcome, {user.username}</span>
                <Button
                  onClick={handleLogout}
                  variant="ghost"
                  size="sm"
                  className="text-gray-300 hover:text-white"
                >
                  <LogOut className="w-4 h-4 mr-1" />
                  Logout
                </Button>
              </div>
            ) : (
              <Link to="/login">
                <Button variant="outline" size="sm" className="text-gray-300 border-gray-600 hover:bg-gray-800">
                  <User className="w-4 h-4 mr-1" />
                  Login
                </Button>
              </Link>
            )}
            
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-300 hover:text-white transition-colors"
            >
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-800">
            <nav className="space-y-2">
              <Link to="/" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded">
                Home
              </Link>
              <Link to="/cart" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded">
                Cart ({cartItems})
              </Link>
              {user ? (
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded"
                >
                  Logout ({user.username})
                </button>
              ) : (
                <Link to="/login" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded">
                  Login
                </Link>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;

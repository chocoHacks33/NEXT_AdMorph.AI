
import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import CategoryFilter from '../components/CategoryFilter';
import ProductGrid from '../components/ProductGrid';
import { Product } from '../components/ProductCard';
import { sampleProducts } from '../data/products';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface IndexProps {
  cartItems: number;
  onAddToCart: (product: Product) => void;
  onProductSelect: (product: Product) => void;
}

const Index = ({ cartItems, onAddToCart, onProductSelect }: IndexProps) => {
  const [products] = useState<Product[]>(sampleProducts);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>(products);
  const [searchQuery, setSearchQuery] = useState('');
  const { user } = useAuth();
  
  // Set initial category to "food" if user is logged in, otherwise "all"
  const [selectedCategory, setSelectedCategory] = useState(user ? 'food' : 'all');
  const navigate = useNavigate();

  const categories = [...new Set(products.map(product => product.category))];

  useEffect(() => {
    let filtered = products;

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.category.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredProducts(filtered);
  }, [selectedCategory, searchQuery, products]);

  const handleProductClick = (product: Product) => {
    onProductSelect(product);
    navigate('/product');
  };

  return (
    <div className="min-h-screen bg-black">
      <Header
        cartItems={cartItems}
        onSearchChange={setSearchQuery}
      />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <CategoryFilter
              categories={categories}
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
            />
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-white mb-2">
                {selectedCategory === 'all' ? 'All Products' : `${selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1)} Products`}
              </h1>
              <p className="text-gray-400">
                {filteredProducts.length} {filteredProducts.length === 1 ? 'product' : 'products'} found
                {searchQuery && ` for "${searchQuery}"`}
              </p>
            </div>

            <ProductGrid
              products={filteredProducts}
              onAddToCart={onAddToCart}
              onProductClick={handleProductClick}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;


import React from 'react';
import { ShoppingCart, Star } from 'lucide-react';

export interface Product {
  id: number;
  name: string;
  price: number;
  originalPrice?: number;
  rating: number;
  reviews: number;
  image: string;
  category: string;
  description: string;
  inStock: boolean;
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
  onProductClick: (product: Product) => void;
}

const ProductCard = ({ product, onAddToCart, onProductClick }: ProductCardProps) => {
  const discountPercentage = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0;

  return (
    <div className="bg-gray-900 rounded-lg overflow-hidden border border-gray-800 hover:border-gray-700 transition-all duration-300 hover:scale-105 cursor-pointer">
      <div onClick={() => onProductClick(product)}>
        <div className="relative">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-48 object-cover"
          />
          {discountPercentage > 0 && (
            <div className="absolute top-2 left-2 bg-red-600 text-white px-2 py-1 rounded-lg text-sm font-bold">
              -{discountPercentage}%
            </div>
          )}
          {!product.inStock && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <span className="text-white font-bold text-lg">Out of Stock</span>
            </div>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="text-white font-semibold text-lg mb-2 line-clamp-2">{product.name}</h3>
          
          <div className="flex items-center mb-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.floor(product.rating)
                      ? 'text-yellow-500 fill-current'
                      : 'text-gray-600'
                  }`}
                />
              ))}
            </div>
            <span className="text-gray-400 text-sm ml-2">({product.reviews})</span>
          </div>

          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-white font-bold text-xl">${product.price}</span>
              {product.originalPrice && (
                <span className="text-gray-500 line-through text-sm">${product.originalPrice}</span>
              )}
            </div>
          </div>
        </div>
      </div>
      
      <div className="px-4 pb-4">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onAddToCart(product);
          }}
          disabled={!product.inStock}
          className={`w-full flex items-center justify-center space-x-2 py-2 px-4 rounded-lg transition-colors ${
            product.inStock
              ? 'bg-purple-600 hover:bg-purple-700 text-white'
              : 'bg-gray-700 text-gray-400 cursor-not-allowed'
          }`}
        >
          <ShoppingCart className="w-4 h-4" />
          <span>{product.inStock ? 'Add to Cart' : 'Out of Stock'}</span>
        </button>
      </div>
    </div>
  );
};

export default ProductCard;


import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Star, ShoppingCart, Heart } from 'lucide-react';
import { Product } from '../components/ProductCard';

interface ProductDetailProps {
  product: Product | null;
  onAddToCart: (product: Product) => void;
}

const ProductDetail = ({ product, onAddToCart }: ProductDetailProps) => {
  const [selectedImage, setSelectedImage] = useState(0);
  const [quantity, setQuantity] = useState(1);

  if (!product) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Product not found</h1>
          <Link
            to="/"
            className="text-purple-400 hover:text-purple-300"
          >
            Return to marketplace
          </Link>
        </div>
      </div>
    );
  }

  const discountPercentage = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0;

  const handleAddToCart = () => {
    for (let i = 0; i < quantity; i++) {
      onAddToCart(product);
    }
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link
          to="/"
          className="inline-flex items-center space-x-2 text-purple-400 hover:text-purple-300 mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to marketplace</span>
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Product Images */}
          <div className="space-y-4">
            <div className="aspect-square bg-gray-900 rounded-lg overflow-hidden">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <p className="text-purple-400 text-sm font-medium uppercase tracking-wide mb-2">
                {product.category}
              </p>
              <h1 className="text-3xl font-bold text-white mb-4">{product.name}</h1>
              
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-5 h-5 ${
                        i < Math.floor(product.rating)
                          ? 'text-yellow-500 fill-current'
                          : 'text-gray-600'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-gray-400 ml-2">
                  {product.rating} ({product.reviews} reviews)
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-3xl font-bold text-white">${product.price}</span>
              {product.originalPrice && (
                <>
                  <span className="text-xl text-gray-500 line-through">
                    ${product.originalPrice}
                  </span>
                  <span className="bg-red-600 text-white px-2 py-1 rounded text-sm font-bold">
                    -{discountPercentage}% OFF
                  </span>
                </>
              )}
            </div>

            <p className="text-gray-300 text-lg leading-relaxed">
              {product.description}
            </p>

            {product.inStock ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <span className="text-white font-medium">Quantity:</span>
                  <div className="flex items-center border border-gray-700 rounded-lg">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                    >
                      -
                    </button>
                    <span className="px-4 py-2 text-white bg-gray-900">{quantity}</span>
                    <button
                      onClick={() => setQuantity(quantity + 1)}
                      className="px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                    >
                      +
                    </button>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={handleAddToCart}
                    className="flex-1 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
                  >
                    <ShoppingCart className="w-5 h-5" />
                    <span>Add to Cart</span>
                  </button>
                  <button className="p-3 border border-gray-700 hover:border-gray-600 rounded-lg text-gray-400 hover:text-white transition-colors">
                    <Heart className="w-6 h-6" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
                <p className="text-red-400 font-semibold">Currently out of stock</p>
                <p className="text-gray-400 text-sm mt-1">
                  We'll notify you when this item is back in stock.
                </p>
              </div>
            )}

            <div className="border-t border-gray-800 pt-6">
              <h3 className="text-white font-semibold mb-3">Product Details</h3>
              <ul className="space-y-2 text-gray-300">
                <li>• Free shipping on orders over $50</li>
                <li>• 30-day return policy</li>
                <li>• 1-year manufacturer warranty</li>
                <li>• Secure payment processing</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
